from datetime import datetime
from threading import Thread
from tasks.task import *
from typing import List
from srv.null import AddRequest, AddResponse
import rospy as ros
import std_srvs.srv as srv
import std_msgs.msg as msg

class Scheduler:
    def __init__(self) -> None:
        self.tasks: List[Task] = []
        self.running_tasks: List[Task] = []
        # self.isRun = False
        self.isBusy = False
        self.dirty = False

    def is_busy_decor(func):
        def wrapper(self, *args, **kwargs):
            while self.isBusy:
                pass

            self.isBusy = True
            res = func(self, *args, **kwargs)
            self.isBusy = False
            return res
        return wrapper
    
    @is_busy_decor
    def append(self, task: AddRequest) -> None:
        # if issubclass(type(task), Task):
        #     raise TypeError(f"task have type: {type(task)}, but must be {type(Task)}")
        
        self.dirty = True
        self.tasks.append(Task(task.name, task.args, task.date))

        # if not self.isRun:
        #     self.run()

    @is_busy_decor
    def get_next(self) -> Task:
        if self.dirty:
            self.tasks.sort()
            self.dirty = False
        
        task = None
        while task is None and len(self.tasks) != 0:
            task = self.tasks[0]
            self.tasks.remove(task)
            if task < datetime.now():
                task = None

        if task is None:
            raise IndexError("get from an empty list")

        return task
    
    def run_task(self, task: Task) -> None:
        if task.isAsync:
            task.isAsync = False
            Thread(target=self.run_task, args=(task))
        
        service = ros.ServiceProxy(task.name, srv.Empty)
        raise NotImplementedError() # change type
        service(task.args)

    def run(self) -> None:
        self.isRun = True

        while len(self.tasks) == 0:
            # TODO do some shit
            raise NotImplementedError()

        self.isRun = False
             
