def input_num(question, response):
    while True:
        try:
            num = float(input(question))
            return num
        except ValueError:
            print(response)

amount = input_num("Enter the amount: ", "Enter the amount as a valid number!")
percent = input_num("Enter a yearly interest rate (in percent): ", "Do not include a percent \"%\" sign!")
years = input_num("Enter a number of years: ", "Enter a valid number!")

final_amount = amount * (1 + percent/100)**years

print(f"The final amount for {amount:g} at a {percent:g}% interest rate after {years:g} year(s) is: {final_amount:.2f}")
