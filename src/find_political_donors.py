#!/usr/bin/env python
from median import Median
import datetime
import argparse


# parse the relevant fields from line
def process_data(line):
    # if valid for CMTE_ID, TRANSACTION_AMT, or OTHER_ID
    other_valid = False

    # if TRANSACTION_DT valid
    date_valid = False

    # if zip_code valid
    zip_valid = False

    fields = line.strip().split('|')

    if len(fields) < 16:
        return [None]*4, other_valid, date_valid, zip_valid

    cmte, zip, date, amt, id = fields[0], fields[10], fields[13], fields[14], fields[15].strip()
    if cmte and not id:
        other_valid = True
    else:
        return [None]*4, other_valid, date_valid, zip_valid

    # make sure amt is valid integer
    try:
        amt = int(amt)
    except ValueError:
        other_valid = False

    # convert date string to datetime object, and check if it's malformed
    try:
        dt = datetime.datetime.strptime(date, "%m%d%Y")
        date_valid = True
    except ValueError:
        dt = None

    # parse zip code
    if len(zip) >= 5:
        zip_valid = True
        zip = zip[:5]

    return [cmte, zip, dt, amt], other_valid, date_valid, zip_valid


# process median_by_zip file 
def median_by_zip(dict_by_zip, cmte, zip, amt, out):
    # get the zip dictionary according to the recipient id 
    zip_dict = dict_by_zip.get(cmte, None)
    

    # if dict_by_zip already has the recipient transaction
    if zip_dict:
        # get the median object according to zip code 
        median = zip_dict.get(zip, None)
        if median:
            median.add_num(amt)
            ready_to_print_median = median.get_median()
            ready_to_print_num = median.get_num()
            ready_to_print_total = median.get_total()
        else:
            # if this recipient no this zip code transaction, then init a new Median obj for this zip code
            median = Median()
            median.add_num(amt)
            zip_dict[zip] = median
            ready_to_print_median = median.get_median()
            ready_to_print_num = median.get_num()
            ready_to_print_total = median.get_total()
    else:
        # dict_by_zip no this recipient transaction, init a new zip dictionary relate to this recipient id
        # and init a new median obj, add the value
        zip_dict = {}
        median = Median()
        median.add_num(amt)
        zip_dict[zip] = median
        dict_by_zip[cmte] = zip_dict
        ready_to_print_median = median.get_median()
        ready_to_print_num = median.get_num()
        ready_to_print_total = median.get_total()
        
    # print out info according to the median object
    out.write(f'{cmte}|{zip}|{ready_to_print_median}|{ready_to_print_num}|{ready_to_print_total}\n')


def median_by_date(dict_by_date, cmte, dt, amt):
    # get the transactions of this recipient
    date_dict = dict_by_date.get(cmte, None)

    # if already have transactions link to this recipient
    if date_dict:
        median = date_dict.get(dt, None)

        # if the transaction to this recipient at this date has already been stored
        if median:
            median.add_num(amt)
        else:
            # init a new median object to store the values
            median = Median()
            median.add_num(amt)
            date_dict[dt] = median
    else:
        # no transactions made at this date, then init a new dictionary for this date
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
            ready_to_print_median = median.get_median()
            ready_to_print_num = median.get_num()
            ready_to_print_total = median.get_total()
            out.write(f'{cmte}|{date}|{ready_to_print_median}|{ready_to_print_num}|{ready_to_print_total}\n')


def main():
    parser = argparse.ArgumentParser(description='input and output files')
    parser.add_argument("--infile", "-i", nargs=1, help="input file path")
    parser.add_argument("--zip", "-z", nargs=1, help="medianvals_by_zip file path")
    parser.add_argument("--date", "-d", nargs=1, help="medianvals_by_date file path")
    args = parser.parse_args()

    dict_by_zip = {}
    dict_by_date = {}
    with open(args.infile[0], 'r') as infile, open(args.zip[0], 'w') as out_by_zip, open(args.date[0], 'w') as out_by_date:
        for line in infile:
            if line.strip():
                data, other_valid, date_valid, zip_valid = process_data(line)
                cmte, zip, dt, amt = data
                if other_valid:
                    if zip_valid:
                        median_by_zip(dict_by_zip, cmte, zip, amt, out_by_zip)
                    if date_valid:
                        median_by_date(dict_by_date, cmte, dt, amt)
        print_median_by_date(dict_by_date, out_by_date)


if __name__ == '__main__':
    main()