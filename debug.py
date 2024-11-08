import random

class Test:
    def __init__(self, mass, heigth):
        self.mass = mass
        self.height = heigth
    def update(self):
        self.__init__(50,7.5)

a1 = Test(100, 15)
a1.update()
print(a1.mass, a1.height)

a = [1,2,3]
a.pop(-1)
print(a)