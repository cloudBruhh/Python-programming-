p, t, r = map(float, input(
    "Enter principal, time, and rate separated by spaces:").split())
SI = (p * t * r) / 100
print(
    f"The simple interest of princinpal {p}, time {t} in years at rate {r} is {SI}")
