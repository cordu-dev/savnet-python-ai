from datetime import datetime

date_str = "2019.11.04 14:53:00"

dt = datetime.strptime(date_str, "%Y.%m.%d %H:%M:%S")

print(dt.isoformat())
