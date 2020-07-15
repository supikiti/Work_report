from glob import glob

month_data = sorted(glob("./TimeStamp/2020-07*"))
work_time = 0

for day_data in month_data:
    day = day_data.split("-")[2]
    with open(day_data, "r") as f:
        timestamp = f.readlines()[0].split()
    print("{}日, 勤務時間: {} ~ {}, 休憩: {} ~ {}".format(
                                day.split(".")[0],
                                timestamp[0],
                                timestamp[1],
                                timestamp[2],
                                timestamp[3]))