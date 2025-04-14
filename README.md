# Project: sahas-os-project2 – Multithreaded Bank Simulation

This project simulates a simplified banking environment using Python threads and semaphores. It models 3 tellers and 50 customers, enforcing access rules for shared resources like the manager, the safe, and the bank entrance.

## Folder Layout

```
sahas-os-project2/
├── bank_simulation.py  # Main Python script for the simulation
├── devlog.md           # Development log with implementation notes
├── README.md           # This file
└── output.txt   
```

## Program Description

### `bank_simulation.py`
- Launches 3 **Teller** threads and 50 **Customer** threads.
- Synchronizes access to:
  - **Manager**: only 1 teller may interact at a time.
  - **Safe**: only 2 tellers may enter at a time.
  - **Bank Door**: only 2 customers may enter simultaneously.
- Each customer selects either **Deposit** or **Withdraw** randomly.
- Tellers interact with the manager for withdrawals, then enter the safe to process all transactions.
- Thread-safe logging prints every step of the simulation in the required format.

### `devlog.md`
- Tracks the project’s development from initial setup to final debugging.
- Lists all design choices, bugs encountered, and their solutions.
- Contains a summary of what works and what could be improved.

### `sample_output.txt`
- Captures a full run of the simulation.
- Demonstrates correct synchronization and thread interaction output.

## getting it started

1. Ensure Python 3.7 or newer is installed.
2. Open a terminal and navigate to the project folder.
3. Run the simulation with:

```bash
python3 bank_simulation.py
```

You can redirect output to a file with:
```bash
python3 bank_simulation.py > sample_output.txt
```

## output Format
Each action follows the format:
```
THREAD_TYPE ID [OTHER_THREAD_TYPE ID]: MESSAGE
```
example:
```
Customer 5 [Teller 1]: selects teller
Teller 1: going to manager for Customer 5
Teller 1: done with manager
Teller 1: going to safe
```

## Additional notes
- Implements robust semaphore-based synchronization with clean exit logic.
- Prevents deadlocks and ensures all 50 customers are served before tellers exit.
- Demonstrates real-world operating systems concepts in a multithreaded Python environment.
