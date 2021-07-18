# from datetime import datetime
# current_time = datetime.strftime(datetime.utcnow(),"%H:%M:%S") #output: 11:12:12
# mytime = "10:12:34"
# if current_time >  mytime:
#     print("Time has passed.")

time = '11:00'
splitted = time.split(':')
hrs = int(splitted[0])
min = int(splitted[1])
min_converted_to_decimal = min/60
print(hrs+min_converted_to_decimal)