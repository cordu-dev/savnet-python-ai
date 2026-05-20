def fun():
    step = 0

    print("Step0")
    yield step
    step += 1

    print("Step1")
    yield step
    step += 1

    print("Step2")
    yield step


print(range(10))
print(fun())

for i in fun():
    print(i)
