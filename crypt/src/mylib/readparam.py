import json


import json

class MyData:
    def __init__(self, json_file):
        self.load_from_file(json_file)

    def load_from_file(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        if "param1" in data:
            self.param1 = data["param1"]
        else:
            self.param1 = None

        if "param2" in data:
            param2_data = data["param2"]
            if "A" in param2_data:
                self.param2_A = param2_data["A"]
            else:
                self.param2_A = None

            if "B" in param2_data:
                self.param2_B = param2_data["B"]
            else:
                self.param2_B = None

        else:
            self.param2_A = None
            self.param2_B = None





        if "param3" in data:
            self.param3 = data["param3"]
        else:
            self.param3 = None


    def display_param1(self):
        if self.param1:
            print("param1:")
            for row in self.param1:
                print(row)
        else:
            print("param1 not found")

    def display_param2_A(self):
        if self.param2_A:
            print("param2 -> A:")
            print(self.param2_A)
        else:
            print("param2 -> A not found")

    def display_param2_B(self):
        if self.param2_B:
            print("param2 -> B:")
            print(self.param2_B)
        else:
            print("param2 -> B not found")

    def display_param3(self):
        if self.param3:
            print("param3:")
            print(self.param3)
        else:
            print("param3 not found")




if __name__ == "__main__":

    # JSONデータを読み込んでクラスのインスタンスを作成
    my_data = MyData('data/param.json')

    # データの表示
    my_data.display_param1()
    my_data.display_param2_A()
    my_data.display_param2_B()
    my_data.display_param3()

    print(my_data.param2_B)
