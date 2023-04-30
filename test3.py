from multiprocessing import Process, Manager
import pandas as pd


def worker(n):
    dataframe = pd.DataFrame()
    dataframe["bye"]=1
    print(n.do,"------------")


def print1(x):
    print(x.do,"**********")


if __name__ == '__main__':
    mgr = Manager()
    ns = mgr.Namespace()
    my_dataframe = pd.DataFrame()
    my_dataframe["hi"]=1
    ns.do = my_dataframe
    p = Process(target=worker, args=(ns, ))
    r = Process(target=print1, args=(ns,))
    r.start()
    p.start()
    r.join()
    p.join()
