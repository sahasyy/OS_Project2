import threading
import random
import time

#constants
NUM_TELLERS = 3
NUM_CUSTOMERS = 50

#semaphores and the locks
bank_open = threading.Event()
door_sem = threading.Semaphore(2)
safe_sem = threading.Semaphore(2)
manager_sem = threading.Semaphore(1)

#shared queues and comms
available_tellers = []
available_tellers_lock = threading.Lock()

customer_queue = []
queue_lock = threading.Lock()

#each customer will have their own set of semaphores to sync with the teller
customer_ready = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
teller_ready = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
transaction_done = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]
customer_left = [threading.Semaphore(0) for _ in range(NUM_CUSTOMERS)]

#tracking served cust
customers_served = 0
customers_served_lock = threading.Lock()
done_event = threading.Event()

#teller threads
transaction_map = {}
class Teller(threading.Thread):
    def __init__(self, tid):
        super().__init__()
        self.tid = tid

    def run(self):
        print(f"Teller {self.tid}: ready to serve")
        
        while not done_event.is_set():
            cid = None
            with queue_lock:
                if customer_queue:
                    cid = customer_queue.pop(0)
                else:
                    available_tellers.append(self)

            if cid is None:
                time.sleep(0.01)
                continue

            print(f"Teller {self.tid}: calls Customer {cid}")
            customer_ready[cid].release()
            teller_ready[cid].acquire()

            transaction_type = transaction_map[cid]
            print(f"Teller {self.tid} [Customer {cid}]: receives {transaction_type}")

            if transaction_type == 'Withdraw':
                print(f"Teller {self.tid}: going to manager for Customer {cid}")
                manager_sem.acquire()
                print(f"Teller {self.tid}: interacting with manager")
                time.sleep(random.uniform(0.005, 0.03))
                print(f"Teller {self.tid}: done with manager")
                manager_sem.release()

            print(f"Teller {self.tid}: going to safe for Customer {cid}")
            safe_sem.acquire()
            print(f"Teller {self.tid}: using safe")
            time.sleep(random.uniform(0.01, 0.05))
            print(f"Teller {self.tid}: done with safe")
            safe_sem.release()

            print(f"Teller {self.tid} [Customer {cid}]: transaction complete")
            transaction_done[cid].release()
            customer_left[cid].acquire()

            with customers_served_lock:
                global customers_served
                customers_served += 1
                if customers_served == NUM_CUSTOMERS:
                    done_event.set()

        print(f"Teller {self.tid}: finished for the day")


#cust thread
class Customer(threading.Thread):
    def __init__(self, cid):
        super().__init__()
        self.cid = cid

    def run(self):
        transaction = random.choice(['Deposit', 'Withdraw'])
        transaction_map[self.cid] = transaction

        time.sleep(random.uniform(0, 0.1))
        door_sem.acquire()
        print(f"Customer {self.cid}: enters the bank")

        assigned_teller = None
        with available_tellers_lock:
            if available_tellers:
                assigned_teller = available_tellers.pop(0)

        if assigned_teller:
            print(f"Customer {self.cid} [Teller {assigned_teller.tid}]: selects teller")
            with queue_lock:
                customer_queue.append(self.cid)
        else:
            with queue_lock:
                customer_queue.append(self.cid)

        customer_ready[self.cid].acquire()
        print(f"Customer {self.cid}: introduces self to Teller")
        teller_ready[self.cid].release()
        print(f"Customer {self.cid}: tells teller to {transaction}")

        transaction_done[self.cid].acquire()
        print(f"Customer {self.cid}: transaction complete, leaving")
        customer_left[self.cid].release()
        door_sem.release()


#start the simulation
def main():
    tellers = [Teller(tid) for tid in range(NUM_TELLERS)]
    customers = [Customer(cid) for cid in range(NUM_CUSTOMERS)]

    for t in tellers:
        t.start()

    for c in customers:
        c.start()

    for c in customers:
        c.join()

    for t in tellers:
        t.join()

    print("\nBank closed. All customers served.")


if __name__ == '__main__':
    main()
