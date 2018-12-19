import json
import requests


def _send(endpoint, type, data=None, token=None):
    uri = 'http://localhost:8081/' + endpoint
    data = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }
    if token:
        headers['Authorization'] = "Bearer " + token
    if type.lower() == 'get':
        return requests.get(uri, headers=headers).json()
    elif type.lower() == 'post':
        return requests.post(uri, data, headers=headers).json()
    else:
        raise ValueError("type '" + token + "' is not defined.")


def get_access_token(name, password):
    print("name", name)
    request_data = {
        'name': name,
        'password': password,
    }
    response = _send(endpoint='login', data=request_data, type='post')
    print(response)
    return response['token']


def load_thread(token, thread_i):
    en_p = "threads/" + str(thread_i)
    return _send(endpoint=en_p, token=token, type="get")


def load_threads(token):
    return _send(endpoint="threads", type="get", token=token)


def load_users(token):
    return _send(endpoint="users", type="get", token=token)


def load_user(token, ui):
    en_p = "users/" + str(ui)
    return _send(endpoint=en_p, token=token, type="get")


def create_post(token, data):
    _send(endpoint="posts", token=token, data=data, type="post")


def create_thread(token, data):
    _send(endpoint="threads", token=token, data=data, type="post")


def create_user(token, data):
    _send(endpoint="signup", token=token, data=data, type="post")


def updated_sentence(si, token, data):
    ens = "sentences/" + str(si)
    _send(endpoint=ens, token=token, data=data, type="post")


def get_thi_list(token):
    threads = load_threads(token)

    thi_list = []
    for thread in threads:
        thi_list.append(thread["id"])
    return thi_list


def get_threads_data(token):
    thi_list = get_thi_list(token)
    threads_data = []
    for th_i in thi_list:
        threads_data.append(load_thread(token, th_i))

    return threads_data
