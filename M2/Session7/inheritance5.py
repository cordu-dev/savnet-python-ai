class Level1(object):
    class_var_1 = 100

    def __init__(self):
        self.instance_var_1 = 101

    def fun_1(self):
        return 102


class Level2(Level1):
    class_var_2 = 200

    def __init__(self):
        super().__init__()
        self.instance_var_2 = 201

    def fun_2(self):
        return 202


class Level3(Level2):
    class_var_3 = 300

    def __init__(self):
        super().__init__()
        self.instance_var_3 = 301

    def fun_3(self):
        return 302


obj = Level3()

print(obj.class_var_1, obj.instance_var_1, obj.fun_1())
print(obj.class_var_2, obj.instance_var_2, obj.fun_2())
print(obj.class_var_3, obj.instance_var_3, obj.fun_3())
