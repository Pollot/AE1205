from math import pi, sin, cos, radians, atan2, degrees
import matplotlib.pyplot as plt

# Castle location
h_0 = 60      # [m]
delta_x = 300 # [m]

# Physics parameters
g_0 = 9.81    # [m/s^2]
rho_0 = 1.225 # [kg/m^3]

# Simulation parameters
tick_rate = 10000     # [Hz = 1/s]
delta_t = 1/tick_rate # [s]

def cow_catapult(R, angle_start, angle_end, L_0, k_elas, m_cow):
    # Living stock parameters
    rho_cow = 1000 # [kg/m^3]
    volume_cow = m_cow / rho_cow           # [m^3]
    r_cow = (3/4 * volume_cow / pi)**(1/3) # [m]
    C_d = 0.7     # [-]
    S = pi * r_cow**2 # [m^2]
    
    # Elapsed time
    t = 0

    # Initial angle, speed and acceleration
    cur_angle = angle_start
    angle_spd = 0
    angle_acc = 0

    # Lists to collect all the data for later plotting
    time_list = []
    x_list = []
    h_list = []
    speed_list = []
    flight_angle_list = []

    # Euler integration of the first part: the launch
    while cur_angle < angle_end:    
        x = -cos(radians(cur_angle)) * R
        y = sin(radians(cur_angle)) * R
        current_speed = angle_spd * R
        current_flight_angle = 90 - cur_angle

        time_list.append(t)
        x_list.append(x)
        h_list.append(y)
        speed_list.append(current_speed)
        flight_angle_list.append(current_flight_angle)

        # Current lenght of the elastic band based on the cosine rule
        L_elas = (R**2 + R**2 - 2 * R * R * cos(radians(90 - cur_angle)))**(1/2)

        F_elas = k_elas * (L_elas - L_0) # [N]

        # The angle between the elastic cord and the swinging arm
        gamma = 45 + cur_angle/2

        # Decomposition of the elastic force
        F_rad = F_elas * cos(radians(gamma))
        F_tan = F_elas * sin(radians(gamma))

        F_grav = g_0 * m_cow # [N]

        # Adding the decomposition of the gravitational force
        F_rad += F_grav * cos(radians(90 - cur_angle))
        F_tan -= F_grav * sin(radians(90 - cur_angle))

        a_tan = F_tan / m_cow # [m/s^2]

        angle_acc = a_tan / R # [rad/s^2]
        angle_spd += angle_acc * delta_t # [rad/s]
        cur_angle += angle_spd * delta_t * 180 / pi # [deg]

        t += delta_t

    # Exit velocity from the launch/initial projectile motion velocity
    v_exit = angle_spd * R
    print(f"Exit velocity: {v_exit:.3f}")

    v_x = v_exit * cos(radians(90 - angle_end))
    v_y = v_exit * sin(radians(90 - angle_end))

    # Euler integration of the first part: the projectile motion
    while y > -h_0:
        v_total = (v_x**2 + v_y**2)**(1/2) # [m/s]
        F_drag = C_d * 1/2 * rho_0 * v_total**2 * S # [N]
        a_drag = F_drag / m_cow # [m/s^2]

        a_drag_x = a_drag * (v_x / v_total)
        a_drag_y = a_drag * (v_y / v_total)

        a_x = -a_drag_x
        a_y = -a_drag_y - g_0

        v_x += a_x * delta_t
        v_y += a_y * delta_t
        current_speed = (v_x**2 + v_y**2)**(1/2)
        current_flight_angle = degrees(atan2(v_y, v_x))

        x += v_x * delta_t
        y += v_y * delta_t
        time_list.append(t)
        x_list.append(x)
        h_list.append(y)
        speed_list.append(current_speed)
        flight_angle_list.append(current_flight_angle)

        t += delta_t

    return time_list, x_list, h_list, speed_list, flight_angle_list

# Catapult input parameters
R = 10          # [m]
angle_start = 0 # [deg]
angle_end = 60  # [deg]
L_0 = 0.5       # [m]
k_elas = 12000   # [N/m]
m_cow = 550     # [kg]

time_list, x_list, h_list, speed_list, flight_angle_list = cow_catapult(R, angle_start, angle_end, L_0, k_elas, m_cow)

print(f"Distance achieved: {x_list[-1]:.3f}")

'''
# Plot the trajectory (h vs x)
plt.plot(x_list, h_list)
plt.xlabel("Distance (m)")
plt.ylabel("Height (m)")
plt.title("Cow Trajectory")
plt.grid(True)
plt.show()
'''

plt.figure(figsize=(10, 5))
plt.plot(x_list, h_list, color='blue', linewidth=2, label='Cow Path')

plt.title(f"Cow Trajectory (Final Distance: {x_list[-1]:.3f} m)")
plt.xlabel("Distance [m]")
plt.ylabel("Height [m]")
plt.grid(True)

# Second window
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 8))
fig.suptitle("Cow speed and flight angle", fontsize=14)

# Plot 1
ax1.plot(time_list, speed_list, color='purple')
ax1.set_ylabel("Speed [m/s]")
ax1.grid(True)

# Plot 2
ax2.plot(time_list, flight_angle_list, color='orange')
ax2.set_ylabel("Flight Angle [deg]")
ax2.set_xlabel("Time [s]")
ax2.grid(True)

plt.tight_layout()
plt.show()
