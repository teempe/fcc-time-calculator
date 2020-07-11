def convert_to_minutes(time):
    hours, minutes = time.split(':')
    return int(hours) * 60 + int(minutes)


def get_day_of_week(start_day, duration_in_minutes):
    days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    start_day_index = days.index(start_day)
    
    days_passed = duration_in_minutes // 1440
    # round up number of days passed if necessary
    if days_passed != 0 and duration_in_minutes % 1440 != 0:
        days_passed += 1
    
    final_day_index = start_day_index + days_passed
    while final_day_index > len(days) - 1:
        final_day_index -= len(days)

    return days[final_day_index]


def add_time(start, duration, start_day=None):
    # 12:00 AM (0:00) of start time day is taken as reference point for calculations
    # This means that result time is in minutes passed from reference point
    #
    # 24-hour-clock: 00:00 ----- 12:00 ----- 24:00
    # 12-hour-clock: 12:00 AM -- 12:00 PM -- 12:00 AM
    # minutes:       0 --------- 720 ------- 1440
    #
    # For example:
    # 1:23 AM -> 83 minutes
    # 1:23 PM -> 83 + 720 = 803 minutes
    
    time, period = start.split() # time=hh:mm, period=AM or PM
    
    start_in_minutes = convert_to_minutes(time)
    if period == 'PM':
        start_in_minutes += 720    
        
    duration_in_minutes = convert_to_minutes(duration)
    
    result_in_minutes = start_in_minutes + duration_in_minutes
    result_hours = result_in_minutes // 60 - (result_in_minutes // 720 * 12)
    
    # In 12-hour-clock midnight is 12:00 AM
    if result_hours == 0:
        result_hours = 12

    result_minutes = result_in_minutes % 60

    # How many 12-hours periods passed from reference point
    if result_in_minutes // 720 % 2 == 0:
        result_cycle = 'AM'
    else:
        result_cycle = 'PM'

    # Format output
    new_time = f'{result_hours}:{result_minutes:02d} {result_cycle}'
    
    if start_day:
        result_day = get_day_of_week(start_day.lower(), duration_in_minutes)
        new_time += f', {result_day.capitalize()}'

    # How many 24-hours periods passed from reference point
    days = result_in_minutes // 1440
    if days > 1:
        new_time += f' ({days} days later)'
    
    if days == 1:
        new_time += f' (next day)'

    return new_time
