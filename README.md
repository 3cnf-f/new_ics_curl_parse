# new_ics_curl_parse

## priciples
* parse well first
* decide on color coding and so on later or in other repo

# not all events have times, some only have dates
* check X-MICROSOFT-MSNCALENDAR-ALLDAYEVENT
* DTSTART;VALUE=DATE:20251027'

## not all events have locations
* all events have summary
* locations if existing , are always duplicate of summary

## days off
* check for summary = Semester, Jourkomp, Föräldraledig
    * they also seem to have a start and end time
* check for time?

## primärjour
* if primärjour then dont consider jourkomp
* when primärjour both location and summary = primärjour
* if jour check for starttime

## semester
* Semester\, P1
* Semester\, stafetta

