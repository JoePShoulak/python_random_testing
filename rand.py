import matplotlib.pyplot as plt
from random import randrange
from time import time
import sys, getopt
from os import mkdir

to_gen = []
save = False
quiet = False
plots = 1
ratio = 4
n_defined = False

def help(message=""):
    #print('rand: illegal option -- %s' % bad_arg.strip("-")[0])
    print
    if message != "":
        print(message)
    print('usage: rand [-hqs] [-p <plot count>] [-r <plot ratio>] [list of values ...]')
    print('\t-h | --help \t Show this message')
    print('\t-q | --quiet \t Do now show plots on screen')
    print('\t-s | --save \t Save the plots to the computer')
    print('\t-p | --plots \t Number of plots to be displayed (default=1, max=5)')
    print('\t-r | --ratio \t Ratio between plot data sizes (default=4)')
    print('\t-n | --n-size \t Number of data points in first graph (default=value for plot)')
    print

args = sys.argv[1:]
try:
    opts, args = getopt.getopt(args,"hqsp:r:n:", ["help", "quiet", "save", "plots=", "ratio=", "n-size="])
except getopt.GetoptError:
    help()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', "--help"):
        help()
        sys.exit()
    elif opt in ('-q', "--quiet"):
        quiet = True
    elif opt in ('-s', "--save"):
        save = True
    elif opt in ('-p', "--plots"):
        plots = int(arg)
        if plots not in [1, 2, 3, 4, 5]:
            help("rand: illegal argument -- plots=%d Maximum of 5 plots allowed" % plots)
            sys.exit(2)
    elif opt in ('-r', "--ratio"):
        if plots > 1:
            ratio = float(arg)
        else:
            help("rand: illegal argument -- ratio=%s Can't define ratio for one plot" % arg)
            sys.exit(2)
    elif opt in ('-n', "--n-size"):
        if float(arg) == int(arg) and int(arg) >= 1:
            n = int(arg)
            n_defined = True
        else:
            help("rand: illegal argument -- %s Size must be a positive integer" % arg)
            sys.exit(2)
if args == []:
    help()
    sys.exit(2)
    
for i in args:
    if float(i) != int(i) or int(i) <= 1:
        help("rand: illegal argument -- %s All values must be integers greater than 1" % " ".join(args))
        sys.exit(2)

for r in args:
    fig = plt.gcf()
    fig.set_size_inches(11,8.5)
    r = int(eval(r))
    f = plt.figure(1)
    my = 0
    all_plots =[]
    for p in range(plots):
        if n_defined:
            n = n*(ratio**p)
        else:
            n = r*(ratio**p)
        if plots != 0:
            new_plot = plt.subplot(plots*100 + 11 + p)
            all_plots += [new_plot]
        if p == 0:
            plt.title("Random values on [0, %d]" % (r-1))
        xs = []
        ys = []
        it = 0
        while it < n:
            start = time()
            xs += [randrange(r)]
            ys += [(time() - start)*1000000]
            it += 1

        plt.plot(xs, ys, "ro")
        if max(ys) > my:
            my = max(ys)
        plt.ylabel("Time (mu s)")
        plt.xlabel("Value")
    if all_plots != []:
        for p in all_plots:
            p.axis([-r*0.05,(r-1)*1.05,-my*0.05,my*1.05])
    else:
        plt.axis([-r*0.05,(r-1)*1.05,-my*0.05,my*1.05])
    f.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
    if save:
        try:
            plt.savefig("./data/r%d.png" % r)
        except:
            mkdir("data")
            plt.savefig("./data/r%d.png" % r)
    if not quiet:
        plt.show()
    plt.clf()
