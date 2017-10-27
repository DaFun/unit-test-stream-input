#!/usr/bin/env python
from median import Median
import datetime

# parse the relevant fields from line
def process_data(line):
    fields = line.strip().split('|')
    return fields[0], fields[10][:5], fields[13], int(fields[14]), fields[15]


# process median_by_zip file 
def median_by_zip(dict_by_zip, cmte, zip, amt, out):
    # get the zip dictionary according to the recipient id 
    zip_dict = dict_by_zip.get(cmte, None)
    
    # if dict_by_zip already has the recipient record
    if zip_dict:
        # get the median object according to zip code 
        median = zip_dict.get(zip, None)
        if median:
            median.add_num(amt)
            ready_to_print_median = median.find_median()
            ready_to_print_num = median.get_num()
            ready_to_print_total = median.get_total()
        else:
            # if this recipient no this zip code record, then init a new Median obj for this zip code
            median = Median()
            median.add_num(amt)
            zip_dict[zip] = median
            ready_to_print_median = median.find_median()
            ready_to_print_num = median.get_num()
            ready_to_print_total = median.get_total()
    else:
        # dict_by_zip no this recipient record, init a new zip dictionary relate to this recipient id
        # and init a new median obj, add the value
        zip_dict = {}
        median = Median()
        median.add_num(amt)
        zip_dict[zip] = median
        dict_by_zip[cmte] = zip_dict
        ready_to_print_median = median.find_median()
        ready_to_print_num = median.get_num()
        ready_to_print_total = median.get_total()
        
    # print out info according to the median object
    out.write("{} | {} | {} | {} | {}\n".format(cmte, zip, ready_to_print_median, ready_to_print_num, ready_to_print_total))


def median_by_date(dict_by_date, cmte, date, amt):
    # get the records of this recipient
    date_dict = dict_by_date.get(cmte, None)

    # convert date string to datetime object in order to sort
    dt = datetime.datetime.strptime(date, "%m%d%Y")

    if date_dict:
        median = date_dict.get(dt, None)

        # if the record relate to this recipient at this date already be stored
        if median:
            median.add_num(amt)
        else:
            # init a new median object to store the values
            median = Median()
            median.add_num(amt)
            date_dict[dt] = median
    else:
        # no records at this date have been found, then init a new dictionary for this date
        date_dict = {}
        median = Median()
        median.add_num(amt)
        date_dict[dt] = median
        dict_by_date[cmte] = date_dict


# print out median_by_date at the end
def print_median_by_date(dict_by_date, out):
    # sorted alphabetical by recipient
    for cmte, v in sorted(dict_by_date.items()):

        # sorted chronologically by date
        for dt, median in sorted(v.items()):
            date = dt.strftime("%m%d%Y")
            ready_to_print_median = median.find_median()
            ready_to_print_num = median.get_num()
            ready_to_print_total = median.get_total()
            out.write("{} | {} | {} | {} | {}\n".format(cmte, date, ready_to_print_median, ready_to_print_num, ready_to_print_total))


with open('../input/test') as f, open('../output/test1', 'w') as out, open('../output/test2', 'w') as out1:
    dict_by_zip = {}
    dict_by_date = {}
    for line in f:
        cmte, zip, dt, amt, id = process_data(line)
        if not id:
            median_by_zip(dict_by_zip, cmte, zip, amt, out)
            median_by_date(dict_by_date, cmte, dt, amt)
    print_median_by_date(dict_by_date, out1)