import pandas as pd
import json
import os
import vk
import graphBuilder
import networkx as nx
from pyvis.network import Network


class Friends_analyzer:
    def __init__(self):
        self.access_token = "check out the README to get an instructions to generate your own access token"
        self.vk_api = vk.API(vk.session)
        self.file = open("data.txt", "w")
        self.G = nx.Graph()
        self.net = Network()
        self.id = self.vk_api.users.get(access_token=self.access_token, v=5.199)[0]["id"]
        self.friends = self.vk_api.friends.get(access_token=self.access_token, v=5.199)["items"]
        self.graph = pd.DataFrame()
        path = os.path.abspath(os.getcwd())
        if os.path.exists(path + "/mutual.csv"):
            self.__read_graph__()
        else:
            self.df = pd.DataFrame(columns=["VKid", "Name", "Friends"])
            self.df.to_csv("data.csv")
        with open('message.json', 'w', encoding='utf-8') as f:
            json.dump({"access_token": self.access_token,
                       "friends": self.friends,
                       "index": 0}, f, ensure_ascii=False, indent=4)

    def create_graph(self):
        graphBuilder.fill_the_graph()
        self.df.to_csv("database.csv")

    def __read_graph__(self):
        self.df = pd.read_csv("mutual.csv").drop(columns=["Unnamed: 0"])
        self.df["Friends"] = self.df["Friends"].apply(lambda x: self.__STR2LIST__(x))

    def __STR2LIST__(self, s):
        my_list = s.strip('][').split(', ')
        for i in range(len(my_list)):
            if my_list[i] != '':
                my_list[i] = int(my_list[i])
        return my_list

    def init_graph(self):
        self.__read_graph__()
        for name in self.df["Name"]:
            self.G.add_node(name)
        for elem in self.df.iterrows():
            i, row = elem
            for friendID in row["Friends"]:
                friend = self.df[self.df["VKid"] == friendID].loc[:, "Name"].values
                if friend.size != 0:
                    self.G.add_edge(row["Name"], friend[0])

    def draw_graph(self):
        self.init_graph()
        self.net.from_nx(self.G)
        self.net.show("nx.html", notebook=False)

    def find_path(self, name1, name2):
        if name1 not in list(self.df["Name"]):
            print(f"Error: No friend with name {name1}")
            return

        if name2 not in list(self.df["Name"]):
            print(f"Error: No friend with name {name2}")
            return

        if not nx.has_path(self.G, name1, name2):
            print(f"Error: No path between {name1} and {name2}")
            return

        path = nx.shortest_path(self.G, source=name1, target=name2)
        new_net = Network()
        new_net.from_nx(self.G.subgraph(path))
        new_net.show("my_path.html", notebook=False)

    def best_friends(self, num):
        data = []
        for elem in self.df.iterrows():
            i, row = elem
            data.append((row["Name"], len(row["Friends"])))
        data.sort(key=lambda x: x[1], reverse=True)
        for i in range(min(len(data), num)):
            print(f"{data[i][0]}. Number of mutual friends: {data[i][1]}")

TEXT = '''
If you want to draw a graph: press 1
If you want to find a path between 2 friends: press 2
If you want to know who your best friends are: press 3
If you want to stop the program: press 0
'''

FA = Friends_analyzer()
resp = -1
current_path = os.path.abspath(os.getcwd())

if not os.path.exists(current_path + "/mutual.csv"):
    print("Give us some time to build the graph...\n")
    FA.create_graph()
    FA.init_graph()

while resp != 0:
    resp = int(input(TEXT))
    if resp == 1:
        FA.draw_graph()
    if resp == 2:
        name1 = input("Enter first friend: ")
        name2 = input("Enter second friend: ")
        FA.init_graph()
        FA.find_path(name1, name2)
    if resp == 3:
        FA.best_friends(int(input("Enter the number of friends: ")))
