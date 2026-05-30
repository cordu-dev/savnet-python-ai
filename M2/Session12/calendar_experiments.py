import calendar


print(calendar.weekheader(2))

calendar.setfirstweekday(calendar.TUESDAY)

calendar.prmonth(2020, 12)
print(calendar.weekday(2026, 5, 30))
