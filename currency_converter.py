import requests

API_KEY = "nIpLYcbpSjAUzOixZ7cAeZZQkMISALp7"
BASE_URL = "https://api.apilayer.com/fixer/convert"

def get_user_input(prompt, validation_fn=None):
    """Continuously prompt the user until valid input is provided."""
    while True:
        user_input = input(prompt)
        if validation_fn:
            is_valid, error_msg = validation_fn(user_input)
            if is_valid:
                return user_input
            print(error_msg)
        else:
            return user_input

def validate_currency_input(currency):
    """Validate that currency input is alphabetic and has a valid length."""
    if not currency.isalpha() or len(currency) != 3:
        return False, "Currency must be a 3-letter code."
    return True, ""

def validate_amount_input(amount_str):
    """Validate that amount input is a positive number."""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Amount must be greater than 0."
        return True, ""
    except ValueError:
        return False, "The amount must be a numeric value."

def get_conversion_rate(from_currency, to_currency, amount):
    """Make the API request to fetch the conversion rate and return the result."""
    url = f"{BASE_URL}?to={to_currency}&from={from_currency}&amount={amount}"
    headers = {"apikey": API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data.get("success", False):
            return data.get("result", None)
        else:
            raise ValueError(f"API Error: {data.get('error', {}).get('info', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Network error occurred: {e}")
    except ValueError as ve:
        raise SystemExit(ve)

def main():
    """Main program execution."""
    # Get validated inputs
    init_currency = get_user_input("Enter an initial currency: ", validate_currency_input).upper()
    target_currency = get_user_input("Enter a target currency: ", validate_currency_input).upper()
    amount = get_user_input("Enter the amount: ", validate_amount_input)

    # Fetch the conversion rate
    try:
        conversion_result = get_conversion_rate(init_currency, target_currency, amount)
        print(f"{amount} {init_currency} is equal to {conversion_result} {target_currency}.")
    except SystemExit as e:
        print(e)

if __name__ == "__main__":
    main()
