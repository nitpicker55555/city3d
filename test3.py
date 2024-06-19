for hour in range(24):  # 循环从0到23小时
    for minute in range(0, 60, 15):  # 每小时的分钟数从0开始，以15为步长
        print(f'{hour:02}:{minute:02}')