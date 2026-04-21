from math import exp

# Constants
G_0 = 9.80665
R = 287

# Initial variables
t_0 = 288.15
p_0 = 101325

while True:
    try:
        h = float(input("Enter altitude [m]: "))
        if h < 0 or h > 86000:
            print("Incorrrect altitude! It needs to be a value between 0 and 86 000 m")
        else:
            break
    except ValueError:
        print("The altitude needs to be a number!")

def output(t, p, rho):
    print(f"Temperature: {round(t, 2)} [K] ({round(t-273.15, 2)} [C])")
    print(f"Pressure: {int(round(p, 0))} [Pa]") # Using int without round would cause the decimals to be clipped
    print(f"Density: {round(rho, 4)} [kg/m^3]")

def gradient(a, t_0, h, h_0, p_0):
    t = t_0 + a * (h - h_0)
    p = (t/t_0)**(-G_0/(a*R)) * p_0
    rho = p/(R*t)
    return t, p, rho

def isothermal(t_0, h, h_0, p_0):
    t = t_0
    p = exp(-G_0/(R*t)*(h-h_0)) * p_0
    rho = p/(R*t)
    return t, p, rho

# layers boundaries calculations
t_11, p_11, rho_11 = gradient(-0.0065, t_0, 11000, 0, p_0)
t_20, p_20, rho_20 = isothermal(t_11, 20000, 11000, p_11)
t_32, p_32, rho_32 = gradient(0.001, t_20, 32000, 20000, p_20)
t_47, p_47, rho_47 = gradient(0.0028, t_32, 47000, 32000, p_32)
t_51, p_51, rho_51 = isothermal(t_47, 51000, 47000, p_47)
t_71, p_71, rho_71 = gradient(-0.0028, t_51, 71000, 51000, p_51)

if h <= 11000:
    result = gradient(-0.0065, t_0, h, 0, p_0)
elif h <= 20000:
    result = isothermal(t_11, h, 11000, p_11)
elif h <= 32000:
    result = gradient(0.001, t_20, h, 20000, p_20)
elif h <= 47000:
    result = gradient(0.0028, t_32, h, 32000, p_32)
elif h <= 51000:
    result = isothermal(t_47, h, 47000, p_47)
elif h <= 71000:
    result = gradient(-0.0028, t_51, h, 51000, p_51)
else:
    result = gradient(-0.002, t_71, h, 71000, p_71)

output(*result)
