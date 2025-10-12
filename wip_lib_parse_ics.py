import pathlib
import icalendar

ics_path=pathlib.Path("./ics.ics")
calendar = icalendar.Calendar.from_ical(ics_path.read_bytes())
for event in calendar.events:
    print(event.get("SUMMARY"),event.duration,event.start,event.end)
