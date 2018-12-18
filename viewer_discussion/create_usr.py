from pathlib import Path
import simplejson as json
import viewer_discussion

f_usr = Path("/Users/ida/github/10_analysis/viewer_discussion/usrs.json")


def create_user_main(create_usr):
    buta_token = viewer_discussion.get_access_token("buta", "test")

    usr_tokens = {}
    f = f_usr.open("r")
    jsonData = json.load(f)
    for user in jsonData:
        if create_usr:
            viewer_discussion.create_user(buta_token, user)
        print(type(user["name"]),"user[password]", type(user["password"]))
        usr_tokens[user["name"]] = viewer_discussion.get_access_token(user["name"], user["password"])

    return usr_tokens
