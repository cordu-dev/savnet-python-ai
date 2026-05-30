from datetime import date, datetime, time, timedelta


def print_title(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def print_character(name, value):
    print(f"{name:<24} -> {value}")


print_title("THE TIME TRAVEL AGENCY")
print("Welcome, recruit.")
print("Today you will learn how Python handles calendar days, clock moments,")
print("and full time-travel coordinates.")


print_title("EXPERIMENT 1: THREE SUSPICIOUS CHARACTERS WALK INTO A PROGRAM")

mission_day = date(2035, 7, 28)
mission_alarm = time(6, 30, 15)
mission_datetime = datetime(2035, 7, 28, 6, 30, 15)

print_character("date", mission_day)
print_character("time", mission_alarm)
print_character("datetime", mission_datetime)

print()
print("date answers: What day on the calendar?")
print("time answers: What time on the clock?")
print("datetime answers: Which day AND what clock time?")


print_title("EXPERIMENT 2: INSPECT THE TIME MACHINE PARTS")

print("The calendar-only object has these parts:")
print_character("year", mission_day.year)
print_character("month", mission_day.month)
print_character("day", mission_day.day)

print()
print("The clock-only object has these parts:")
print_character("hour", mission_alarm.hour)
print_character("minute", mission_alarm.minute)
print_character("second", mission_alarm.second)

print()
print("The full datetime object has BOTH sets of parts:")
print_character("year", mission_datetime.year)
print_character("month", mission_datetime.month)
print_character("day", mission_datetime.day)
print_character("hour", mission_datetime.hour)
print_character("minute", mission_datetime.minute)
print_character("second", mission_datetime.second)


print_title("EXPERIMENT 3: THE ROBOT IS LATE")

arrival_time = datetime(2035, 7, 28, 6, 30)
robot_delay = timedelta(hours=2, minutes=45)
actual_arrival = arrival_time + robot_delay

print_character("Planned arrival", arrival_time)
print_character("Robot delay", robot_delay)
print_character("Actual arrival", actual_arrival)

print()
print("A datetime can move forward or backward using timedelta.")
print("Think of timedelta as a duration: 3 days, 2 hours, 10 minutes, etc.")


print_title("EXPERIMENT 4: THE PIZZA COUNTDOWN")

pizza_ordered_at = datetime(2035, 7, 28, 19, 15)
pizza_arrives_at = datetime(2035, 7, 28, 19, 52)
waiting_time = pizza_arrives_at - pizza_ordered_at

print_character("Pizza ordered", pizza_ordered_at)
print_character("Pizza arrives", pizza_arrives_at)
print_character("Waiting time", waiting_time)
print_character("Waiting seconds", waiting_time.total_seconds())

print()
print("Subtracting two datetime objects gives you a timedelta.")
print("This is how Python answers: How much time passed?")


print_title("EXPERIMENT 5: COMBINE DATE + TIME INTO ONE SUPER OBJECT")

dragon_meeting_day = date(2035, 10, 3)
dragon_meeting_time = time(22, 5)
dragon_meeting = datetime.combine(dragon_meeting_day, dragon_meeting_time)

print_character("Meeting day", dragon_meeting_day)
print_character("Meeting time", dragon_meeting_time)
print_character("Combined datetime", dragon_meeting)

print()
print("If date is the map and time is the clock, datetime is the full address.")


print_title("EXPERIMENT 6: SPLIT A DATETIME BACK INTO DATE AND TIME")

secret_party = datetime(2035, 12, 31, 23, 59, 59)

print_character("Secret party", secret_party)
print_character("Only the date", secret_party.date())
print_character("Only the time", secret_party.time())


print_title("EXPERIMENT 7: CHANGE ONE PIECE WITHOUT REBUILDING EVERYTHING")

boring_lunch = datetime(year=2035, month=5, day=10, hour=12, minute=0)
dramatic_lunch = boring_lunch.replace(hour=23, minute=59)

print_character("Boring lunch", boring_lunch)
print_character("Dramatic lunch", dramatic_lunch)

print()
print("replace() creates a changed copy.")
print("It does not mutate the original object.")


print_title("EXPERIMENT 8: ISO FORMAT, THE ROBOT-FRIENDLY LANGUAGE")

# message_from_robot_date = "2035-08-14"  # ISO 8601 for date
message_from_robot = "2035-08-14T09:45:30"  # ISO 8601 for datetime
decoded_message = datetime.fromisoformat(message_from_robot)

print_character("Robot message", message_from_robot)
print_character("Decoded datetime", decoded_message)
print_character("Back to text", decoded_message.isoformat())

print()
print("ISO format is a clean standard way to store and exchange date/time data.")


print_title("MINI CHALLENGES")
print("1. Change the mission date to your birthday.")
print("2. Add 100 days to today's date.")
print("3. Find how many days are left until New Year's Eve.")
print("4. Create a silly event using datetime.combine().")
print("5. Use replace() to turn a normal Monday into a dramatic midnight Monday.")


print_title("FINAL BOSS SUMMARY")
print("date      = calendar only: year, month, day")
print("time      = clock only: hour, minute, second, microsecond")
print("datetime  = date + time together")
print("timedelta = a duration used for time math")
print()
print("Congratulations, recruit. Your time machine did not explode.")
