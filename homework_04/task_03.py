i = 0
print(i)
i += 1

while i < 101:
    user_answer = input("Should we break?(yes/no): ")
    if "no" == user_answer:
        break
    elif "yes" == user_answer:
        print(i)
        i += 1
    else:
        print("Don't understand you!")
