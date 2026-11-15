# Building a Casino Slot Machine in Python: Architecture, Code Deep Dive, and In-Depth Complexity Analysis

*A complete, production-grade guide covering game mechanics, probability calculations, clean Pythonic architecture, line-by-line code explanation, and rigorous software complexity analysis (Cyclomatic, Cognitive, Time, and Space).*

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [The Basic Idea](#2-the-basic-idea)
3. [What We Are Trying to Demonstrate](#3-what-we-are-trying-to-demonstrate)
4. [Python-Specific Features & Data Structures Used](#4-python-specific-features--data-structures-used)
5. [The Logic Behind Calculations & Odds](#5-the-logic-behind-calculations--odds)
6. [Program Flowchart](#6-program-flowchart)
7. [System Architecture](#7-system-architecture)
8. [Step-by-Step Code Deep Dive (9 Snippets)](#8-step-by-step-code-deep-dive-9-snippets)
   - [Snippet 1: Imports, Constants & Symbol Tables](#snippet-1-imports-constants--symbol-tables)
   - [Snippet 2: Evaluating Paylines (`check_winnings`)](#snippet-2-evaluating-paylines-check_winnings)
   - [Snippet 3: Reel Simulation Engine (`get_slot_machine_spin`)](#snippet-3-reel-simulation-engine-get_slot_machine_spin)
   - [Snippet 4: 2D Matrix Rendering (`print_slot_machine`)](#snippet-4-2d-matrix-rendering-print_slot_machine)
   - [Snippet 5: User Funding (`deposit`)](#snippet-5-user-funding-deposit)
   - [Snippet 6: Bounded Input Sanitation (`get_number_of_lines`)](#snippet-6-bounded-input-sanitation-get_number_of_lines)
   - [Snippet 7: Wager Sanitation (`get_bet`)](#snippet-7-wager-sanitation-get_bet)
   - [Snippet 8: Core Round Orchestrator (`spin`)](#snippet-8-core-round-orchestrator-spin)
   - [Snippet 9: Session State Controller (`main`)](#snippet-9-session-state-controller-main)
9. [Comprehensive Complexity Analysis](#9-comprehensive-complexity-analysis)
   - [Complexity Summary Table](#complexity-summary-table)
   - [Cyclomatic Complexity (McCabe)](#cyclomatic-complexity-mccabe)
   - [Cognitive Complexity (SonarQube)](#cognitive-complexity-sonarqube)
   - [Time Complexity (Algorithmic Runtime)](#time-complexity-algorithmic-runtime)
   - [Space Complexity (Memory Footprint)](#space-complexity-memory-footprint)
10. [Key Takeaways & Conclusion](#10-key-takeaways--conclusion)

---

## 1. Introduction

Building text-based arcade games in Python is one of the most effective, battle-tested methods for bridging the gap between beginner syntax and intermediate software engineering. 

A casino slot machine appears deceptively straightforward on the surface: you insert money, pull a lever, reels spin, and you either win a multiplier or lose your stake. However, translating this physical experience into clean, resilient, and maintainable software requires solving a series of classic computer science challenges:
- **Matrix Manipulation**: Handling 2D grids (columns vs. rows) and transposing internal state for visual display.
- **Probability Modeling**: Simulating non-uniform random distributions using weighted frequency tables.
- **Defensive State Management**: Preventing infinite input loops, bankruptcy deadlocks, and invalid state transitions.
- **Algorithmic Elegance**: Using advanced Python idioms (like `for...else` loops, slicing copies, and tuple unpacking) rather than bloated spaghetti code.

In this article, we break down an entire terminal-based Python Slot Machine from first principles, explore its architecture and mathematical foundation, explain every line across 9 modular snippets, and finish with an industry-grade software complexity audit (evaluating Cyclomatic Complexity, Cognitive Complexity, Time Complexity, and Space Complexity).

---

## 2. The Basic Idea

The core concept behind our slot machine is a standard **3-Row by 3-Column (3x3) Video Slot Wheel**.

### Game Loop Mechanics:
1. **The Deposit Phase**: The player starts by depositing a positive cash amount into their game balance.
2. **The Session Phase**:
   - The user is shown their current balance.
   - If their balance is too low to place even a single minimum bet, the engine offers an immediate top-up deposit prompt instead of locking up.
   - The user presses `Enter` to spin the wheel or types `q` to cash out and exit.
3. **The Wager Phase**:
   - The player selects how many horizontal paylines they want to bet on (from 1 up to 3).
   - The player chooses their wager per line (between $1 and $1000).
   - The system checks that `Lines * Bet <= Balance` before initiating the spin.
4. **The Spin & Simulation Phase**:
   - The engine generates 3 independent vertical columns (reels).
   - Each column is populated by drawing symbols at random without replacement from a weighted probability pool.
5. **The Evaluation & Payout Phase**:
   - The engine renders the 3x3 grid cleanly to the terminal separated by `|` pipes.
   - Each active payline is checked: if all 3 symbols on that horizontal line are identical, the player wins the corresponding multiplier for that symbol multiplied by their line bet.
   - Winnings are added, the total wager is deducted, and the net balance is updated.

---

## 3. What We Are Trying to Demonstrate

Beyond being a fun terminal game, this project is crafted as a pedagogical blueprint demonstrating clean coding practices:

1. **Separation of Concerns**: Pure functions handle calculations and matrix generation, dedicated validation functions handle standard I/O, and orchestration functions manage game state.
2. **Defensive Programming**: User input is inherently untrusted. The program validates string-to-integer conversions (`.isdigit()`), numerical boundary constraints, and fiscal solvency checks before executing any game step.
3. **Edge-Case Resilience**: Handling the "Bankruptcy Trap." In naive slot machine tutorials, a user whose balance drops to $0 gets stuck in an infinite prompt loop because the minimum bet is $1. We demonstrate how to catch this edge case gracefully with proactive boundary checks.
4. **Idiomatic Python**: Avoiding anti-patterns by leaning into Python’s built-in language capabilities:
   - Eliminating redundant boolean tracking flags with `for...else`.
   - Using shallow slicing (`[:]`) to prevent unintended mutation of global symbol templates.
   - Unpacking iterables cleanly with the splat operator (`*`).

---

## 4. Python-Specific Features & Data Structures Used

This project makes deliberate use of Python's primary native data structures and idioms:

### 1. Dictionaries (`dict`)
Used for $\mathcal{O}(1)$ key-value mappings:
- `symbol_count`: Defines the frequency distribution (weighting) of each symbol across the reel.
- `symbol_value`: Defines the multiplier payout table for winning combinations.

### 2. Lists (`list`) and 2D Matrices
- Dynamic 1D Lists: `all_symbols` acts as a flat pool of available symbols.
- 2D Nested Lists: `columns` is structured as a list of lists (`columns[col][row]`), modeling the physical mechanics of slot reels.
- List Slicing (`[:]`): Creates independent shallow copies of symbol pools per column, ensuring selections in one reel do not deplete symbols in subsequent reels.

### 3. Tuples (`tuple`)
- Functions like `check_winnings` return `(winnings, winnings_lines)`. Python implicitly packages multiple return values as immutable tuples, allowing clean multi-variable unpacking at the call site.

### 4. Control Flow Constructs
- `while True` Loops: Used for robust input-validation guards that repeat until valid data is supplied.
- The `for...else` Clause: In Python, a `for` loop can have an `else` block. The `else` block executes **only if the loop completes normally without hitting a `break`**. This eliminates the need for clumsy flags like `is_winner = True`.

### 5. String Manipulation & Terminal Formatting
- `.isdigit()`: Sanitizes string inputs to prevent `ValueError` exceptions prior to type casting.
- `print(..., end=" | ")`: Overrides default newline termination to format multi-column grid rows.
- Splat Operator (`*`): Unpacks list elements into positional function arguments (`print("You Won on lines:", *winning_lines)`).

---

## 5. The Logic Behind Calculations & Odds

Understanding a slot machine requires looking at the mathematics of probability and expected return.

### The Symbol Pool & Rarity
The reel uses 4 distinct symbols with the following distribution:

| Symbol | Count in Pool ($S_i$) | Probability per Draw ($P$) | Payout Multiplier ($M_i$) | Relative Rarity |
| :---: | :---: | :---: | :---: | :---: |
| **A** | 2 | $2/20 = 10.0\%$ | **5x** | Very Rare (Jackpot) |
| **B** | 4 | $4/20 = 20.0\%$ | **4x** | Rare |
| **C** | 6 | $6/20 = 30.0\%$ | **3x** | Medium |
| **D** | 8 | $8/20 = 40.0\%$ | **2x** | Common |
| **Total** | **20** | **100%** | — | — |

### Winning Line Probability
Each column independently draws 3 symbols from its own copy of the 20-symbol pool.
For a horizontal line across all 3 columns to match symbol $X$:
$$	ext{P}(	ext{Line } L 	ext{ is all } X) = 	ext{P}(X 	ext{ in col 1}) 	imes 	ext{P}(X 	ext{ in col 2}) 	imes 	ext{P}(X 	ext{ in col 3})$$

Since the first symbol drawn in column $c$ has probability $rac{	ext{count}(X)}{20}$:
- **3 of A**: $(0.10)^3 = 0.001 = 0.1\%$ chance (1 in 1,000 spins per line).
- **3 of B**: $(0.20)^3 = 0.008 = 0.8\%$ chance (1 in 125 spins per line).
- **3 of C**: $(0.30)^3 = 0.027 = 2.7\%$ chance (approx 1 in 37 spins per line).
- **3 of D**: $(0.40)^3 = 0.064 = 6.4\%$ chance (approx 1 in 15.6 spins per line).

Total probability of any single line hitting a win:
$$P(	ext{Win on Line } L) = 0.001 + 0.008 + 0.027 + 0.064 = 0.100 = 10.0\%$$

### Financial Formulas
1. **Total Wager**:
   $$	ext{Total Bet} = 	ext{bet per line} 	imes 	ext{number of lines}$$
2. **Line Payout**:
   $$	ext{Line Winnings} = 	ext{symbol\_value}[X] 	imes 	ext{bet per line}$$
3. **Round Net Delta**:
   $$\Delta 	ext{Balance} = \sum 	ext{Line Winnings} - 	ext{Total Bet}$$

---

## 6. Program Flowchart

Below is the complete state machine representing the lifecycle of an application session:

```mermaid
flowchart TD
    Start([Application Start]) --> Deposit[Player Deposits Funds]
    Deposit --> CheckBal{Balance >= MIN_BET?}
    
    CheckBal -- No --> ReDepositPrompt{Deposit More?}
    ReDepositPrompt -- Yes --> TopUp[Call deposit and Add to Balance]
    TopUp --> CheckBal
    ReDepositPrompt -- No --> CashOut[Display Final Balance & Exit]
    
    CheckBal -- Yes --> DisplayBal[Display Current Balance]
    DisplayBal --> PlayPrompt{Press Enter to Play or 'q' to Quit?}
    PlayPrompt -- 'q' --> CashOut
    PlayPrompt -- Enter --> ChooseLines[Prompt Number of Lines 1-3]
    
    ChooseLines --> ValidateLines{Lines * MIN_BET <= Balance?}
    ValidateLines -- No --> LinesError[Show Error: Insufficient Balance] --> ChooseLines
    ValidateLines -- Yes --> ChooseBet[Prompt Bet Per Line]
    
    ChooseBet --> ValidateBet{Bet * Lines <= Balance?}
    ValidateBet -- No --> BetError[Show Error: Bet Exceeds Balance] --> ChooseBet
    ValidateBet -- Yes --> DeductBet[Compute Total Bet]
    
    DeductBet --> SpinEngine[Generate 3x3 Random Symbol Grid]
    SpinEngine --> RenderGrid[Print Grid to Terminal With Pipes]
    RenderGrid --> CheckWins[Evaluate Matching Symbols on Active Lines]
    CheckWins --> CalculatePayout[Calculate Total Winnings & Display Lines]
    CalculatePayout --> UpdateBalance[Balance = Balance + Winnings - Total Bet]
    UpdateBalance --> CheckBal
```

---

## 7. System Architecture

The application is structured into four decoupled logical layers:

```
+-----------------------------------------------------------------------+
|                         PRESENTATION LAYER                            |
|             print_slot_machine()  |  Terminal I/O Prompts             |
+-----------------------------------------------------------------------+
                                   ▲
                                   │ (Renders Grid & Outputs Text)
+-----------------------------------------------------------------------+
|                         ORCHESTRATION LAYER                           |
|        main() [Session State]  <--->  spin() [Round Controller]       |
+-----------------------------------------------------------------------+
        │ (Coordinates)                         │ (Delegates)
        ▼                                       ▼
+-----------------------------------+   +-------------------------------+
|         INPUT & VALIDATION        |   |       CORE GAME ENGINE        |
|  - deposit()                      |   |  - get_slot_machine_spin()    |
|  - get_number_of_lines()          |   |  - check_winnings()           |
|  - get_bet()                      |   |  - random.choice() generation |
+-----------------------------------+   +-------------------------------+
                                   ▲
                                   │ (Reads Configuration)
+-----------------------------------------------------------------------+
|                         CONFIGURATION LAYER                           |
|      Constants (ROWS, COLS, MAX_LINES, MIN_BET, MAX_BET)              |
|      Lookup Tables (symbol_count, symbol_value)                       |
+-----------------------------------------------------------------------+
```

### Layer Responsibilities:
1. **Configuration Layer**: Establishes global constraints and mathematical models.
2. **Input & Validation Layer**: Shields the system from invalid states, ensuring only sanitized, verified data reaches the logic engine.
3. **Core Game Engine**: Pure functions containing business logic without UI side effects; easy to isolate and unit test.
4. **Orchestration Layer**: Manages the outer game loop, round lifecycles, and balance state mutations.

---

## 8. Step-by-Step Code Deep Dive (9 Snippets)

Let us examine every snippet of the project line by line.

---

### Snippet 1: Imports, Constants & Symbol Tables

```python
import random

MAX_LINES = 3
MAX_BET = 1000
MIN_BET = 1 

ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8 
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}
```

#### Line-by-Line Explanation:
- `import random`: Imports Python's built-in pseudorandom number generator module, utilized later for stochastic reel selection.
- `MAX_LINES = 3`: Constant fixing the maximum number of horizontal betting lines to 3 (corresponding to the 3 rows of the matrix).
- `MAX_BET = 1000`: Upper ceiling threshold per single line wager ($1,000) to maintain input bounds.
- `MIN_BET = 1`: Lower floor threshold per single line wager ($1).
- `ROWS = 3`: Dimension constant setting vertical grid height to 3 rows.
- `COLS = 3`: Dimension constant setting horizontal grid width to 3 columns.
- `symbol_count = { ... }`: A dictionary defining symbol frequencies in the master pool. Rare symbols have lower values (`"A": 2`), while common symbols have higher counts (`"D": 8`). Total symbols in the pool = 20.
- `symbol_value = { ... }`: A lookup table defining the payout multiplier for each symbol. Symbol `A` pays 5x the line bet, while symbol `D` pays 2x.

---

### Snippet 2: Evaluating Paylines (`check_winnings`)

```python
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winnings_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)
    
    return winnings, winnings_lines
```

#### Line-by-Line Explanation:
- `def check_winnings(columns, lines, bet, values):`: Function signature accepting the generated 2D grid (`columns`), the number of lines bet on (`lines`), the bet per line (`bet`), and the payout dictionary (`values`).
- `winnings = 0`: Accumulator variable to tally the total payout earned across all winning lines.
- `winnings_lines = []`: Dynamic list that records the 1-indexed numbers of lines that successfully hit 3-of-a-kind.
- `for line in range(lines):`: Iterates through each active line (e.g., `0`, `1`, or `2`). Line `0` is the top row, `1` is middle, `2` is bottom.
- `symbol = columns[0][line]`: Inspects the symbol located in the first column (`column index 0`) at the current horizontal row (`line`). This acts as the benchmark symbol that all subsequent columns must match.
- `for column in columns:`: Inner loop traversing each vertical column list in the grid.
- `symbol_to_check = column[line]`: Extracts the symbol in the current column at the exact same horizontal row index.
- `if symbol != symbol_to_check:`: Compares the current symbol against the benchmark. If a mismatch is detected, the line cannot be a win.
- `break`: Aborts the inner column loop immediately upon the first mismatch to save CPU cycles.
- `else:`: **The Python `for...else` construct!** This block executes if and only if the inner `for column in columns` loop completed without encountering a `break` (meaning all columns had identical symbols on this line).
- `winnings += values[symbol] * bet`: Multiplies the winning symbol's multiplier by the user's line bet and adds it to total winnings.
- `winnings_lines.append(line + 1)`: Appends the human-friendly (1-based) line number to our winners list.
- `return winnings, winnings_lines`: Packages both results into a tuple and returns them to the caller.

---

### Snippet 3: Reel Simulation Engine (`get_slot_machine_spin`)

```python
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)

    return columns
```

#### Line-by-Line Explanation:
- `def get_slot_machine_spin(rows, cols, symbols):`: Function signature accepting grid dimensions and the symbol count configuration.
- `all_symbols = []`: Initializes an empty list to assemble the complete weighted symbol pool.
- `for symbol, symbol_count in symbols.items():`: Iterates through each key-value pair in `symbols` (e.g., `"A": 2`).
- `for _ in range(symbol_count):`: Loops as many times as the frequency count specified for that symbol.
- `all_symbols.append(symbol)`: Appends the symbol to the pool. When finished, `all_symbols` contains 20 elements (`['A', 'A', 'B', 'B', 'B', 'B', ...]`).
- `columns = []`: Initializes the master container list for the 2D grid.
- `for _ in range(cols):`: Loops once for each column to be generated (3 iterations).
- `column = []`: Initializes a list to hold the rows for the current column.
- `current_symbols = all_symbols[:]`: **Crucial Idiom**: Performs a shallow slice copy of the master symbol pool. This ensures that symbol removals in this column do not mutate `all_symbols` or affect other columns.
- `for _ in range(rows):`: Loops 3 times to pick symbols for the 3 vertical rows of this column.
- `value = random.choice(current_symbols)`: Selects a random symbol uniformly from the available pool.
- `current_symbols.remove(value)`: Removes the chosen symbol from the local pool so it cannot be selected again in the same column (sampling without replacement across rows).
- `column.append(value)`: Adds the selected symbol to the current column list.
- `columns.append(column)`: Appends the fully assembled column list to the outer `columns` grid.
- `return columns`: Returns the completed 2D matrix (represented as a list of columns).

---

### Snippet 4: 2D Matrix Rendering (`print_slot_machine`)

```python
def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")

        print()
```

#### Line-by-Line Explanation:
- `def print_slot_machine(columns):`: Function receiving the column-major 2D matrix.
- `for row in range(len(columns[0])):`: Loops through horizontal row indices (0, 1, 2). Because our data structure is column-major (`columns[col][row]`), we must iterate rows on the outside to print horizontally across the screen.
- `for i, column in enumerate(columns):`: Iterates through each column while tracking the index `i` (0, 1, or 2).
- `if i != len(columns) - 1:`: Checks if the current column is NOT the final column.
- `print(column[row], end=" | ")`: Prints the symbol at `column[row]` followed by a pipe separator without inserting a newline (`end=" | "`).
- `else:`: Executes when printing the final column in the row.
- `print(column[row], end="")`: Prints the symbol with no trailing pipe.
- `print()`: Emits an empty print call, outputting a newline character (`
`) to advance the cursor to the next line of the terminal.

---

### Snippet 5: User Funding (`deposit`)

```python
def deposit():
    while True:
        amount = input(" What would you like to Deposit? $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Amount must be greater than 0.")
        else:
            print("Please enter a number.")
    
    return amount
```

#### Line-by-Line Explanation:
- `def deposit():`: Function prompting the user to supply funds to their balance.
- `while True:`: Infinite loop ensuring the prompt re-appears until a valid, positive numerical input is supplied.
- `amount = input(" What would you like to Deposit? $")`: Displays the prompt and captures user input as a string.
- `if amount.isdigit():`: Validates that the input string contains purely digits (rejects letters, symbols, decimals, and negative signs).
- `amount = int(amount)`: Safely casts the validated string to a Python integer.
- `if amount > 0:`: Verifies that the deposit is strictly positive ($1 or more).
- `break`: Exits the validation loop when all conditions are satisfied.
- `else:` (inner): Prints an error message if the integer entered was 0.
- `else:` (outer): Prints an error message if non-numeric characters were supplied.
- `return amount`: Returns the sanitized deposit integer to the caller.

---

### Snippet 6: Bounded Input Sanitation (`get_number_of_lines`)

```python
def get_number_of_lines():
    while True:         
        lines = input("Enter the number of lines to bet on (1- " + str(MAX_LINES)+")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("Enter valid no. of lines. ")
        else:
            print("Please enter a  number.")
    
    return lines
```

#### Line-by-Line Explanation:
- `def get_number_of_lines():`: Function signature for acquiring line count.
- `while True:`: Loop guarding against invalid selections.
- `lines = input(...)`: Prompts the user, dynamically concatenating `MAX_LINES` (`3`) into the prompt string.
- `if lines.isdigit():`: Ensures raw input consists only of numeric characters.
- `lines = int(lines)`: Converts input to integer.
- `if 1 <= lines <= MAX_LINES:`: **Chained Comparison**: Checks that the requested lines fall strictly between 1 and 3 inclusive.
- `break`: Exits loop when valid lines are entered.
- `else:` (inner): Informs the user if their integer was outside the 1–3 range.
- `else:` (outer): Informs the user if their entry was not a valid number.
- `return lines`: Returns validated line count integer.

---

### Snippet 7: Wager Sanitation (`get_bet`)

```python
def get_bet():
    while True:
        amount = input(" What would you like to Bet on each line? $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"Amount must be between ${MIN_BET} - ${MAX_BET}.")
        else:
            print("Please enter a  number.")
    
    return amount
```

#### Line-by-Line Explanation:
- `def get_bet():`: Function signature for getting the wager per line.
- `while True:`: Validation guard loop.
- `amount = input(...)`: Captures user wager input.
- `if amount.isdigit():`: Validates that entry is numeric.
- `amount = int(amount)`: Converts input string to integer.
- `if MIN_BET <= amount <= MAX_BET:`: Validates that the wager satisfies both lower bound ($1) and upper bound ($1,000).
- `break`: Exits loop on successful validation.
- `else:` (inner): Emits an f-string message informing the user of the allowed bet bounds.
- `else:` (outer): Rejects non-digit input.
- `return amount`: Returns the validated bet amount per line.

---

### Snippet 8: Core Round Orchestrator (`spin`)

```python
def spin(balance):
    while True:
        lines = get_number_of_lines()
        if lines * MIN_BET > balance:
            print(f"You cannot bet on {lines} lines with a ${balance} balance. (Minimum bet per line is ${MIN_BET})")
        else:
            break
    
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"you do not have enough to bet that amount, your current balance is: ${balance}")    
        else:
            break
            
    print(f"you are betting ${bet} on {lines} lines. Total bet is: ${total_bet}  ")

    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"You Won ${winnings}.")
    print("You Won on lines:", *winning_lines)
    
    return winnings - total_bet
```

#### Line-by-Line Explanation:
- `def spin(balance):`: Function executing one complete spin round, accepting current `balance`.
- `while True:` (lines loop): Validates lines against minimum possible outlay.
- `lines = get_number_of_lines()`: Calls line input prompt.
- `if lines * MIN_BET > balance:`: **Critical Insolvency Guard**: Checks if the player's balance is lower than `lines * MIN_BET` (e.g. balance is $2, but user picks 3 lines where minimum bet is $3). If so, it alerts the user and prompts for lines again, avoiding an unescapable trap!
- `else: break`: Proceeds once a feasible line count is selected.
- `while True:` (bet loop): Validates that the wager fits the player's bankroll.
- `bet = get_bet()`: Calls wager input prompt.
- `total_bet = bet * lines`: Calculates total cost of the round.
- `if total_bet > balance:`: Verifies that the player has sufficient balance to cover the total bet.
- `else: break`: Escapes loop when total bet is affordable.
- `print(f"you are betting ${bet} on {lines} lines...")`: Prints confirmation of the wager.
- `slots = get_slot_machine_spin(...)`: Generates the random 3x3 reel matrix.
- `print_slot_machine(slots)`: Displays the grid visually in the terminal.
- `winnings, winning_lines = check_winnings(...)`: Evaluates lines, returning total payout and winning line indices.
- `print(f"You Won ${winnings}.")`: Informs player of their payout.
- `print("You Won on lines:", *winning_lines)`: **Splat Operator (`*`)**: Unpacks the list of winning line numbers cleanly as comma-free space-separated values.
- `return winnings - total_bet`: Returns the net profit or loss for the round (e.g. won $20 on a $10 bet returns $+10$; won $0 on a $10 bet returns $-10$).

---

### Snippet 9: Session State Controller (`main`)

```python
def main():
    balance = deposit()
    while True:
        print(f"Current balance is ${balance}")
        if balance < MIN_BET:
            print("You do not have enough money to place a bet.")
            top_up = input("Would you like to deposit more? (y/n): ").lower()
            if top_up == "y":
                balance += deposit()
                continue
            else:
                break

        answer = input("Press enter to play (q to quit).")
        if answer == "q":
            break
        balance += spin(balance)

    print(f"You Left with ${balance}")


main()
```

#### Line-by-Line Explanation:
- `def main():`: Main driver function managing player session state.
- `balance = deposit()`: Initializes the player's balance with an initial deposit.
- `while True:`: Outer session loop running round after round until the user exits or runs out of funds.
- `print(f"Current balance is ${balance}")`: Displays current bankroll before prompting to play.
- `if balance < MIN_BET:`: Checks if the balance is too low to place any valid bet ($1).
- `top_up = input(...).lower()`: Proactively offers the player an option to deposit additional funds instead of crashing or looping indefinitely.
- `if top_up == "y":`: If player confirms, calls `deposit()` and adds funds to `balance`.
- `continue`: Skips the remainder of the loop and re-checks balance with fresh funds.
- `else: break`: If player declines, terminates the session gracefully.
- `answer = input("Press enter to play (q to quit).")`: Prompts user to initiate a spin or exit.
- `if answer == "q": break`: Breaks the game loop if `q` was entered.
- `balance += spin(balance)`: Executes the spin and adds the round's net outcome (`winnings - total_bet`) directly to `balance`.
- `print(f"You Left with ${balance}")`: Prints departing balance summary upon game termination.
- `main()`: Python entry point statement executing the `main()` function when the script runs.

---

## 9. Comprehensive Complexity Analysis

As software engineers, writing code that works is only the first half of the equation; proving how well it scales, its structural branching complexity, and its mental maintainability is the second half.

Below is the definitive complexity audit of the application.

### Complexity Summary Table

| Function | Cyclomatic Complexity (McCabe) | Cognitive Complexity (SonarQube) | Time Complexity (Per Call) | Auxiliary Space Complexity |
| :--- | :---: | :---: | :---: | :---: |
| `check_winnings()` | **4** | **7** | $\mathcal{O}(L \cdot C) ightarrow \mathcal{O}(1)$ | $\mathcal{O}(L) ightarrow \mathcal{O}(1)$ |
| `get_slot_machine_spin()` | **5** | **6** | $\mathcal{O}(C \cdot R \cdot S) ightarrow \mathcal{O}(1)$ | $\mathcal{O}(S + R \cdot C) ightarrow \mathcal{O}(1)$ |
| `print_slot_machine()` | **4** | **7** | $\mathcal{O}(R \cdot C) ightarrow \mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| `deposit()` | **4** | **8** | $\mathcal{O}(K) ightarrow \mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| `get_number_of_lines()` | **4** | **8** | $\mathcal{O}(K) ightarrow \mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| `get_bet()` | **4** | **8** | $\mathcal{O}(K) ightarrow \mathcal{O}(1)$ | $\mathcal{O}(1)$ |
| `spin()` | **5** | **8** | $\mathcal{O}(C \cdot R \cdot S) ightarrow \mathcal{O}(1)$ | $\mathcal{O}(S + R \cdot C) ightarrow \mathcal{O}(1)$ |
| `main()` | **5** | **9** | $\mathcal{O}(N)$ rounds | $\mathcal{O}(1)$ |
| **Project Total / Average** | **Total: 35** (Avg: **4.38**) | **Total: 61** (Avg: **7.63**) | **$\mathcal{O}(N)$** across session | **$\mathcal{O}(1)$** Constant Memory |

---

### Cyclomatic Complexity (McCabe)
**Cyclomatic Complexity ($M$ or $CC$)** measures the number of linearly independent execution paths through a program's source code:
$$M = E - N + 2P \quad 	ext{or} \quad M = 1 + 	ext{Decision Points}$$

In Python AST analysis, decision points include `if`, `while`, `for`, boolean operators (`and`, `or`), and exception handlers.

#### Breakdown per Function:
- **`check_winnings` (CC = 4)**:
  - Base complexity: 1
  - Decision points: `for line in range(lines)` (+1), `for column in columns` (+1), `if symbol != symbol_to_check` (+1) $ightarrow 1 + 3 = 4$.
- **`get_slot_machine_spin` (CC = 5)**:
  - Base: 1
  - Decision points: `for symbol, symbol_count` (+1), `for _ in range(symbol_count)` (+1), `for _ in range(cols)` (+1), `for _ in range(rows)` (+1) $ightarrow 1 + 4 = 5$.
- **`print_slot_machine` (CC = 4)**:
  - Base: 1
  - Decision points: `for row` (+1), `for i, column` (+1), `if i != len(columns) - 1` (+1) $ightarrow 1 + 3 = 4$.
- **`deposit`, `get_number_of_lines`, `get_bet` (CC = 4 each)**:
  - Base: 1
  - Decision points: `while True` (+1), `if isdigit()` (+1), boundary check `if` (+1) $ightarrow 1 + 3 = 4$.
- **`spin` (CC = 5)**:
  - Base: 1
  - Decision points: Lines `while True` (+1), lines affordability `if` (+1), bet `while True` (+1), total bet affordability `if` (+1) $ightarrow 1 + 4 = 5$.
- **`main` (CC = 5)**:
  - Base: 1
  - Decision points: Session `while True` (+1), `if balance < MIN_BET` (+1), `if top_up == 'y'` (+1), `if answer == 'q'` (+1) $ightarrow 1 + 4 = 5$.

**Industry Assessment**: In software engineering, functions with Cyclomatic Complexity between **1 and 10** are considered simple, highly maintainable, and easy to unit test. Every function in this project scores $\le 5$, demonstrating exceptional structural discipline.

---

### Cognitive Complexity (SonarQube)
Unlike Cyclomatic Complexity, which simply tallies mathematical branches, **Cognitive Complexity** measures how much mental effort a human developer must expend to understand the control flow. It penalizes nested structures (nesting increments) because human working memory degrades rapidly as indentations deepen.

#### Breakdown per Function:
- **`get_slot_machine_spin` (Score = 6)**:
  - Outer `for` loop (+1, nesting 0).
  - Nested `for` loop (+2, nesting 1).
  - Columns `for` loop (+1, nesting 0).
  - Nested rows `for` loop (+2, nesting 1) $ightarrow 1 + 2 + 1 + 2 = 6$.
- **`check_winnings` (Score = 7)**:
  - Outer line `for` (+1, nesting 0).
  - Inner column `for` (+2, nesting 1).
  - Nested mismatch `if` (+3, nesting 2).
  - The `for...else` clause (+1) $ightarrow 1 + 2 + 3 + 1 = 7$.
- **`print_slot_machine` (Score = 7)**:
  - Outer row `for` (+1, nesting 0).
  - Inner column `for` (+2, nesting 1).
  - Nested separator `if` (+3, nesting 2).
  - `else` branch (+1) $ightarrow 1 + 2 + 3 + 1 = 7$.
- **`deposit`, `get_number_of_lines`, `get_bet` (Score = 8 each)**:
  - `while True` (+1, nesting 0).
  - Nested `if isdigit()` (+2, nesting 1).
  - Deeply nested boundary `if` (+3, nesting 2).
  - Two `else` fallbacks (+1 + 1) $ightarrow 1 + 2 + 3 + 1 + 1 = 8$.
- **`spin` (Score = 8)**:
  - Two sequential validation routines: `while` (+1) + nested `if` (+2) + `else` (+1) = 4 points each $ightarrow 4 + 4 = 8$.
- **`main` (Score = 9)**:
  - Session `while True` (+1, nesting 0).
  - Nested `if balance < MIN_BET` (+2, nesting 1).
  - Deeper `if top_up == 'y'` (+3, nesting 2) with fallback `else` (+1).
  - Prompt check `if answer == 'q'` (+2, nesting 1) $ightarrow 1 + 2 + 3 + 1 + 2 = 9$.

**Industry Assessment**: SonarQube flags any function with Cognitive Complexity greater than **15** as code smell requiring refactoring. Our highest score is **9** (in `main`), proving the code is intuitive and readable.

---

### Time Complexity (Algorithmic Runtime)

Let us define the operational parameters:
- $R$ = Number of rows ($R = 3$).
- $C$ = Number of columns ($C = 3$).
- $L$ = Number of lines bet on ($1 \le L \le 3$).
- $S$ = Size of symbol pool ($S = 20$).
- $K$ = Number of retries a user takes to type valid input.
- $N$ = Number of total spins played across the session.

#### 1. Per Spin Operation: $\mathcal{O}(1)$ (Constant Time)
- **Symbol Generation (`get_slot_machine_spin`)**:
  - Populating `all_symbols`: $\mathcal{O}(S) = 20$ iterations.
  - Slicing `all_symbols[:]`: $\mathcal{O}(S) = 20$ operations.
  - Sampling: Across $C$ columns and $R$ rows, `random.choice` is $\mathcal{O}(1)$, while `list.remove()` is $\mathcal{O}(S)$ linear scan. Total operations = $C 	imes (S + R \cdot S) = 3 	imes (20 + 3 	imes 20) = 240$ operations.
- **Payline Evaluation (`check_winnings`)**:
  - Checks $L$ lines across $C$ columns: $L 	imes C = 3 	imes 3 = 9$ comparisons.
- **Terminal Printing (`print_slot_machine`)**:
  - Performs $R 	imes C = 9$ formatted output operations.

Because $R$, $C$, and $S$ are fixed physical constants, the runtime per round does not depend on an expanding input $n$. Mathematically:
$$T(	ext{spin}) = \mathcal{O}(C \cdot R \cdot S + L \cdot C) = \mathcal{O}(1)$$
Every spin executes instantaneously in **$\mathcal{O}(1)$ Constant Time**.

#### 2. Full Application Lifecycle: $\mathcal{O}(N)$
Across an entire play session of $N$ spins:
$$T(	ext{session}) = \mathcal{O}(N 	imes T(	ext{spin})) = \mathcal{O}(N)$$
The application exhibits perfect linear time complexity scaling directly with the number of rounds played.

---

### Space Complexity (Memory Footprint)

Space complexity evaluates auxiliary memory allocated by the program during execution.

#### 1. Global & State Memory:
- `symbol_count` and `symbol_value` dictionaries store 4 keys each: $\mathcal{O}(1)$.
- Scalar integers (`balance`, `lines`, `bet`, `total_bet`): $\mathcal{O}(1)$.

#### 2. Local Heap Memory per Round:
- In `get_slot_machine_spin`:
  - `all_symbols` holds 20 strings.
  - `current_symbols` holds 20 strings.
  - `columns` 2D list holds 3 column sublists of 3 strings each (9 items total).
- In `check_winnings`:
  - `winnings_lines` list holds at most 3 integers: $\mathcal{O}(L)$.

#### Total Memory Bound:
The peak auxiliary memory allocated at any microsecond of execution is:
$$	ext{Space}(	ext{peak}) = \mathcal{O}(S + R \cdot C + L) = \mathcal{O}(20 + 9 + 3) = \mathcal{O}(1)$$
The total memory footprint is less than **50 kilobytes** including Python interpreter overhead, operating strictly in **$\mathcal{O}(1)$ Constant Auxiliary Space**.

---

## 10. Key Takeaways & Conclusion

By dissecting this Python Slot Machine project, we have demonstrated that even a simple terminal application can reflect modern software engineering excellence:

1. **Defensive Input Validation**: By pairing `.isdigit()` with range assertions and balance guards, user errors never cause unhandled exceptions or infinite bankruptcy loops.
2. **Matrix Modeling**: We converted column-major data structures into human-readable horizontal lines using clean nested loops and index offsets.
3. **Pythonic Idioms**: Using `for...else` to detect matching paylines and `all_symbols[:]` shallow copying showcase how Python's syntax enables concise, expressive logic.
4. **Algorithmic Efficiency**: With an average Cyclomatic Complexity of **4.38**, Cognitive Complexity of **7.63**, **$\mathcal{O}(1)$** space complexity, and **$\mathcal{O}(1)$** per-spin time complexity, this implementation is clean, production-grade, and scalable.

Whether you are preparing for coding interviews, refining your OOP fundamentals, or publishing tutorials, building small projects with this degree of structural rigor is what distinguishes everyday coders from true software craftsmen.
