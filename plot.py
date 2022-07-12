import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import datetime
import os
import numpy as np
import time

def plot_PR(P_list, R_list, k_list):
    x = list(R_list)
    x.reverse()
    y = list(P_list)
    y.reverse()
    w = list(k_list)
    w.reverse()
    font={
        'family':'Times new roman',
        'weight':'normal',
        'color':'black',
        'size':'12',
        }
    #P-R curves
    fg = plt.figure()
    ax = fg.add_subplot(1,1,1)
    
    ax.set_xlabel('Recall', fontdict=font)
    ax.set_ylabel('Precision', fontdict=font)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.xticks(fontproperties='Times New Roman', size=12)
    plt.yticks(fontproperties='Times New Roman', size=12)
    #ax.set_title('P-R curve', fontdict=font)
    ax.plot(x, y)
    
    fig_dir = './curves/'
    fig_name = 'P-R_curve_' + datetime.datetime.now().strftime('%H_%M_%S_%f')
    plt.savefig(fig_dir+fig_name+'.eps')
    
    #P/R curves
    PR_q = list(np.array(y)/np.array(x))
    fg2 = plt.figure()
    ax2 = fg2.add_subplot(1,1,1)
    ax2.set_xlabel('w', fontdict=font)
    ax2.set_ylabel('P/R', fontdict=font)
    for i,rate in enumerate(PR_q) :
        if rate > 1 :
            y1 = PR_q[i-1]
            y2 = rate
            x1 = w[i-1]
            x2 = w[i]
            k = (y2-y1)/(x2-x1)
            b = y2 - k * x2
            x_cross = (1-b)/k
            break
    try:
        plt.scatter(x_cross, 1, color='r')
    except UnboundLocalError:
        print('No BEP found.')
    else:
        plt.plot([x_cross, x_cross], [1,0], "y--")
    #Truncate P/R curve
    margin =5
    w = w [:i+margin]
    PR_q = PR_q[:i+margin]
    ax2.plot(w, PR_q)
    ax2.plot(w, [1]*len(w), linestyle='--')

    fig_name = 'w_' + datetime.datetime.now().strftime('%H_%M_%S_%f')
    plt.savefig(fig_dir+fig_name+'.eps')

if __name__ == '__main__':
    log_path = './log/'
    log_list = os.listdir(log_path)
    for log in log_list:
        data = np.loadtxt(log_path + log, dtype=float, delimiter='\t')
        k = data[0]
        P = data[1]
        R = data[2]
        plot_PR(P, R, k)
        print(log + 'has been plotted.')
