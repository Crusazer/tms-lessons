seconds = int(input("Введите время в секундах: "))
days = seconds // (24 * 3600)
seconds %= 24 * 3600

hours = seconds // 3600
seconds %= 3600

minutes = seconds / 60
sec = seconds % 60

print(f"{days}:{hours}:{minutes}:{sec}")
