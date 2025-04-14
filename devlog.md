# Project 2 Dev Log – CS4348 Spring 2024

## Timeline

### April 10, 2024 – Made GitHub repo
- Read the full project description from `project2.pdf`.
- Identified major thread entities: 3 tellers, 50 customers.
- Noted synchronization requirements: manager (1), safe (2), door (2), and communication between each customer-teller pair.
- Chose Python for implementation (using `threading` and `Semaphore`).

### April 11, 2024 – First Implementation
- Created thread classes: `Teller` and `Customer`.
- Set up initial semaphores:
  - `manager_sem`, `safe_sem`, `door_sem`.
  - Per-customer semaphores for `customer_ready`, `teller_ready`, `transaction_done`, and `customer_left`.
- Introduced global `transaction_map` for transaction type lookup.
- Tellers immediately exited due to incorrect termination condition based on `customer_queue`.

### April 12, 2024 – Debugging & Finalizing
- Fixed teller exit logic by adding:
  - `customers_served` counter
  - `customers_served_lock`
  - `done_event` to gracefully terminate tellers after serving 50 customers
- Added realistic `time.sleep()` to simulate manager and safe interactions
- Verified console logs matched format: `THREAD_TYPE ID [OTHER_THREAD_TYPE ID]: MESSAGE`
- Ran full simulation — verified all threads completed and simulation terminated with: `Bank closed. All customers served.`

## Key Design Decisions

### semaphore Use:
- **Manager**: `Semaphore(1)` — only one teller at a time.
- **Safe**: `Semaphore(2)` — max two tellers inside.
- **Bank Door**: `Semaphore(2)` — max two customers enter at a time.
- **Customer-Teller Sync**: 4 semaphores per customer thread to handle: greeting, transaction exchange, completion, and leaving.

### synchronization Mechanisms:
- Used `queue_lock` to protect shared customer queue.
- Used `available_tellers_lock` for managing idle teller pool.
- Avoided deadlocks using simple conditional waits and retry logic (via small `sleep`).

## what has worked
- Thread-safe interaction between 3 tellers and 50 customers
- Manager and safe access rules enforced
- Every customer completes exactly one transaction
- Terminal output clearly tracks all actions

## some limiations
- Does not simulate bank opening delay (tellers are ready immediately)
- Customers may wait longer than needed if not perfectly balanced across tellers
- No queue priority or advanced fairness logic

## what I learnt
- Practical semaphore-based synchronization in Python
- Real-time debugging of thread coordination issues
- Importance of separating customer-teller pairs with unique semaphores
- Dealing with early thread exits and graceful termination using global counters
