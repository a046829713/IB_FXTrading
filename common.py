import datetime
import pytz







def change_to_taiwan_time_zone(source_time: str) ->str:
    # Split the input string to get the datetime part and the timezone part
    datetime_str, tz_str = source_time.rsplit(' ', 1)

    # Assert that the timezone is 'US/Eastern'
    assert tz_str == 'US/Eastern', f"Timezone must be US/Eastern, got {tz_str}"

    # Define the source and target timezones
    source_tz = pytz.timezone('US/Eastern')
    target_tz = pytz.timezone('Asia/Taipei')

    # Convert the string to a datetime object with the source timezone
    datetime_obj = source_tz.localize(datetime.datetime.strptime(datetime_str, '%Y%m%d %H:%M:%S'))    
    converted_datetime_obj = datetime_obj.astimezone(target_tz)

    # Return the converted datetime as a string without timezone information
    return converted_datetime_obj.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')


def generate_range_day(durationStr: str, begin_time: str):
    assert durationStr[-1] == 'D', "This type not code in this function"
    
    # time_len
    time_len = int(durationStr.split(' ')[0])

    # 設置時區
    # 由於IB 他是此用向前回補 所以begin_time 在IB裡面當做回補時間
    begin_time = datetime.datetime.strptime(begin_time, '%Y%m%d %H:%M:%S')        
    end_time = datetime.datetime.now()  # 預設已經為台北時間

    # 每兩天產生一個日期範圍
    current_date = begin_time    
    date_ranges = []
    while current_date <= end_time:
        date_ranges.append(current_date.strftime("%Y%m%d %H:%M:%S") +' Asia/Taipei')
        current_date += datetime.timedelta(days=time_len)
    # 如果有超過也加進來
    date_ranges.append(current_date.strftime("%Y%m%d %H:%M:%S") +' Asia/Taipei')
    return date_ranges