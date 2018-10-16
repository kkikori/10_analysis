import numpy as np
from collections import Counter

def extract_list(n, datas):
    rl = []
    for kikan, qs in datas.items():
        d = np.array(qs)
        rl.extend(list(d[:,n]))
    return rl

def quote(header, datas):
    total_quo = []
    for i in range(-3, 0):
        print(header[i])
        quo=extract_list(i,datas)
        print(Counter(quo))
        total_quo.extend(quo)

    print()
    total_quo = Counter(total_quo)
    print(total_quo)
