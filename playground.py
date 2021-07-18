from datetime import datetime
current_time = datetime.strftime(datetime.utcnow(),"%H:%M:%S") #output: 11:12:12
mytime = "10:12:34"
if current_time >  mytime:
    print("Time has passed.")