from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any

executer = ThreadPoolExecutor(max_workers=2)

tasks = [
    lambda: print("Hello"),
    lambda: "what",
    lambda: print("Halo"),
    lambda: print("Heaven"),
    lambda: print("Hell"),
    lambda: print("Overworld"),
]

def callback(future: Future[Any]):
    try:
        string = future.result()
        print(string)
    except Exception as _:
        pass


for task in tasks:
    future = executer.submit(task)
    future.add_done_callback(callback)