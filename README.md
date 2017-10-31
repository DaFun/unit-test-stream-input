# Find Political Donors

## Introduction

This project is mainly about distill useful information from the donations record file provided by the [Federal Election Commission](http://classic.fec.gov/finance/disclosure/ftpdet.shtml), 
and output the information to two different files: 
1. `medianvals_by_zip.txt` is collecting donation information by zip code: recording donation median and sum of a specific zip.
2. `medianvals_by_date.txt` is collecting donation information by date: recording donation median and sum of a date.

## Prerequisites

```
Anaconda (python 3.6)
```
## How to run
Before run it, save the itcont.txt into `input/` directory
```bash
./run.sh
```

### Unit Test

run unit test of median class:
```bash
python ./src/test_median.py
```

## Approach 

The hardest part of this project must be find median from the data stream.
In order to implement this function, I built a Median class, which has a min-heap and a max-heap.
The max-heap stores smaller half of data, meanwhile the min-heap stores the bigger half of the data.
Thus, the time complexity to find the median is O(1). 

The Median class also record the number of transactions and the sum of transactions, so outputting results is very convenient.  

## Authors 

* [DaFun](https://github.com/DaFun/)**(Fei Cheng)**
* [jlantos](https://github.com/jlantos)
* [emhoa](https://github.com/emhoa)

## Acknowledgments

**[InsightDataScience](https://github.com/InsightDataScience/)**