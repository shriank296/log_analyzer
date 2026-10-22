import threading
import time
from concurrent.futures import ThreadPoolExecutor

from utils import time_spent


def task(name: str) -> None:
    print(f"{name} started")
    time.sleep(2)
    if name == "Task 2":
        raise ValueError
    print(f"{name} finished")


with ThreadPoolExecutor(max_workers=2) as executor:
    future1 = executor.submit(task, "Task 1")
    future2 = executor.submit(task, "Task 2")
    future3 = executor.submit(task, "Task 3")
    future1.result()
    future2.result()
    future3.result()


# thread1 = threading.Thread(target=task, args=("Task 1",))
# thread2 = threading.Thread(target=task, args=("Task 2",))

# thread1.start()
# thread2.start()

# thread1.join()
# thread2.join()

print("All tasks completed successfully")
