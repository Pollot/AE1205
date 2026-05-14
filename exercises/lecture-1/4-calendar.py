days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_date(question):
    while True:
        try:
            date = input(question)
            date = date.split(".")
            day = int(date[0])
            month = int(date[1])
            year = int(date[2])

            max_days = days_per_month[month - 1]  # -1, because the index starts at 0
            if month == 2 and check_leap_year(year):
                max_days = 29
            
            if year < 1:
                print("Invalid year!")
            elif month < 1 or month > 12:
                print("Invalid month!")
            elif day < 1 or day > max_days:
                print("Invalid day!")
            else:
                return [day, month, year]
        except (ValueError, IndexError):
            print("Enter a valid date!")

# Returns absolute number of days since year 1, 01.01.0001 = day 1
def abs_num_days(date: list) -> int:
    days = date[0]
    days_month = sum(days_per_month[0:(date[1] - 1)])  # -1 to exclude the current month
    days_year = (date[2] - 1) * 365  # -1 to exclude the current year
    days_leap = count_leap_years(date)
    return days + days_month + days_year + days_leap

# Counts passed leap years
def count_leap_years(date: list) -> int:
    cur_year = date[2]
    count = 0
    for year in range(1, cur_year):  # Start from 1 to avoid counting "year 0"
        if check_leap_year(year):
            count += 1
    # Add an additional leap day if the current year is a leap year and the month has passed February
    if check_leap_year(cur_year) and date[1] > 2:
        count += 1
    return count

def check_leap_year(year: int) -> bool:
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        return True
    else:
        return False

# 01.01.0001 is used as a reference
# It was a Monday in the proleptic Gregorian calendar and matches the list of weekdays
# The proleptic Gregorian calendar extends the Gregorian calendar (introduced in 1582) backwards
def get_weekday(date: list) -> str:
    return weekdays[(abs_num_days(date) - 1) % 7]  # -1, because the index 0 of the list corresponds to day 1 of the calendar

date_1 = get_date("Enter the first date (dd.mm.yyyy): ")
date_2 = get_date("Enter the second date (dd.mm.yyyy): ")

abs_diff = abs(abs_num_days(date_1) - abs_num_days(date_2))

print(f"The number of days between the dates is: {abs_diff}")

weekday_1 = get_weekday(date_1)
weekday_2 = get_weekday(date_2)

print(f"The weekday of {date_1[0]:02d}.{date_1[1]:02d}.{date_1[2]:04d} is: {weekday_1}")
print(f"The weekday of {date_2[0]:02d}.{date_2[1]:02d}.{date_2[2]:04d} is: {weekday_2}")
