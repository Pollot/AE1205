from math import sqrt

while True:
    try:
        a = float(input("Input the first side of the triangle: "))
        b = float(input("Input the second side of the triangle: "))
        if a <= 0 or b <= 0:
            print("Sides must be numbers above 0 (can be floats)!")
            continue
        break
    except ValueError:
        print("Input sides as numbers (can be floats)!")

c = sqrt(a**2 + b**2)

print(f"The hypotenuse is: {c:g}")  # :g removes trailing zero if the hypotenuse is an integer
