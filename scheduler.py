from collections import deque
from time import sleep

# TASK TYPES:
# Z: 1 - R1, R3
# Y: 2 - R2, R3
# X: 3 - R1, R2

class scheduler:
    def __init__(self, resrc_num, task):
        self.resrc_num = resrc_num
        self.task = task
        self.time = self.set_time()
        self.current_time = 0
        self.running = self.update_running()
        self.waiting = self.update_waiting()
        self.ready = self.update_ready()

    def set_time(self):
        time = 0;
        for i in range(len(self.task)):
            time += self.task[i].get("duration")
        return time

    def FCFS(self):
        for i in range(self.time):
            if i != self.current_time:
                continue

            task_num = self.get_highest_priority();

            cur_task = self.task[task_num]
            name = cur_task.get("name")
            d = cur_task.get("duration")

            run = self.take_resource(task_num)

            if run:
                self.task[task_num].update({"status": "running"})
                for j in range(d):
                    self.print_stats()
                    self.current_time += 1
                    sleep(0.1)
                
                self.task[task_num].update({"status": "terminated"})
                self.task[task_num].update({"cpu_time": d})
                self.free_resource(task_num)

            else:
                print(f"not enough resources for {name}")
                self.task[task_num].update({"status": "waiting"})
                self.current_time -= 1

    def SJF(self):
        for i in range(self.time):
            if i != self.current_time:
                continue

            task_num = self.get_shortest_job();

            cur_task = self.task[task_num]
            name = cur_task.get("name")
            d = cur_task.get("duration")

            run = self.take_resource(task_num)

            if run:
                self.task[task_num].update({"status": "running"})
                for j in range(d):
                    self.print_stats()
                    self.current_time += 1
                    sleep(0.1)
                
                self.task[task_num].update({"status": "terminated"})
                self.task[task_num].update({"cpu_time": d})
                self.free_resource(task_num)

            else:
                print(f"not enough resources for {name}")
                self.task[task_num].update({"status": "waiting"})
                self.current_time -= 1

    def RR(self, quantum):
        for i in range(self.time):
            if i % 3 == 0:
                for task in self.task:
                    if task.get("status") == "waiting":
                        task.update({"status": "ready"})

            if i != self.current_time:
                continue

            task_num = self.get_highest_priority();

            cur_task = self.task[task_num]
            name = cur_task.get("name")
            d = cur_task.get("duration")
            cpu_t = cur_task.get("cpu_time")
            remaining_time = d - cpu_t
            t = min(remaining_time, quantum)

            run = self.take_resource(task_num)

            if run:
                self.task[task_num].update({"status": "running"})

                for j in range(t):
                    self.print_stats()
                    self.current_time += 1
                    sleep(0.1)

                cpu_t += t
                cur_task.update({"cpu_time": cpu_t})

                if d == cpu_t:
                    cur_task.update({"status": "terminated"})
                    self.free_resource(task_num)
                else:
                    cur_task.update({"status": "ready"})

                self.task.pop(task_num)
                self.task.append(cur_task)

            else:
                print(f"not enough resources for {name}")
                self.task[task_num].update({"status": "waiting"})
                self.current_time -= 1

    def update_running(self):
        for i in range(len(self.task)):
            if self.task[i].get("status") == "running" :
                return self.task[i].get("name")

    def update_waiting(self):
        waiting = []
        for i in range(len(self.task)):
            if self.task[i].get("status") == "waiting" :
                waiting.append(self.task[i].get("name"))
        return waiting

    def update_ready(self):
        ready = []
        for i in range(len(self.task)):
            if self.task[i].get("status") == "ready" :
                ready.append(self.task[i].get("name"))
        return ready

    def take_resource(self, task_num):
        if self.task[task_num].get("has_src") == True:
            return True
        type = self.task[task_num].get("type")
        if type == "X":
            if self.resrc_num[0] > 0 and self.resrc_num[1] > 0:
                self.resrc_num[0] -= 1
                self.resrc_num[1] -= 1
                self.task[task_num].update({"has_src": True})
                return True
        elif type == "Y":
            if self.resrc_num[2] > 0 and self.resrc_num[1] > 0:
                self.resrc_num[2] -= 1
                self.resrc_num[1] -= 1
                self.task[task_num].update({"has_src": True})
                return True
        elif type == "Z":
            if self.resrc_num[0] > 0 and self.resrc_num[2] > 0:
                self.resrc_num[0] -= 1
                self.resrc_num[2] -= 1
                self.task[task_num].update({"has_src": True})
                return True
        return False

    def free_resource(self, task_num):
        type = self.task[task_num].get("type")
        if type == "X":
            self.resrc_num[0] += 1
            self.resrc_num[1] += 1
        elif type == "Y":
            self.resrc_num[2] += 1
            self.resrc_num[1] += 1
        elif type == "Z":
            self.resrc_num[0] += 1
            self.resrc_num[2] += 1
        self.task[task_num].update({"has_src": False})

    def get_highest_priority(self):
        for i in range(len(self.task)):
            p = self.task[i].get("type")
            s = self.task[i].get("status")
            if p == "Z" and s == "ready":
                return i
        for i in range(len(self.task)):
            p = self.task[i].get("type")
            s = self.task[i].get("status")
            if p == "Y" and s == "ready":
                return i
        for i in range(len(self.task)):
            p = self.task[i].get("type")
            s = self.task[i].get("status")
            if p == "X" and s == "ready":
                return i

    def get_shortest_job(self):
        index = 0
        min = 20
        for i in range(len(self.task)):
            d = self.task[i].get("duration")
            s = self.task[i].get("status")
            if d < min and s == "ready":
                min = d
                index = i
        return index

    def print_stats(self):
        self.running = self.update_running()
        self.waiting = self.update_waiting()
        self.ready = self.update_ready()
        print(f"\n#### current time = {self.current_time} ####")
        print(f"running process = {self.running}")
        print(f"wating queue = {self.waiting}")
        print(f"ready queue = {self.ready}")
        print(f"available R1 = {self.resrc_num[0]}")
        print(f"available R2 = {self.resrc_num[1]}")
        print(f"available R3 = {self.resrc_num[2]}\n")

