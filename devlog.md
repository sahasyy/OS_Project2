# Dev Log – CS4348 Project 2 Sahas Sharma SXS210541

## [04/13/2025] 10:14 AM
- Read through the full PDF spec from eLearning
- Identified major components: 3 Teller threads, 50 Customer threads
- Recognized critical shared resources: bank door (2 customers), safe (2 tellers), manager (1 teller)
- Decided to use Python with the `threading` module and `Semaphore` for synchronization

## [04/13/2025] 12:33 PM
### Planning Notes
- Broke the simulation into 2 main classes: `Teller` and `Customer`
- Mapped out inter-thread communcation using per customer semphores
- Brainstormed structure of logging and sequencing actions per spec

## [04/13/2025] 1:15 PM (session 1 begins)
- created skeleton for `Teller` and `Customer` thread classes
- added global structures: `transaction_map`, semaphres, locks, and queue logic
- implemented customer thread: random transaction type, entrance wait, teller selection

## [04/13/2025] 3:30 PM (session 1 ends)
- customers could enter and select tellers, but tellers were terminating immediately
- realized early exit condition was incorrect — tellers needed a better way to wait for customers

## [04/13/2025] 4:50 PM (session 2 begins)
- remade teller loop to wait for all 50 custmers to finish using a shared `customers_served` counter
- introduced `done_event` to cleanly terminate all teller threads after simulation
- Wrapped queue access and teller assignment in appropriate locks

## [04/13/2025] 6:00 PM (session 2 ends)
- Teller now waits properly, interacts with manager and safe with correct logging and delay
- confirmed output meets requred format: `THREAD_TYPE ID [THREAD_TYPE ID]: MSG`
- All shared resources now log three lines: going to, using, done using

## [04/13/2025] 7:30 PM (session 3 begins)
- tested full simulation with 50 customers
- output validated for: entry/exit control, transaction sequncing, correct thread sync
- All edge cases handled (e.g., customers waiting, tellers sharing safe/manager access)

## [04/13/2025] 9:15 PM (session 3 ends)
- created `README.md` with full project instructions and structure
- finished timestamped `devlog.md` file

## [04/13/2025] 10:51 PM (session 4 begins)
- final cleanup pass before submission
- verufy the semaphores prevent race condtions
- output reviewed and sample run redirected to `output.txt`

## [04/13/2025] 11:40 PM (session 4 ends)
- All deliverables ready: `bank_simulation.py`, `README.md`, `devlog.md`, `sample_output.txt`
- code is submission ready and passes all logical checks
- Submitted right on time 

