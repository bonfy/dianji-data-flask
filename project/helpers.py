# coding:utf-8

import datetime
from decimal import Decimal
import json
__author__ = 'bonfy'

# result to json


def row_to_json(row):
    return {i: change_row_type(i,row) for i in row.keys()}


def change_row_type(i, row):
    if isinstance(row[i], datetime.datetime):
        return str(row[i])
    elif isinstance(row[i], Decimal):
        return float(row[i])
    return row[i]

