i = 0
print(i)
i += 1

while i < 101:
    user_answer = input("Should we break?(yes/no): ")
    if user_answer == "no":
        print(i)
        i += 1
    elif user_answer == "yes":
        break
    else:
        print("Don't understand you!")
