class creature():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print_a(self):
        print("aaa")

class herbivore(creature):
    def __init__(self, x, y):
        super().__init__(x,y)

    def print_b(self):
        self.x += 1
        print(self.x)


a = herbivore(1,1)

a.print_b()