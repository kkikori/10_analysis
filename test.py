import sys
from collections import Counter

def main():
    print(list(range(-3, 0)))
    k = [1,2,2,3,4]
    cc = Counter(k)
    print(cc)
    cc.update([1,5])
    print(cc)

if __name__ == "__main__":
    main()
