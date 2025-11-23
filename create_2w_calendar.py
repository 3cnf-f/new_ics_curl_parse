import wip_lib_own_parse as lp
import wip_download_ics as wdi
from datetime import datetime,timezone
import time

a_week_in_secs=604800
thirty_mins_in_secs=1800

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

def get_cal_w_update():
    flat_list_calendar=lp.get_flat_list("ics2.ics")
    tud_epoch,tud_dateobject = lp.get_datestamp(flat_list_calendar)
    todate = datetime.fromtimestamp(time.time())
    to_epoch = todate.timestamp()
    iiii= abs(to_epoch - tud_epoch) 
    if iiii > thirty_mins_in_secs:
        print("need to update")
        status_dl=wdi.dl_ics()
        if status_dl == "downloaded":
            print("downloaded")

            flat_list_calendar=lp.get_flat_list("ics2.ics")
        else:
            print(f"error downloading {status_dl}")
            exit()
    else:
        print("no need to update")
    
    return flat_list_calendar

def day_w_stuff_in_week(in_weeks_to_include,in_list_cal):
    unq_days_list=[]
    for get_week in weeks_to_include:
        thislist=[(x['start_time'].strftime("%d%m%y"),x['summary']) for x in in_list_cal if x['weeknumber'] == get_week]
        d_in_this_list=[x[0] for x in thislist]
        set_d_in_list=set(d_in_this_list)
        sorted_list_of_set=list(set_d_in_list)
        sorted_list_of_set.sort()
        unq_days_list.append({get_week:sorted_list_of_set})
    return unq_days_list

def make_paragraphs(list_of_w_n_days,in_list_cal):
    for this_week in list_of_w_n_days:
        
        iter_week=list(this_week.keys())[0]
        print(f"week {iter_week}")

        iter_dates=list(this_week.values())[0]
        for this_it_date in iter_dates:
            this_date_w_events=[x for x in in_list_cal if x['start_time'].strftime("%d%m%y") == this_it_date]
            print(this_date_w_events[0]['start_time'].strftime("%A %d/%b"))
            summaries=[(x['summary'],x['start_time'].strftime("%H:%M")) for x in this_date_w_events]
            for sss in summaries:
                out_str=f" - {sss[0]}"
                if 'primärjour' in sss[0].lower():
                    out_str=f" - {sss[0]} {sss[1]}"
                print(out_str)





if __name__ == "__main__":
    weeks_to_include=decide_what_weeks_to_include()
    list_cal=get_cal_w_update()
    list_of_w_n_days=day_w_stuff_in_week(weeks_to_include,list_cal)
    make_paragraphs(list_of_w_n_days,list_cal)







