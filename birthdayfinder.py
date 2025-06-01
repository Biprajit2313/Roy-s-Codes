import datetime
date=input("Enter the date of birth in the format dd/mm/yyyy: ")
date=datetime.datetime.strptime(date,"%d/%m/%Y")
today=datetime.datetime.today()
age=today.year-date.year
if today.month<date.month:
    age-=1
print("Your age is",age)
print("Your Birthday felt in dates:")
for year in range(date.year,today.year+1):
    birthday=datetime.datetime(year,date.month,date.day)
    day=birthday.strftime("%A")
    print(f"{date.day}-{date.month}-{year} was a {day}")