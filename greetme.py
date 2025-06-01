import time
gettime=time.strftime("%H:%M:%S")
print(f"The current time is {gettime}")
c=int(gettime[0:2])
name=input("Enter your name: ")
if c>=0 and c<12:
    print(f"Good Morning {name}")
elif c>=12 and c<18:
    print(f"Good Afternoon {name}")
else:
    print(f"Good Evening {name}")