import calendar
Y=int(input("Enter the year:"))
M=int(input("Enter the month (1-12):"))
print("The calendar for the given month is:")
print(calendar.month(Y,M))
print(calendar.calendar(Y))