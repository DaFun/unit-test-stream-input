#!/usr/bin/env python

import re
from heapq import *

class Median:
    def __init__(self):
        self.heaps = [], []
        self.total = 0
        self.num = 0

    def add_num(self, num):
        small, large = self.heaps
        heappush(small, -heappushpop(large, num))
        if len(large) < len(small):
            heappush(large, -heappop(small))
        self.num += 1
        self.total += num

    def find_median(self):
        small, large = self.heaps
        if len(large) > len(small):
            return float(large[0])
        return (large[0] - small[0]) / 2.0

    def get_num(self):
        return self.num

    def get_total(self):
        return self.total

def process_data(line):
    fields = line.strip().split('|')
    return fields[0], fields[10][:5], fields[13], int(fields[14]), fields[15]

with open('../input/test') as f, open('../output/test', 'w') as out:
    file_by_zip = {}
    for line in f:
        cmte, zip, dt, amt, id = process_data(line)
        if not id:
            zip_dict = file_by_zip.get(cmte, None)
            if zip_dict:
                median = zip_dict.get(zip, None)
                if median:
                    median.add_num(amt)
                    out_median = median.find_median()
                    out_num = median.get_num()
                    out_total = median.get_total()
                else:
                    median = Median()
                    median.add_num(amt)
                    zip_dict[zip] = median
                    out_median = median.find_median()
                    out_num = median.get_num()
                    out_total = median.get_total()
            else:
                zip_dict_tmp = {}
                median = Median()
                median.add_num(amt)
                zip_dict_tmp[zip] = median
                file_by_zip[cmte] = zip_dict_tmp
                out_median = median.find_median()
                out_num = median.get_num()
                out_total = median.get_total()
            out.write("{} | {} | {} | {} | {}\n".format(cmte, zip, out_median, out_num, out_total))