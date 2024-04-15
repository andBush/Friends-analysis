import pandas as pd
import json
import graphBuilder
import networkx as nx
from pyvis.network import Network

class Friends_analyzer:
    def __init__(self, user_id="growalltime"):
        self.access_token = "YOUR ACCESS TOKEN WITH PERMISSION TO FRIENDS"
        self.vk_api = vk.API(vk.session)
        self.file = open("data.txt", "w")
        self.id = self.vk_api.users.get(access_token=self.access_token, user_ids=[user_id], v=5.199)[0]["id"]
        self.friends = self.vk_api.friends.get(access_token=self.access_token, user_id=self.id, v=5.199)["items"]
        self.graph = pd.DataFrame()
        self.df = pd.DataFrame(columns=["VKid", "Name", "Friends"])
        self.df.to_csv("data.csv")
        with open('message.json', 'w', encoding='utf-8') as f:
            json.dump({"access_token": self.access_token,
                       "friends": self.friends,
                       "index": 0}, f, ensure_ascii=False, indent=4)

    def create_graph(self):
        graphBuilder.fill_the_graph()

    def __read_graph__(self):
        self.df = pd.read_csv("mutual.csv").drop(columns=["Unnamed: 0"])
        self.df["Friends"] = self.df["Friends"].apply(lambda x: self.__STR2LIST__(x))

    def __STR2LIST__(self, s):
        my_list = s.strip('][').split(', ')
        for i in range(len(my_list)):
            if my_list[i] != '':
                my_list[i] = int(my_list[i])
        return my_list

    def draw_graph(self):
        self.__read_graph__()
        G = nx.Graph()
        net = Network()
        for name in self.df["Name"]:
            G.add_node(name)
        for elem in self.df.iterrows():
            i, row = elem
            for friendID in row["Friends"]:
                print("iter")
                friend = self.df[self.df["VKid"] == friendID].loc[:, "Name"].values
                if friend.size != 0:
                    G.add_edge(row["Name"], friend[0])
        print(G)
        net.from_nx(G)
        net.toggle_physics(False)
        net.show("nx.html", notebook=False)




FA = Friends_analyzer()
#FA.create_graph()
FA.draw_graph()
