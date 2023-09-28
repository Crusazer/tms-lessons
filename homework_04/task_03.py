i = 0
print(i)
i += 1

while i < 101:
    user_answer = input("Should we break?(yes/no): ")
    if user_answer == "no":
        break
    elif user_answer == "yes":
        print(i)
        i += 1
    else:
        print("Don't understand you!")
