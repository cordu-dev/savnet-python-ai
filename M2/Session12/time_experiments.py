from datetime import date, datetime, timedelta
import time

# Number of seconds from 1970 (1st Jan)
timestamp = time.time()
print("Timestamp:", timestamp)

timestamp = 1572879180
print("CTIME: ", time.ctime(timestamp))

timestamp = 1572879180
print(time.gmtime(timestamp))
print(time.localtime(timestamp))

print("-" * 20)

d = date.fromtimestamp(timestamp)
print("Date:", d)

dt = datetime.fromtimestamp(timestamp)
print("Datetime:", dt)

anna_birthday = date.fromisoformat("1999-12-28")
print(anna_birthday)
print(anna_birthday.year)
print(anna_birthday.month)
print(anna_birthday.day)

# Bob birthday is after 12 days from Anna's bday
bob_birthday = anna_birthday + timedelta(days=12)
print(bob_birthday)

# Kat's bday is same day and month as Anna's, but differnt year
kat_birthday = anna_birthday.replace(year=2008)
print(kat_birthday)
