import pandas as pd
import json
import time
import vk

def fill_the_graph():
    file = open('message.json')
    data = json.load(file)
    df = pd.read_csv("data.csv").drop(columns="Unnamed: 0")
    vk_api = vk.API(vk.session)
    friends = data["friends"]
    ind = int(data["index"])
    start = ind
    token = data["access_token"]
    while ind < len(friends):
        try:
            friend = friends[ind]
            resp = vk_api.friends.get(access_token=token, user_id=friend, v=5.199)
            ind += 1
            info = vk_api.users.get(access_token=token, user_ids=[friend], v=5.199)[0]
            df.loc[df.shape[0]] = [friend, info["first_name"] + " " + info["last_name"], list(set(resp["items"]) & set(friends))]
            time.sleep(0.7)
        except vk.exceptions.VkAPIError:
            ind += 1

    df.to_csv("mutual.csv")
