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

def flatten_calendar_data(nested_data):
    """
    Converts the nested date-bucketed calendar dictionary into a flat list of event dictionaries.
    
    Args:
        nested_data (dict): The original dictionary with dates as keys.
        
    Returns:
        list: A list of dictionaries, where each dictionary is a single, self-contained event.
    """
    flat_events = []

    for date_key, bucket in nested_data.items():
        # Extract parent 'bucket' info (shared by all events on this day)
        week_number = bucket.get('weeknumber')
        weekday = bucket.get('weekday')

        for event in bucket.get('event_list', []):
            # 1. Base object with the parent info included
            flat_event = {
                'date_key': date_key,
                'weeknumber': week_number,
                'weekday': weekday,
                'summary': event.get('summary'),
                'start_time': event.get('datetime_object'),
                'has_time': event.get('has_time', False),
                'raw_lines': event.get('all_lines', [])
            }

            # 2. Extract specific fields buried in 'all_lines'
            # We iterate through lines to find UID and LOCATION
            uid = None
            location = None
            
            for line in flat_event['raw_lines']:
                if line.startswith('UID:'):
                    # Split only on the first colon to handle complex IDs
                    uid = line.split(':', 1)[1] 
                elif line.startswith('LOCATION:'):
                    location = line.split(':', 1)[1]

            flat_event['uid'] = uid
            flat_event['location'] = location

            # 3. Add to the master list
            flat_events.append(flat_event)

    return flat_events





        

if __name__ == "__main__":
    ics_file_path = "ics2.ics"
    ics_data = read_ics_file(ics_file_path)
    nested_calendar = get_events(ics_data)
    calendar = flatten_calendar_data(nested_calendar)
    pass
    pass
    calendar2=calendar
    pass
    for date in nested_calendar:
        print(date)
        print(f"{ nested_calendar[date]["weekday"]= }")
        print(f"{ nested_calendar[date]["weeknumber"]= }")
        for event in nested_calendar[date]["event_list"]:
            print(f"  {event["summary"]=}")
            print(f"  {event["datetime_object"]=}")


        # print(line)
    # user hits enter to exit
