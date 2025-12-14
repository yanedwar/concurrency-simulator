import threading
import queue
from dataclasses import dataclass
from typing import List

#to do:
#add more structed logging methods
#allow workers to be able to execute variable amounts of work

@dataclass
#with priority: lower number means higher priority
class Task:
    id: int
    remaining: int
    priority: int = 0


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
    def __init__(self, tasks: List[Task], workers=2, quantum=1, policy="round_robin"):
        self.tasks = tasks
        self.quantum = quantum
        self.policy = policy
        self.cmd_q = queue.Queue()
        self.res_q = queue.Queue()
        self.workers = [Worker(i, self.cmd_q, self.res_q) for i in range(workers)]

    def _select_task(self):
        active = [t for t in self.tasks if t.remaining > 0]
        if not active:
            return None

        if self.policy == "priority":
            return sorted(active, key=lambda t: (t.priority, t.id))[0]

        return active[0]

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

                    print(
                        f"tick {tick}: worker {wid} ran task {tid} "
                        f"(priority={task.priority}), remaining={task.remaining}"
                    )

        for _ in self.workers:
            self.cmd_q.put((None, 0))


if __name__ == "__main__":
    tasks = [
        Task(id=1, remaining=5, priority=2),
        Task(id=2, remaining=4, priority=0),
        Task(id=3, remaining=3, priority=1),
    ]

    Scheduler(tasks, policy="priority").run() #leave string empty for round-robin
