#!/usr/bin/env python
from median import Median


def process_data(line):
    fields = line.strip().split('|')
    return fields[0], fields[10][:5], fields[13], int(fields[14]), fields[15]

with open('../input/test') as f, open('../output/test1', 'w') as out:
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