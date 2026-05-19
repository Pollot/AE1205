from math import pi, sin, cos, atan2, radians, degrees
import matplotlib.pyplot as plt

# Castle location
h_0 = 60      # [m]
delta_x = 300 # [m]

# Physics parameters
g_0 = 9.81      # [m/s^2]
rho_air = 1.225 # [kg/m^3]

# Simulation parameters
tick_rate = 10000     # [Hz]
delta_t = 1/tick_rate # [s]

def cow_catapult(R, phi_start, phi_stop, L_0, k_elas, m_cow):
    # Livestock parameters
    rho_cow = 1000                      # [kg/m^3]
    vol_cow = m_cow / rho_cow           # [m^3]
    r_cow = (3/4 * vol_cow / pi)**(1/3) # [m], derived from sphere volume formula
    S = pi * r_cow**2                   # [m^2]
    C_D = 0.7                           # [-]

    # Elapsed time
    t = 0

    # Initial position, angle, speed and acceleration
    x = R * -cos(radians(phi_start))
    y = R * sin(radians(phi_start))
    phi = phi_start
    phi_spd = 0
    phi_acc = 0

    # Lists to collect all the data for later plotting
    t_list = []
    x_list = []
    h_list = []
    spd_list = []
    fpa_list = [] # Flight Path Angle

    # First part: launch motion
    while phi < phi_stop:
        # The hinge of the catapult is the origin (0,0)
        x = R * -cos(radians(phi))
        y = R * sin(radians(phi))
        linear_spd = phi_spd * R
        fpa = 90 - phi

        t_list.append(t)
        x_list.append(x)
        h_list.append(y)
        spd_list.append(linear_spd)
        fpa_list.append(fpa)

        # Current length of the elastic band using cosine rule
        L_elas = (R**2 + R**2 - 2 * R * R * cos(radians(90 - phi)))**(1/2) # [m]

        # Elastic force using Hooke's law
        F_elas = k_elas * (L_elas - L_0) # [N]

        # The angle between the elastic cord and the swinging arm
        gamma = 45 + phi/2 # [deg]

        # Decomposition of the elastic force into tangent and radial components (n-t coordinates)
        F_tan = F_elas * sin(radians(gamma)) # [N]
        F_rad = F_elas * cos(radians(gamma)) # [N]

        # Adding the decomposition of the gravitational force
        F_grav = m_cow * g_0                     # [N]
        F_tan -= F_grav * sin(radians(90 - phi)) # [N], "-" comes from the opposite direction/negative contribution
        F_rad += F_grav * cos(radians(90 - phi)) # [N]

        a_tan = F_tan / m_cow # [m/s^2], uses F = ma
        phi_acc = a_tan / R   # [rad/s^2]

        # Euler integration
        phi_spd += phi_acc * delta_t        # [rad/s]
        phi += phi_spd * delta_t * 180 / pi # [deg]

        t += delta_t

    # Launch velocity from the catapult/initial velocity of the projectile motion
    v_launch = phi_spd * R # [m/s]
    print(f"Launch velocity: {v_launch:.3f}")

    # Decomposition of the exit velocity into x-y components
    v_x = v_launch * cos(radians(90 - phi_stop)) # [m/s]
    v_y = v_launch * sin(radians(90 - phi_stop)) # [m/s]

    # Second part: projectile motion
    while y > -h_0:
        v_total = (v_x**2 + v_y**2)**(1/2)            # [m/s]
        F_drag = C_D * 1/2 * rho_air * v_total**2 * S # [N]
        a_drag = F_drag / m_cow                       # [m/s^2]

        # Decompose the drag acceleration into x-y components
        # Uses direction specified by the velocity unit vector: v/v_total = <v_x/v_total, v_y/v_total>
        # The drag unit vector is the same, just with the opposite direction, hence the minus sign
        a_drag_x = - a_drag * (v_x / v_total)
        a_drag_y = - a_drag * (v_y / v_total)

        # Total acceleration in x-y components
        a_x = a_drag_x
        a_y = a_drag_y - g_0

        # Euler integration
        v_x += a_x * delta_t
        v_y += a_y * delta_t
        x += v_x * delta_t
        y += v_y * delta_t

        fpa = degrees(atan2(v_y, v_x)) # The velocity vector is v_x + v_y, so to get the FPA (angle between the velocity vector and the horizon), use arctan(v_y / v_x), atan2 takes y and x components and handles the sign and div by 0

        t_list.append(t)
        x_list.append(x)
        h_list.append(y)
        spd_list.append(v_total)
        fpa_list.append(fpa)

        t += delta_t

    return t_list, x_list, h_list, spd_list, fpa_list

# Catapult input parameters
R = 10         # [m]
phi_start = 0  # [deg]
phi_stop = 60  # [deg]
L_0 = 0.5      # [m]
k_elas = 10160 # [N/m], 9000 was the initial value, 10160 results in a distance of 300 m
m_cow = 550    # [kg]

t_list, x_list, h_list, spd_list, fpa_list = cow_catapult(R, phi_start, phi_stop, L_0, k_elas, m_cow)

# Main window
plt.figure(figsize=(10, 5))
plt.plot(x_list, h_list, color="blue", linewidth=2, label="Cow Trajectory")

# Trajectory plot
plt.title(f"Cow Trajectory (Final Distance: {x_list[-1]:.2f} m)")
plt.xlabel("Distance [m]")
plt.ylabel("Height [m]")
plt.grid(True)

# Additional ground and target constant lines
plt.axhline(y=-h_0, color="red", linestyle="-", label=f"Ground ({-h_0} m)")
plt.axvline(x=delta_x, color="green", linestyle="--", label=f"Target Distance ({delta_x} m)")

plt.legend()

# Second window
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 8))
fig.suptitle("Cow Telemetry: Speed and Flight Path Angle", fontsize=14)

# Speed plot
ax1.plot(t_list, spd_list, color="green")
ax1.set_ylabel("Speed [m/s]")
ax1.grid(True)

# FPA plot
ax2.plot(t_list, fpa_list, color="orange")
ax2.set_ylabel("Flight Path Angle [deg]")
ax2.set_xlabel("Time [s]")
ax2.grid(True)

plt.tight_layout()
plt.show()
