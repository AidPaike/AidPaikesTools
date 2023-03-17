def uncovered_if(var=True):
    if var:
        return False
    else:
        return True


def fully_covered():
    return True;


def uncovered():
    return True


class C:
    def __init__(self):
        self.a: str = "a"
        self.c = "b"

    def __post_init__(self):
        self.c = self.a


c1 = C()
# print(c1.a)
c1.a = "b"
# print(c1.a)
c2 = C()
# print(c2.a)
print(c2.c)
