from datetime import datetime
import os
import csv
now = datetime.now()

formatted_date = now.strftime("%m%d%y")

print(formatted_date)

def is_date_greater(date1_str, date2_str):
    # Convert the date strings to datetime objects
    date1 = datetime.strptime(date1_str, "%m%d%y")
    date2 = datetime.strptime(date2_str, "%m%d%y")
    
    # Compare the dates
    return date2 > date1

# Example usage
date1 = "080824"
date2 = "080924"

a = [1,2,3,4]
print([-1])

