# cli_bmi_calculator.py

def calculate_bmi(weight, height, height_unit):
    """
    Calculate BMI using the formula: BMI = weight / (height^2)
    
    Args:
        weight (float): Weight in kilograms
        height (float): Height value
        height_unit (str): Unit of height ('m', 'cm', 'ft')
    
    Returns:
        float: Calculated BMI value
    """
    # Convert height to meters first
    if height_unit == 'cm':
        height_m = height / 100
    elif height_unit == 'ft':
        height_m = height * 0.3048  # 1 ft = 0.3048 m
    else:  # meters
        height_m = height
    
    return weight / (height_m ** 2)

def classify_bmi(bmi):
    """
    Classify BMI into categories based on WHO standards
    
    Args:
        bmi (float): BMI value
    
    Returns:
        str: BMI category
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_valid_input(prompt, input_type=float, min_val=0, max_val=300):
    """
    Get and validate user input
    
    Args:
        prompt (str): Message to display to user
        input_type: Expected data type (float or int)
        min_val: Minimum acceptable value
        max_val: Maximum acceptable value
    
    Returns:
        Validated user input
    """
    while True:
        try:
            user_input = input_type(input(prompt))
            if min_val <= user_input <= max_val:
                return user_input
            else:
                print(f"Please enter a value between {min_val} and {max_val}.")
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")

def get_height_unit():
    """
    Get and validate height unit from user
    
    Returns:
        str: Valid height unit ('m', 'cm', 'ft')
    """
    while True:
        print("\nSelect height unit:")
        print("1. Meters (m)")
        print("2. Centimeters (cm)")
        print("3. Feet (ft)")
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            return 'm'
        elif choice == '2':
            return 'cm'
        elif choice == '3':
            return 'ft'
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def get_weight_unit():
    """
    Get and validate weight unit from user
    
    Returns:
        str: Valid weight unit ('kg', 'lb')
    """
    while True:
        print("\nSelect weight unit:")
        print("1. Kilograms (kg)")
        print("2. Pounds (lb)")
        choice = input("Enter your choice (1/2): ").strip()
        
        if choice == '1':
            return 'kg'
        elif choice == '2':
            return 'lb'
        else:
            print("Invalid choice. Please enter 1 or 2.")

def convert_weight_to_kg(weight, weight_unit):
    """
    Convert weight to kilograms
    
    Args:
        weight (float): Weight value
        weight_unit (str): Unit of weight ('kg', 'lb')
    
    Returns:
        float: Weight in kilograms
    """
    if weight_unit == 'lb':
        return weight * 0.453592  # 1 lb = 0.453592 kg
    else:  # kg
        return weight

def get_height_range(height_unit):
    """
    Get appropriate height range based on unit
    
    Args:
        height_unit (str): Unit of height
    
    Returns:
        tuple: (min_val, max_val)
    """
    if height_unit == 'cm':
        return (50, 300)  # 50cm to 300cm
    elif height_unit == 'ft':
        return (1.0, 8.0)  # 1ft to 8ft
    else:  # meters
        return (0.5, 2.5)  # 0.5m to 2.5m

def get_weight_range(weight_unit):
    """
    Get appropriate weight range based on unit
    
    Args:
        weight_unit (str): Unit of weight
    
    Returns:
        tuple: (min_val, max_val)
    """
    if weight_unit == 'lb':
        return (2.2, 660)  # 2.2lb to 660lb
    else:  # kg
        return (1, 300)  # 1kg to 300kg

def display_bmi_table():
    """
    Display BMI classification table for reference
    """
    print("\nBMI Classification Table:")
    print("+" + "-" * 40 + "+")
    print("| Category        | BMI Range         |")
    print("+" + "-" * 40 + "+")
    print("| Underweight     | BMI < 18.5        |")
    print("| Normal weight   | 18.5 ≤ BMI < 25   |")
    print("| Overweight      | 25 ≤ BMI < 30     |")
    print("| Obese           | BMI ≥ 30          |")
    print("+" + "-" * 40 + "+")

def get_user_choice():
    """
    Get user choice for continuing or exiting
    
    Returns:
        bool: True if user wants to continue, False otherwise
    """
    while True:
        choice = input("\nWould you like to calculate another BMI? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")

def main():
    """
    Main function to run the CLI BMI calculator
    """
    print("=" * 60)
    print("          ADVANCED BMI CALCULATOR (Command Line)")
    print("=" * 60)
    print("Welcome! This calculator supports multiple units for height and weight.")
    
    while True:
        try:
            print("\n" + "=" * 40)
            print("          ENTER YOUR DETAILS")
            print("=" * 40)
            
            # Get weight unit and value
            weight_unit = get_weight_unit()
            weight_min, weight_max = get_weight_range(weight_unit)
            weight_prompt = f"Enter your weight in {weight_unit}: "
            weight = get_valid_input(weight_prompt, float, weight_min, weight_max)
            
            # Get height unit and value
            height_unit = get_height_unit()
            height_min, height_max = get_height_range(height_unit)
            height_prompt = f"Enter your height in {height_unit}: "
            height = get_valid_input(height_prompt, float, height_min, height_max)
            
            # Convert everything to metric system
            weight_kg = convert_weight_to_kg(weight, weight_unit)
            
            # Calculate BMI
            bmi = calculate_bmi(weight_kg, height, height_unit)
            category = classify_bmi(bmi)
            
            # Display results
            print("\n" + "=" * 50)
            print("           BMI RESULTS")
            print("=" * 50)
            print(f"📊 Weight: {weight:.2f} {weight_unit}")
            print(f"📏 Height: {height:.2f} {height_unit}")
            print(f"🔢 BMI: {bmi:.2f}")
            print(f"🏷️  Category: {category}")
            print("=" * 50)
            
            # Display additional information based on category
            if category == "Underweight":
                print("\n💡 Recommendation: Consider consulting a healthcare provider for nutritional advice.")
            elif category == "Normal weight":
                print("\n✅ Great! Maintain your healthy lifestyle.")
            elif category == "Overweight":
                print("\n⚠️  Recommendation: Consider incorporating more physical activity and balanced diet.")
            else:
                print("\n🚨 Recommendation: Please consult a healthcare provider for guidance.")
            
            # Display BMI table
            display_bmi_table()
            
            # Ask if user wants to continue
            if not get_user_choice():
                print("\n" + "=" * 60)
                print("Thank you for using the Advanced BMI Calculator!")
                print("Stay healthy! 👋")
                print("=" * 60)
                break
                
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user. Goodbye! 👋")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()