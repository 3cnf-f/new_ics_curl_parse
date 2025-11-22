import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo # Standard in Python 3.9+
import re
import sys
import pathlib

def read_ics_file(ics_file_path):
    with open(ics_file_path, 'r') as f:
        ics_data = f.read()
    return ics_data

def get_events(ics_data):
    """
    returns a dict of dates=keys that have any events on them and each date
    with an event with a list,
    that list will contain all the events that have that date,
    if the date has no events there is no list object with that key
    20260227T063000Z

    """
    this_lines = ics_data.split('\n')
    date_dict={}
    for i,this_line in enumerate(this_lines):
        pass
        this_prop,this_value=check_type(this_line)
        if this_prop == "BEGIN" and this_value == "VEVENT":
            start_date=None
            date_object=None
            this_summary=None
            has_time=False
            
            for j, next_line in enumerate(this_lines[i:]):
                next_prop, next_value = check_type(next_line)
                if next_prop == "DTSTART":
                    if "VALUE" in next_value:
                        start_date=re.match(r"^VALUE=DATE:(.*)$",next_value).group(1)
                        date_object = datetime.strptime(start_date, "%Y%m%d")
                        has_time=False
                    else:
                        start_date=next_value[:8]
                        dt_utc = datetime.strptime(next_value, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
                        date_object = dt_utc.astimezone(ZoneInfo("Europe/Stockholm"))
                        has_time=True


                if next_prop == "SUMMARY":
                    this_summary=next_value


                if next_prop == "END" and next_value == "VEVENT":
                    if not start_date in list(date_dict.keys()):
                        date_dict[start_date]={}
                        date_dict[start_date]["event_list"]=[]


                    this_date_dict={}
                    this_date_dict["all_lines"]=this_lines[i+1:i+j]
                    this_date_dict["start_date"]=start_date
                    this_date_dict["datetime_object"]=date_object
                    this_date_dict["summary"]=this_summary
                    this_date_dict["has_time"]=has_time
                    date_dict[start_date]["event_list"].append(this_date_dict)
                    date_dict[start_date]["weekday"]=date_object.strftime("%A")
                    date_dict[start_date]["weeknumber"]=date_object.isocalendar()[1]
                    break

    return date_dict

def check_type(in_line):

    if ";" in in_line:
        resulto=re.match(r"^(.*)(;)(.*)$",in_line)
    elif "SUMMARY" in in_line:
        resulto=re.match(r"^(SUMMARY)(:)(.*)$",in_line)
        
    else:
        resulto=re.match(r"^(.*)(:)(.*)$",in_line)

    
    return resulto.group(1),resulto.group(3)

if __name__ == "__main__":
    ics_file_path = "ics2.ics"
    ics_data = read_ics_file(ics_file_path)
    calendar = get_events(ics_data)
    for date in calendar:
        print(date)
        print(calendar[date]["weekday"])
        print(calendar[date]["weeknumber"])
        for event in calendar[date]["event_list"]:
            print(f"  {event["summary"]=}")
            print(f"  {event["datetime_object"]=}")


        # print(line)
    # user hits enter to exit
