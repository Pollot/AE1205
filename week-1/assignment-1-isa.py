from math import exp

# Constants
G_0 = 9.80665
R = 287

# Initial variables
h_0 = 0
t_0 = 288.15
p_0 = 101325
a = -0.0065

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

if h <= 11000:
    output(*gradient(a, t_0, h, h_0, p_0))

elif h <= 20000:
    (t_0, p_0, rho) = gradient(a, t_0, 11000, h_0, p_0)
    h_0 = 11000
    output(*isothermal(t_0, h, h_0, p_0))

elif h <= 32000:
    (t_0, p_0, rho) = gradient(a, t_0, 11000, h_0, p_0)
    h_0 = 11000
    (t_0, p_0, rho) = isothermal(t_0, 20000, h_0, p_0)
    h_0 = 20000
    a = 0.001
    output(*gradient(a, t_0, h, h_0, p_0))

elif h <= 47000:
    (t_0, p_0, rho) = gradient(a, t_0, 11000, h_0, p_0)
    h_0 = 11000
    (t_0, p_0, rho) = isothermal(t_0, 20000, h_0, p_0)
    h_0 = 20000
    a = 0.001
    (t_0, p_0, rho) = gradient(a, t_0, 32000, h_0, p_0)
    h_0 = 32000
    a = 0.0028
    output(*gradient(a, t_0, h, h_0, p_0))

elif h <= 51000:
    (t_0, p_0, rho) = gradient(a, t_0, 11000, h_0, p_0)
    h_0 = 11000
    (t_0, p_0, rho) = isothermal(t_0, 20000, h_0, p_0)
    h_0 = 20000
    a = 0.001
    (t_0, p_0, rho) = gradient(a, t_0, 32000, h_0, p_0)
    h_0 = 32000
    a = 0.0028
    (t_0, p_0, rho) = gradient(a, t_0, 47000, h_0, p_0)
    h_0 = 47000
    output(*isothermal(t_0, h, h_0, p_0))

elif h <= 71000:
    (t_0, p_0, rho) = gradient(a, t_0, 11000, h_0, p_0)
    h_0 = 11000
    (t_0, p_0, rho) = isothermal(t_0, 20000, h_0, p_0)
    h_0 = 20000
    a = 0.001
    (t_0, p_0, rho) = gradient(a, t_0, 32000, h_0, p_0)
    h_0 = 32000
    a = 0.0028
    (t_0, p_0, rho) = gradient(a, t_0, 47000, h_0, p_0)
    h_0 = 47000
    (t_0, p_0, rho) = isothermal(t_0, 51000, h_0, p_0)
    h_0 = 51000
    a = -0.0028
    output(*gradient(a, t_0, h, h_0, p_0))

elif h <= 86000:
    (t_0, p_0, rho) = gradient(a, t_0, 11000, h_0, p_0)
    h_0 = 11000
    (t_0, p_0, rho) = isothermal(t_0, 20000, h_0, p_0)
    h_0 = 20000
    a = 0.001
    (t_0, p_0, rho) = gradient(a, t_0, 32000, h_0, p_0)
    h_0 = 32000
    a = 0.0028
    (t_0, p_0, rho) = gradient(a, t_0, 47000, h_0, p_0)
    h_0 = 47000
    (t_0, p_0, rho) = isothermal(t_0, 51000, h_0, p_0)
    h_0 = 51000
    a = -0.0028
    (t_0, p_0, rho) = gradient(a, t_0, 71000, h_0, p_0)
    h_0 = 71000
    a = -0.002
    output(*gradient(a, t_0, h, h_0, p_0))
