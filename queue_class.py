class queue: 
    def __init__(self, arr, max_size):  #----------define the variable where the array is held and the max size of the queue 
        self.arr = arr 
        self.max_size = max_size 
    def isFull(self):                       
        if len(self.arr) == self.max_size: #-------define a method to check if the queue is full 
            return True 
        else: 
            return False 
    def enqueue(self, item):                #--------if the queue is full, append the new item and remove the first item 
        if self.isFull():
            for i in range(1, len(self.arr)): 
                self.arr[i-1] = self.arr[i]
            self.arr[-1] = item 
        else: 
            self.arr.append(item)           #--------if it is not full then append the new item at the end
        return self.arr
        