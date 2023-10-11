x = int(input("x = "))
y = int(input("y = "))
z = int(input("z = "))

if x > y:
    if x > z:
        print(x)
    else:
        print(z)
else:
    if y > z:
        print(y)
    else:
        print(z)
