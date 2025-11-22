import pathlib
import icalendar
# add libraries for time zone correction
# convert times to utc Europe/Stockholm also respecting daylight saving datetime

from datetime import datetime
import pytz

# Define the target timezone
target_tz = pytz.timezone('Europe/Stockholm')

# --- Function to convert and format time ---
def fix_timezone(event_start):
    """
    Converts a datetime object (from icalendar) to Europe/Stockholm 
    and formats it as 'hh:mm'.
    
    Args:
        event_start (datetime): The event's start time (event.start).
        
    Returns:
        str: The formatted time string, e.g., '14:30'.
    """
    # 1. Handle naive datetime objects (assuming they represent UTC or 
    #    the original timezone from the ical file, often UTC if unspecified).
    #    If the ical file's times are consistently in a known timezone (e.g., UTC), 
    #    make it explicitly aware first. 
    #    For robust parsing, it's best to check the event's original VTIMEZONE 
    #    or assume UTC if it's naive, as is common practice.
    if event_start.tzinfo is None or event_start.tzinfo.utcoffset(event_start) is None:
        # Assuming naive datetime objects from icalendar are in UTC 
        # (common behavior if timezone is not specified in the iCal data).
        utc = pytz.utc
        aware_start = utc.localize(event_start)
    else:
        # It's already timezone-aware, no localization needed, just conversion
        aware_start = event_start

    # 2. Convert to the target timezone (Europe/Stockholm)
    stockholm_time = aware_start.astimezone(target_tz)
    
    # 3. Format as 'hh:mm' (24-hour format)
    return {'date':stockholm_time.strftime('%Y-%m-%d'), 'time':stockholm_time.strftime('%H:%M'), 'datetime':stockholm_time, 'weeknumber':stockholm_time.isocalendar()[1], 'weekday':stockholm_time.isocalendar()[2]}

test_time = datetime(2023, 9, 1, 14, 30, tzinfo=pytz.UTC)
print(fix_timezone(test_time)['weeknumber'])


ics_path=pathlib.Path("./ics.ics")
calendar = icalendar.Calendar.from_ical(ics_path.read_bytes())
for event in calendar.events:
#converted times:
    print(event)
    fixed_start=fix_timezone(event.start)
    fixed_end=fix_timezone(event.end)

    #print(event.get("SUMMARY"),event.duration,event.start,event.end)
    print(f"\n\n{event.get('SUMMARY')=}\n {event.duration=}\n {event.start=}\n {fixed_start['date']}\n w={fixed_start['weeknumber']}\n wd={fixed_start['weekday']} \n {fixed_start['time']=}\n {event.end=} ")
    user_input=input("press enter to continue")
