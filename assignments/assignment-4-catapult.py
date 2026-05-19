from math import pi, sin, cos

# Castle location
h_0 = 60      # [m]
delta_x = 300 # [m]

# Catapult parameters
R = 10           # [m]
angle_start = 0  # [deg]
angle_end = 60   # [deg]
L_0 = 0.5        # [m]
k_elastic = 9000 # [N/m]

# Living stock parameters
m_cow = 550    # [kg]
rho_cow = 1000 # [kg/m^3]
volume_cow = m_cow / rho_cow           # [m^3]
r_cow = (3/4 * volume_cow / pi)**(1/3) # [m]

print(f"Volume: {volume_cow}, r: {r_cow}")

# Initial x position of the cow
x_0 = cos(angle_start) * R

# Initial y position of the cow
y_0 = sin(angle_start) * R

cow_pos = [x_0, y_0]

print(f"Current cow position: {cow_pos}")
