import random  # Import the random module to generate random symbol outcomes

# Global game configuration constants
MAX_LINES = 3  # Maximum number of lines a player can bet on (horizontal rows)
MAX_BET = 1000  # Maximum bet allowed per single line in dollars
MIN_BET = 1  # Minimum bet allowed per single line in dollars

ROWS = 3  # Number of rows in the slot machine grid
COLS = 3  # Number of columns in the slot machine grid

# Distribution of symbols in the slot machine reel (rarity)
symbol_count = {
    "A": 2,  # Symbol 'A' is rarest (appears 2 times in the pool)
    "B": 4,  # Symbol 'B' appears 4 times in the pool
    "C": 6,  # Symbol 'C' appears 6 times in the pool
    "D": 8   # Symbol 'D' is most common (appears 8 times in the pool)
}

# Multiplier payout value for each symbol when a winning line is hit
symbol_value = {
    "A": 5,  # 3 of 'A' pays 5x the bet on that line
    "B": 4,  # 3 of 'B' pays 4x the bet on that line
    "C": 3,  # 3 of 'C' pays 3x the bet on that line
    "D": 2   # 3 of 'D' pays 2x the bet on that line
}


def check_winnings(columns, lines, bet, values):
    """Checks each bet line to determine if all symbols match and calculates total winnings."""
    winnings = 0  # Initialize accumulator for total payout
    winnings_lines = []  # List to track the 1-based index of every winning line
    
    # Iterate through each horizontal line the user chose to bet on
    for line in range(lines):
        symbol = columns[0][line]  # Get the symbol from the first column on the current line
        
        # Check if the symbol matches across all columns in this row
        for column in columns:
            symbol_to_check = column[line]  # Symbol in the current column on this line
            if symbol != symbol_to_check:  # If any symbol doesn't match the first one
                break  # Not a winning line, stop checking further columns
        else:
            # Executes only if the loop completed without breaking (all symbols matched)
            winnings += values[symbol] * bet  # Add payout: symbol multiplier times line bet
            winnings_lines.append(line + 1)  # Record winning line number (1-indexed for display)

    return winnings, winnings_lines  # Return total winnings and list of winning line numbers


def get_slot_machine_spin(rows, cols, symbols):
    """Generates a random spin grid representing columns and rows of symbols."""
    all_symbols = []  # Flat list holding the complete pool of symbols
    
    # Populate all_symbols list based on frequency counts defined in symbols dictionary
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):  # Add each symbol symbol_count times
            all_symbols.append(symbol)

    columns = []  # Outer list representing all vertical columns in the slot machine
    
    # Generate each column independently
    for _ in range(cols):
        column = []  # List to store symbols for the current column
        current_symbols = all_symbols[:]  # Make a fresh copy of the symbol pool for this column
        
        # Pick random symbols for each row in this column
        for _ in range(rows):
            value = random.choice(current_symbols)  # Randomly pick a symbol from available pool
            current_symbols.remove(value)  # Remove chosen symbol so it can't be chosen again in this column
            column.append(value)  # Append symbol to current column

        columns.append(column)  # Add completed column to list of columns

    return columns  # Return 2D grid of columns


def print_slot_machine(columns):
    """Transposes columns into horizontal rows and prints the slot machine grid."""
    # Loop through each row index (0 to rows - 1)
    for row in range(len(columns[0])):
        # Loop through each column to print the symbol at the current row
        for i, column in enumerate(columns):
            if i != len(columns) - 1:  # If not the last column
                print(column[row], end=" | ")  # Print symbol followed by pipe separator
            else:
                print(column[row], end="")  # Print symbol without trailing pipe

        print()  # Print newline after completing each row


def deposit():
    """Prompts the user to enter a valid positive deposit amount."""
    while True:  # Loop until a valid numeric deposit is entered
        amount = input(" What would you like to Deposit? $")  # Prompt user for deposit amount
        if amount.isdigit():  # Verify input contains only digits
            amount = int(amount)  # Convert string input to integer
            if amount > 0:  # Ensure deposit is greater than zero
                break  # Input is valid, exit the loop
            else:
                print("Amount must be greater than 0.")  # Reject zero or negative values
        else:
            print("Please enter a number.")  # Reject non-numeric input

    return amount  # Return the validated deposit amount


def get_number_of_lines():
    """Prompts the user to enter the number of lines to bet on (1 to MAX_LINES)."""
    while True:  # Loop until a valid line count within range is entered
        lines = input("Enter the number of lines to bet on (1- " + str(MAX_LINES) + ")? ")  # Prompt for lines
        if lines.isdigit():  # Verify input is numeric
            lines = int(lines)  # Convert input string to integer
            if 1 <= lines <= MAX_LINES:  # Ensure lines chosen is between 1 and MAX_LINES
                break  # Valid number of lines, exit loop
            else:
                print("Enter valid no. of lines. ")  # Notify user if line number is out of bounds
        else:
            print("Please enter a  number.")  # Reject non-numeric input

    return lines  # Return validated line count


def get_bet():
    """Prompts the user to enter a valid bet amount per line."""
    while True:  # Loop until a valid bet within limits is entered
        amount = input(" What would you like to Bet on each line? $")  # Prompt for bet per line
        if amount.isdigit():  # Verify input is numeric
            amount = int(amount)  # Convert input string to integer
            if MIN_BET <= amount <= MAX_BET:  # Ensure bet is within allowable MIN_BET and MAX_BET
                break  # Valid bet, exit loop
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")  # Notify out-of-range bet
        else:
            print("Please enter a  number.")  # Reject non-numeric input

    return amount  # Return validated bet per line


def spin(balance):
    """Executes a single spin round: gets lines and bet, spins machine, checks winnings, and updates balance."""
    # Validate that the player can afford at least the minimum bet on the chosen number of lines
    while True:
        lines = get_number_of_lines()  # Get desired number of lines from user
        if lines * MIN_BET > balance:  # Check if player's balance can cover minimum bet for selected lines
            print(f"You cannot bet on {lines} lines with a ${balance} balance. (Minimum bet per line is ${MIN_BET})")
        else:
            break  # Balance is sufficient for chosen lines

    # Validate that player has enough balance for the total bet
    while True:
        bet = get_bet()  # Get bet per line from user
        total_bet = bet * lines  # Calculate total bet (bet per line * number of lines)

        if total_bet > balance:  # Check if total bet exceeds available balance
            print(f"you do not have enough to bet that amount, your current balance is: ${balance}")
        else:
            break  # Total bet is affordable, proceed with spin

    # Print confirmation of the current wager
    print(f"you are betting ${bet} on {lines} lines. Total bet is: ${total_bet}  ")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)  # Generate random 3x3 slot grid
    print_slot_machine(slots)  # Display slot machine grid to the user
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)  # Calculate payout
    print(f"You Won ${winnings}.")  # Display total winnings earned
    print("You Won on lines:", *winning_lines)  # Display which line numbers won

    return winnings - total_bet  # Return net round profit or loss to add/subtract from balance


def main():
    """Main game loop managing player balance, rounds, re-deposits, and game exit."""
    balance = deposit()  # Initialize player balance with their first deposit
    
    # Main game session loop
    while True:
        print(f"Current balance is ${balance}")  # Display current balance before each round
        
        # If balance falls below minimum allowable bet, offer re-deposit option
        if balance < MIN_BET:
            print("You do not have enough money to place a bet.")
            top_up = input("Would you like to deposit more? (y/n): ").lower()  # Prompt for re-deposit
            if top_up == "y":  # User wants to add funds
                balance += deposit()  # Add new deposit to balance
                continue  # Resume game with updated balance
            else:
                break  # User chooses not to deposit more, end game

        answer = input("Press enter to play (q to quit).")  # Prompt user to spin or quit
        if answer == "q":  # User chose to exit game
            break  # Exit game loop
            
        balance += spin(balance)  # Play round and update balance with net outcome

    print(f"You Left with ${balance}")  # Final farewell message showing remaining balance


main()  # Call entry point to start the program
