from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


def print_title(title):
    print()
    print("=" * 74)
    print(title)
    print("=" * 74)


def print_passport(label, value):
    print(f"{label:<28} -> {value}")


print_title("THE INTERNATIONAL PANCAKE INCIDENT")
print("Welcome back, time recruit.")
print("Today our mission is dangerous: schedule breakfast across timezones.")
print("One wrong timezone and somebody gets pancakes at midnight.")


print_title("EXPERIMENT 1: DATE HAS NO PASSPORT")

meeting_day = date(2035, 3, 14)

print_passport("Meeting date", meeting_day)
print_passport("Date timezone", "No timezone")

print()
print("A date only knows the calendar day: year, month, day.")
print("It does not know if that day belongs to Bucharest, Tokyo, or Mars.")
print("Timezone belongs to moments in time, not plain calendar labels.")


print_title("EXPERIMENT 2: TIME CAN WEAR A TIMEZONE HAT")

bucharest_time = time(9, 30, tzinfo=ZoneInfo("Europe/Bucharest"))
tokyo_time = time(9, 30, tzinfo=ZoneInfo("Asia/Tokyo"))
utc_time = time(9, 30, tzinfo=timezone.utc)

print_passport("Bucharest clock time", bucharest_time)
print_passport("Tokyo clock time", tokyo_time)
print_passport("UTC clock time", utc_time)
print_passport("Bucharest tzinfo", bucharest_time.tzinfo)
print_passport("Tokyo tzinfo", tokyo_time.tzinfo)
print_passport("UTC tzinfo", utc_time.tzinfo)

print()
print("A timezone-aware time says: this clock reading belongs to this zone.")
print("But be careful: without a date, daylight saving rules can be tricky.")
print("The clock has a hat, but it still forgot what day it is.")


print_title("EXPERIMENT 3: DATETIME GETS A FULL PASSPORT")

bucharest_breakfast = datetime(
    year=2035,
    month=3,
    day=14,
    hour=9,
    minute=30,
    tzinfo=ZoneInfo("Europe/Bucharest"),
)

print_passport("Breakfast in Bucharest", bucharest_breakfast)
print_passport("Timezone name", bucharest_breakfast.tzinfo)
print_passport("UTC offset", bucharest_breakfast.utcoffset())

print()
print("A timezone-aware datetime knows the full mission:")
print("calendar date, clock time, and where on Earth the clock is located.")


print_title("EXPERIMENT 4: SAME MOMENT, DIFFERENT CLOCKS")

tokyo_breakfast = bucharest_breakfast.astimezone(ZoneInfo("Asia/Tokyo"))
new_york_breakfast = bucharest_breakfast.astimezone(ZoneInfo("America/New_York"))
utc_breakfast = bucharest_breakfast.astimezone(timezone.utc)

print_passport("Bucharest sees", bucharest_breakfast)
print_passport("Tokyo sees", tokyo_breakfast)
print_passport("New York sees", new_york_breakfast)
print_passport("UTC sees", utc_breakfast)

print()
print("Same real moment. Different wall clocks.")
print("Like watching the same movie with subtitles in different languages.")


print_title("EXPERIMENT 5: NAIVE VS AWARE DATETIME")

naive_datetime = datetime(2035, 3, 14, 9, 30)
aware_datetime = datetime(
    2035,
    3,
    14,
    9,
    30,
    tzinfo=ZoneInfo("Europe/Bucharest"),
)

print_passport("Naive datetime", naive_datetime)
print_passport("Naive tzinfo", naive_datetime.tzinfo)
print_passport("Aware datetime", aware_datetime)
print_passport("Aware tzinfo", aware_datetime.tzinfo)

print()
print("Naive datetime: I know the date and time, but not the country.")
print("Aware datetime: I know the date, time, and timezone.")
print("In serious applications, aware datetime is usually safer.")


print_title("EXPERIMENT 6: THE PANCAKE DELIVERY RACE")

delivery_start = datetime(
    year=2035,
    month=3,
    day=14,
    hour=9,
    minute=30,
    tzinfo=ZoneInfo("Europe/Bucharest"),
)

delivery_duration = timedelta(hours=5, minutes=45)
delivery_arrival = delivery_start + delivery_duration

print_passport("Pancakes leave", delivery_start)
print_passport("Travel duration", delivery_duration)
print_passport("Pancakes arrive", delivery_arrival)
print_passport("Arrival in UTC", delivery_arrival.astimezone(timezone.utc))

print()
print("You can still use timedelta with timezone-aware datetime objects.")
print("Python keeps the timezone information attached.")


print_title("EXPERIMENT 7: FIXED OFFSET VS REAL TIMEZONE")

fixed_plus_two = timezone(timedelta(hours=2))
fixed_offset_meeting = datetime(2035, 7, 1, 12, 0, tzinfo=fixed_plus_two)
real_bucharest_meeting = datetime(
    2035,
    7,
    1,
    12,
    0,
    tzinfo=ZoneInfo("Europe/Bucharest"),
)

print_passport("Fixed +02:00 meeting", fixed_offset_meeting)
print_passport("Real Bucharest meeting", real_bucharest_meeting)
print_passport("Fixed offset", fixed_offset_meeting.utcoffset())
print_passport("Bucharest offset", real_bucharest_meeting.utcoffset())

print()
print("timezone(timedelta(...)) creates a fixed offset.")
print("ZoneInfo('Europe/Bucharest') uses real timezone rules.")
print("Real zones can change because of daylight saving time.")


print_title("EXPERIMENT 8: THE SUMMER VS WINTER PLOT TWIST")

winter_bucharest = datetime(
    2035,
    1,
    15,
    12,
    0,
    tzinfo=ZoneInfo("Europe/Bucharest"),
)
summer_bucharest = datetime(
    2035,
    7,
    15,
    12,
    0,
    tzinfo=ZoneInfo("Europe/Bucharest"),
)

print_passport("Winter Bucharest", winter_bucharest)
print_passport("Winter UTC offset", winter_bucharest.utcoffset())
print_passport("Summer Bucharest", summer_bucharest)
print_passport("Summer UTC offset", summer_bucharest.utcoffset())

print()
print("Same city. Same clock time. Different UTC offset.")
print("That is why real timezone databases are useful.")


print_title("EXPERIMENT 9: ISO FORMAT WITH TIMEZONE")

robot_message = "2035-03-14T09:30:00+02:00"
decoded_robot_message = datetime.fromisoformat(robot_message)

print_passport("Robot message", robot_message)
print_passport("Decoded datetime", decoded_robot_message)
print_passport("Decoded tzinfo", decoded_robot_message.tzinfo)
print_passport("Back to text", decoded_robot_message.isoformat())

print()
print("The +02:00 part means: this time is 2 hours ahead of UTC.")
print("Timezone-aware ISO strings are excellent for saving exact moments.")


print_title("MINI CHALLENGES")
print("1. Create your birthday as a date. Does it have a timezone?")
print("2. Create 08:00 with timezone.utc as a time object.")
print("3. Create a datetime in Europe/Bucharest and convert it to Asia/Tokyo.")
print("4. Compare winter and summer offsets for your own city.")
print("5. Decode this ISO string: 2040-01-01T00:00:00+00:00")


print_title("FINAL BOSS SUMMARY")
print("date                 = calendar only, no timezone")
print("time with tzinfo     = clock time with a timezone label")
print("naive datetime       = date + time, but no timezone")
print("aware datetime       = date + time + timezone")
print("timezone.utc         = the global reference timezone")
print("ZoneInfo(...)        = real-world timezone rules")
print("astimezone(...)      = convert the same moment to another timezone")
print()
print("Congratulations. The pancakes arrived in the correct timezone.")
