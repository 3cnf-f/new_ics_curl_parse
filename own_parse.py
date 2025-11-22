import os
import sys
import pathlib

def read_ics_file(ics_file_path):
    with open(ics_file_path, 'r') as f:
        ics_data = f.read()
    return ics_data

def parse_ics_lines(ics_data):
    lines = ics_data.split('\n')
    print(lines)
    return lines

if __name__ == "__main__":
    ics_file_path = "ics2.ics"
    ics_data = read_ics_file(ics_file_path)
    lines = parse_ics_lines(ics_data)
