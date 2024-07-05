import random

#constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3

symbol_count = {    #symbols per column
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {    #multiplier for winning
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):                   #[0, lines); loop through the number of lines, 1 - first row, 2 - top 2 rows, 3 - top 3 rows, etc.
        symbol = columns[0][line]               #gets the symbol at the start of row line (eg. if line == 2, then symbol is the first symbol of row 2)
        for column in columns:                  #iterates through each column of row line to check if column[line] == symbol (eg. if line == 2, then checks if each column of row 2 has the same symbol as the first symbol of row 2)
            symbol_to_check = column[line]
            if symbol != symbol_to_check:       #if mismatch, then break out of current row
                break
        else:                                   #runs when no break occurs (aka they win)
            winnings += values[symbol] * bet    #winnings are equal to bet per line multiplied by the corresponding multiplier
            winning_lines.append(line + 1)
    
    return winnings, winning_lines

#function to generate slot machine spin
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():    #for each symbol and frequency in symbols dictionary, add the symbol to list for the number of frequency
        for _ in range(symbol_count):               # _ is an anonymous variable
            all_symbols.append(symbol)
    
    columns = []
    for _ in range(cols):                           #for each column, loop through the rows
        column = []
        current_symbols = all_symbols[:]            #creates a copy of the all_symbols list
        for _ in range(rows):                       #for each row in column, pick a random value from the current_symbols list and add that value to the column, removing value from current_symbols to choose from for the column
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)
    
    return columns

#function to transpose the grid to show columns vertically and print it
def print_slot_machine(columns):
    for row in range(len(columns[0])):          #loop through every row
        for i, column in enumerate(columns):    #loop through every column and print the element at the row; enumerate gives index as well as column
            if i != len(columns) - 1:           #adds " | " as long as the column being printed is not the last column
                print(column[row], end = " | ")
            else:
                print(column[row])

#function to get deposit from user
def deposit():
    while True:
        amount = input("How much would you like to deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    
    return amount

#function to get number of lines user would like to bet on
def get_number_of_lines():
    while True:
        lines = input("Enter the number of lines to bet on (1 - " + str(MAX_LINES) + "): ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter a valid number of lines.")
        else:
            print("Please enter a number.")
    
    return lines

#function to get the amount of money the user would like to bet
def get_bet():
    while True:
        bet = input("How much would you like to bet on each line? $")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f"Bet must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a number.")
    
    return bet

#function containing game functionality per spin
def game(balance):
    lines = get_number_of_lines()
    print("Your balance is: $" + str(balance), "\nNumber of lines:", lines)

    while True:             #if total bet exceeds balance, prompt user to enter a valid bet amount
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough to bet that amount.\nCurrent balance: ${balance}")
        else:
            break

    print(f"You are betting ${bet} on {lines} lines. Total bet is ${total_bet}.")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count) #slots = columns
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You won: ${winnings}")
    print(f"You won on lines:", *winning_lines)     #splat operator to unpack list
    return winnings - total_bet

#main method to run the game
def main():
    balance = deposit()
    while balance > 0:
        print(f"Current balance is: ${balance}")
        spin = input("Press enter to play (q to quit) ")
        if spin == "q":
            break
        balance += game(balance)
    
    print(f"You left with: ${balance}")

#calling the main method to run the game
main()