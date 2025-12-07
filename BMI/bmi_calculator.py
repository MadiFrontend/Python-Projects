# Global Variables and Imports


# getting user inputs - Height and Weight
def get_user_inputs():
    weight = float(input("Enter your Weight (Kg): "))
    height = float(input("Enter your Height (M): "))
    return weight, height


# calculate BMI
def calculate_bmi(weight, height):
    return weight // (height**2)


# Get the BMI Result
def get_bmi_result(bmi):
    if bmi < 18.5:
        print("Underweight")
    elif 18.5 <= bmi < 25:
        print("Normal weight")
    elif 25 <= bmi < 30:
        print("Overweight")
    elif 30 <= bmi < 35:
        print("Obse")
    else:
        print("extreme Obese")


# Main function to run the BMI calculator
def main():
    weight, height = get_user_inputs()
    bmi = calculate_bmi(weight, height)
    print(f"Your BMI is: {bmi}")
    get_bmi_result(bmi)


if __name__ == "__main__":
    main()
