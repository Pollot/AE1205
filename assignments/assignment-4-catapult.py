from math import pi, sin, cos, radians
import matplotlib.pyplot as plt

# Castle location
h_0 = 60      # [m]
delta_x = 300 # [m]

# Catapult parameters
R = 10          # [m]
angle_start = 0 # [deg]
angle_end = 60  # [deg]
L_0 = 0.5       # [m]
k_elas = 9000   # [N/m]

# Living stock parameters
m_cow = 550    # [kg]
rho_cow = 1000 # [kg/m^3]
volume_cow = m_cow / rho_cow           # [m^3]
r_cow = (3/4 * volume_cow / pi)**(1/3) # [m]

# Physics parameters
g_0 = 9.81 # [m/s^2]

# Simulation parameters
tick_rate = 10000     # [Hz = 1/s]
delta_t = 1/tick_rate # [s]

# Elapsed time
t = 0

# Initial angle, speed and acceleration
cur_angle = angle_start
angle_spd = 0
angle_acc = 0

# Lists to collect all the data for later plotting
time_list = []
angle_list = []
angle_spd_list = []
angle_acc_list = []
pos = []

# Euler integration of the first part: the launch
while cur_angle < angle_end:
    time_list.append(t)
    angle_list.append(cur_angle)
    angle_spd_list.append(angle_spd)
    angle_acc_list.append(angle_acc)
    
    x = cos(radians(cur_angle)) * R
    y = sin(radians(cur_angle)) * R
    pos.append([t, x, y])

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
v_0 = angle_spd * R
print(f"Exit velocity: {v_0}")

'''
# AI code to plot the launch phases
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(8, 10))

# --- Graph 1: Angle ---
ax1.plot(time_list, angle_list, color='red', label="Angle")
ax1.set_ylabel("Angle (deg)")
ax1.set_title("Catapult Angular Dynamics") # Title for the top of the overall stack
ax1.grid(True)

# --- Graph 2: Angular Velocity ---
ax2.plot(time_list, angle_spd_list, color='green', label="Velocity")
ax2.set_ylabel("Angular Velocity (rad/s)")
ax2.grid(True)

# --- Graph 3: Angular Acceleration ---
ax3.plot(time_list, angle_acc_list, color='blue', label="Acceleration")
ax3.set_ylabel("Angular Accel (rad/s²)")
ax3.set_xlabel("Time (s)")  # Only need to label the bottom X-axis because sharex=True
ax3.grid(True)

plt.tight_layout()
plt.show()
'''
