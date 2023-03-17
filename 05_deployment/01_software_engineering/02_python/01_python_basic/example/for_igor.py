class A:
    cl_1 = 5  # "static" in Java but "class valuable" in Python
    cl_2 = 5
    cl_3 = 7

    def __init__(self, v):
        self.a1 = v + self.__class__.cl_2
        self.a2 = v + A.cl_3

    def do_something_1(self):
        print(self.a1, self.a2)

    def do_something_2(my_own_name):
        print(my_own_name.a1, my_own_name.a2)

    def do_something_3(селф):
        print(селф.a1, селф.a2)

    @staticmethod  # decorator
    def do_static():
        print('staticmethod')

    @staticmethod
    def overload_init(b1, b2, b3):
        return A(b1 + b2 + b3)

    @classmethod
    def do_class(cls, a, b):
        print(cls.cl_1, a, b)


class B:
    bb = 1

    def __init__(self):
        self.b1 = 6
        b2 = 4


inst1 = A(1)
print(inst1.cl_1)
# inst1.cl_1 = inst1.cl_1 + 100
inst1.cl_1 = inst1.__class__.cl_1 + 100
print(inst1.cl_1, inst1.__class__.cl_1)

# ====================
inst1.my_1 = 666
print(inst1.my_1)

inst1.__class__.cl_my1 = 999
# A.cl_my1 = 999
print(inst1.__class__.cl_my1)

inst2 = A(2)
print(inst2.cl_my1)
print(inst2.__class__.cl_my1)

inst2.cl_my1 = 777
print(inst2.cl_my1)
print(inst2.__class__.cl_my1)

A.do_class(1, 2)

if __name__ == '__main__':
    print("MAIN!!!")

if __name__ == 'for_igor':
    print("I'm joking")

inst3 = A.overload_init(1, 2, 3)

# -----------------------------
inst4 = A(4)
print(inst4)
inst4.__class__ = B
print(inst4)
inst4.__class__()
# inst4.__init__()
print(inst4)

inst5 = inst1.__class__(777)
print(inst5)

# ------------------------
my_val = 5
print(my_val.__class__)
print(type(my_val))
