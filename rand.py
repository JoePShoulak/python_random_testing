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
    print
    if message != "":
        print(message)
    print('usage: rand [-hqs] [-p <plot count>] [-r <plot ratio>] [-n <data size>] [list of ranges maxs...]')
    print('  -h | --help    Show this message')
    print('  -q | --quiet   Do now show plots on screen')
    print('  -s | --save    Save the plots to the computer')
    print('  -p | --plots   Number of plots to be displayed (default=1, min=1, max=5)')
    print('  -r | --ratio   Ratio between plot data sizes (default=4)')
    print('  -n | --n-size  Number of data points in first graph (default=range max, min=1)')
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
        if arg not in ["1", "2", "3", "4", "5"]:
            help("rand: illegal argument -- plots=%s Must be an integer 1<=plots<=5" % arg)
            sys.exit(2)
        plots = int(arg)    
    elif opt in ('-r', "--ratio"):
        if plots > 1:
            ratio = float(arg)
            if ratio <= 0:
                help("rand: illegal argument --ratio=%f Ratio must be positive")
                sys.exit(2)
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
    i = eval(i)
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
            xs += [randrange(r)] # <========= THIS BAD BOY RIGHT HERE
            ys += [(time() - start)*1000000]
            it += 1
        plt.plot(xs, ys, "ro")
        if max(ys) > my:
            my = max(ys)
        plt.ylabel("Time (mu s)")
        plt.xlabel("Value")
    for p in all_plots:
        p.axis([-r*0.05,(r-1)*1.05,-my*0.05,my*1.05])
    f.subplots_adjust(hspace=0)
    if save:
        try:
            plt.savefig("./data/r%ds%d.png" % (r, plots))
        except:
            mkdir("data")
            plt.savefig("./data/r%ds%d.png" % (r, plots))
    if not quiet:
        plt.show()
    plt.clf()
