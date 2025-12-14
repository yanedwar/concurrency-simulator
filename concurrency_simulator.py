import threading
import queue
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    remaining: int


class Worker(threading.Thread):
    def __init__(self, wid, cmd_q, res_q):
        super().__init__(daemon=True)
        self.worker_id = wid
        self.cmd_q = cmd_q
        self.res_q = res_q

    def run(self):
        while True:
            task, units = self.cmd_q.get()
            if task is None:
                break
            executed = min(units, task.remaining)
            self.res_q.put((task.id, executed, self.worker_id))
            self.cmd_q.task_done()


class Scheduler:
    def __init__(self, tasks, workers=2, quantum=1):
        self.tasks = tasks
        self.quantum = quantum
        self.cmd_q = queue.Queue()
        self.res_q = queue.Queue()
        self.workers = [Worker(i, self.cmd_q, self.res_q) for i in range(workers)]

    def run(self):
        for worker in self.workers:
            worker.start()

        tick = 0
        while any(task.remaining > 0 for task in self.tasks):
            for task in self.tasks:
                if task.remaining > 0:
                    tick += 1
                    self.cmd_q.put((task, self.quantum))
                    tid, done, wid = self.res_q.get()
                    task.remaining -= done
                    print(f"tick {tick}: worker {wid} ran task {tid}, remaining={task.remaining}")

        for _ in self.workers:
            self.cmd_q.put((None, 0))

if __name__ == "__main__":
    tasks = [Task(i + 1, 3) for i in range(5)]
    Scheduler(tasks).run()
