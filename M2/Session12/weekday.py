from datetime import date

# It handles leap years.
d = date(2000, 2, 29)

weekday_names = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}

print(weekday_names[d.weekday()])

print(d.isoweekday())
