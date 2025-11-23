import wip_lib_own_parse as lp
from datetime import datetime,timezone
import time

a_week_in_secs=604800

def get_today_weekday():
    today=datetime.fromtimestamp(time.time())
    in_a_week=datetime.fromtimestamp(time.time()+a_week_in_secs)
    in_2_weeks=datetime.fromtimestamp(time.time()+2*a_week_in_secs)
    return today.strftime("%A"),today,in_a_week,in_2_weeks

def decide_what_weeks_to_include():
    dayname_today,today,in_a_week,in_2_weeks=get_today_weekday()
    this_weeks=[]
    if dayname_today == "Sunday" or dayname_today == "Saturday":
        print("sunday or saturday")

        this_weeks.append(in_a_week.isocalendar()[1])
        this_weeks.append(in_2_weeks.isocalendar()[1])
    else:
        print("not sunday or saturday")
        this_weeks.append(today.isocalendar()[1])
        this_weeks.append(in_a_week.isocalendar()[1])
    return this_weeks

def timestamp_str_t_utc(timestamp_str):
    return datetime.strptime(timestamp_str, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)

if __name__ == "__main__":
    weeks_to_include=decide_what_weeks_to_include()
    flat_list_calendar=lp.flatten_calendar_data(lp.get_events(lp.read_ics_file("ics2.ics")))
    print(flat_list_calendar)
    this_update=[x for x in flat_list_calendar[0]['raw_lines'] if 'DTSTAMP' in x][0][8:]

    this_update_date_object = timestamp_str_t_utc(this_update)
    print(flat_list_calendar)
    print()
    print()




