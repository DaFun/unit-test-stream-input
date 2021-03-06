from heapq import *

class Median:
    def __init__(self):
        self.heaps = [], []
        self.total = 0
        self.num = 0

    def add_num(self, num):
        # smaller half and bigger half of values
        small, large = self.heaps

        # push inverted values into small, so make small as a max-heap
        heappush(small, -heappushpop(large, num))

        # keep large hold the median if odd elements
        if len(large) < len(small):
            heappush(large, -heappop(small))
        self.num += 1
        self.total += num

    def get_median(self):
        small, large = self.heaps

        # odd elements in total
        if len(large) > len(small):
            return large[0]

        # even elements in total
        else:
            # deal with round up, especially when meet big number
            middle = large[0] - small[0]
            res = middle if middle >= 0 else -middle
            res = (res >> 1) + (res & 1)
            return res if middle >= 0 else -res

    def get_num(self):
        return self.num

    def get_total(self):
        return self.total