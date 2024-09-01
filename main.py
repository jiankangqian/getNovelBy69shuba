# import random
#
# data = [2,4,65,74,8]
# random.shuffle(data)
# print(data)
#
# result = random.choice(data)
# print(result)
# for i in range(10):
#     if i == 0:
#         print('    ',end='')
#         continue
#     print(i,end='\t')
#
# print("\n")
# for i in range(1,10):
#     print(i,end='\t')
#     for j in range(9):
#         print('+',end='\t')
#     print('\n')

# header = '    ' +'\t'.join([str(i) for i in range(1,10)])
# rows = ['\n'.join(['\t'.join(['+' for _ in range(9)])]) for _ in range(9)]
# print(header)
# print(rows)

# 首行
class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

person1 = Person("John",25)
person1.greet()
print(person1.name)

class Animal:
    def __init__(self,name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")

    @classmethod
    def water(self):
        print("I am a water.")

class Dog(Animal):
    def __init__(self,name,age):
        super().__init__(name)  # 调用父类的构造函数
        self.age = age
    def eat(self):
        print(f"{self.age}岁的{self.name} is eating.")
class Cat(Animal):
    pass

dog = Dog("Bob",18)
dog.eat()
cat = Cat("Jack")
cat.eat()
Animal.water()
