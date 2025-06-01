shopping_list=[]
print("Enter 'stop' when you are finished!")
print("What do you want to buy?")
while True:
    item=input()
    if item=='stop':
        break
    shopping_list.append(item)
print(f"You want to buy {shopping_list}")