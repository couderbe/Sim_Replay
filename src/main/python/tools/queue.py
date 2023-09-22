import math

class Queue:

    def __init__(self, _size) -> None:
        self.queue = []
        self.size = _size
        self.m = math.inf
        self.M = -math.inf

    def add(self, val) -> None:
        if(len(self.queue) >= self.size):
            self.queue.pop(0)
        if val!=None:
            if(val>self.M):
                self.M = val
            if(val<self.m):
                self.m = val
        self.queue.append(val)
    
    def get_values(self)->list:
        return self.queue
    
    def get_size(self)->int:
        return len(self.queue)