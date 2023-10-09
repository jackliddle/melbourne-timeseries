# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 14:16:43 2023

@author: jackl
"""
from datetime import datetime

date_formats = ["%d %B %Y",
                "%d %b %Y",
                "%d-%b-%y",
                "%Y-%m-%d",
                "%d/%m/%Y"]

def parse_date(date_string, date_formats):
    for format in date_formats:
        try:
            parsed_date = datetime.strptime(date_string, format)
            return parsed_date
        except ValueError:
            pass
    raise ValueError(f"Unable to parse date from string: {date_string}")