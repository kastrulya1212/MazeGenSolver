class abc:
    pass

a1 = abc()
a2 = abc()
mas = [a1,a2]
mas.remove(a1)
print(mas)