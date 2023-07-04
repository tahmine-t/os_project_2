import re
from scheduler import scheduler

def main():

    # inp = input("enter number of available resources: ").strip()
    # # R1 R2 R3
    # resrc_num = re.split(r'\s+', inp)
    # for i in range(len(resrc_num)):
    #     resrc_num[i] = int(resrc_num[i])

    # n = int(input("enter number of tasks: "))
    # task = [];
    # for i in range(n):
    #     inp = input(f"enter task {i+1} name, type and duration: ").strip()
    #     inp = re.split(r'\s+', inp)
    #     thisdict = {
    #         "name": inp[0],
    #         "type": inp[1],
    #         "duration": int(inp[2]),
    #         "status" : "ready",
    #         "cpu_time" : 0,
    #         "has_src": False
    #     }
    #    task.append(thisdict)

    # mySched = scheduler(resrc_num, task)
    # mySched.FCFS()
    # mySched.SJF()
    # mySched.RR()

    resrc_num = [20, 20, 20]
    task = [
        {"name": "Task1", "type": "X", "duration": 3, "status": "ready", "cpu_time": 0, "has_src": False},
        {"name": "Task2", "type": "Y", "duration": 4, "status": "ready", "cpu_time": 0, "has_src": False},
        {"name": "Task3", "type": "X", "duration": 2, "status": "ready", "cpu_time": 0, "has_src": False},
        {"name": "Task4", "type": "X", "duration": 2, "status": "ready", "cpu_time": 0, "has_src": False},
        {"name": "Task5", "type": "Y", "duration": 3, "status": "ready", "cpu_time": 0, "has_src": False},
        {"name": "Task6", "type": "Z", "duration": 4, "status": "ready", "cpu_time": 0, "has_src": False}
    ]

    s = scheduler(resrc_num, task)

    # s.RR(quantum=2)
    # s.FCFS()
    s.SJF()


if __name__ == "__main__":
    main()
