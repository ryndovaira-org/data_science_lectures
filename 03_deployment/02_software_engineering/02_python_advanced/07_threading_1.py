import threading


def new():
    for x in range(6):
        print(f"Child {x} Thread Here!!")


t1 = threading.Thread(target=new)

t1.start()
t1.join()
print("Main Thread Here!!")
