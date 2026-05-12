while True:
    raw_time_input = input("Enter the time in hh:mm format: ")
    if ":" not in raw_time_input:
        print("Include \":\" as the separator between hours and minutes!")
        continue

    try:
        hour_value = int(raw_time_input.split(":")[0])
        minute_value = int(raw_time_input.split(":")[1])
    except ValueError:
        print("Enter the time as integers!")
        continue
    
    if not 0 <= hour_value < 24:
        print("Enter an hour from 0 to 23!")
        continue
    elif not 0 <= minute_value < 60:
        print("Enter minutes from 0 to 59!")
        continue
    else:
        break

# Convert 24-hour to 12-hour for angle calculations
if hour_value >= 12:
    hour_value -= 12

# Calculate the hand angles with respect to the 12
hour_hand_angle = (hour_value + minute_value / 60) * 30
minute_hand_angle = minute_value * 6  # Comes from 360 deg swept in 60 min => 360/60

hand_diff = abs(hour_hand_angle - minute_hand_angle)

# Get the smallest difference between hand angles
if hand_diff > 180:
    hand_diff = 360 - hand_diff

print(f"The angle between the hour and minute hands is: {hand_diff} degrees")
