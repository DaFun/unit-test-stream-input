from heapq import *

class Median:
    def __init__(self):
        self.heaps = [], []
        self.total = 0
        self.num = 0

    def add_num(self, num):
        small, large = self.heaps
        heappush(small, heappushpop(large, num))
        if len(large) < len(small):
            heappush(large, heappop(small))
        self.num += 1
        self.total += num

    def find_median(self):
        small, large = self.heaps
        if len(large) > len(small):
            return large[0]
        return ((large[0] + small[0]) >> 1) + ((large[0] + small[0]) & 1)

    def get_num(self):
        return self.num

    def get_total(self):
        return self.total