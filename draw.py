import json
import os.path

import numpy as np
import matplotlib.pyplot as plt

def read_file(path):
    with open(path, 'r') as a:
        data_str=a.read()
    data=json.loads(data_str)
    return data


def read_data(data):
    len=[]
    time=[]
    for i in data:
        len.append(data[i]['len'])
        time.append(data[i]['time'])

    avg_len=float(np.mean(len))
    avg_time=float(np.mean(time))
    return len, time, avg_len, avg_time


def draw(data, avg_data, name=""):
    plt.figure(figsize=(8, 5))
    line1, = plt.plot(data, color='red')
    line2, = plt.plot([avg_data for i in data], color='blue')
    plt.xlabel('Test Time')
    plt.ylabel('Round')
    plt.title('Round of killer bull')
    plt.legend(handles=[line1, line2],
               labels=['Round', 'Average round'],
               loc='best')
    plt.savefig('D:\\git_project\\cs520_final\\picture\\killer_bull_rounds.jpg')
    plt.show()


if __name__ == '__main__':
    current_path=os.path.dirname(os.path.abspath("__file__"))
    # file_name=os.path.join(current_path, "data_shy_bull.json")
    file_name = os.path.join(current_path, "data_killer_bull_25.json")
    data=read_file(file_name)
    a,b,c,d=read_data(data)
    # draw(a,c)
