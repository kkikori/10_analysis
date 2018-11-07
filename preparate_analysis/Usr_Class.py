# ユーザクラス
class UserClass():
    def __init__(self, name):
        self.name = name
        self.pi_list = []
        self.previousQ_list = []

    #リストに追加の際，ソートをかける
    def add_pi_list(self,pi):
        self.pi_list.append(pi)
        self.pi_list = sorted(self.pi_list)