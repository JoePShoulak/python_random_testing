import matplotlib.pyplot as plt
from random import randrange
from time import time
import sys, getopt
from os import mkdir

to_gen = []
save = False
quiet = False

def help(bad_arg=""):
    if bad_arg != "":
        print('rand: illegal option -- %s' % bad_arg.strip("-")[0])
    print('usage: rand [-hqs] [list of values ...]')
    print('\t-h | --help \t Show this message')
    print('\t-q | --quiet \t Do now show plots on screen')
    print('\t-s | --save \t Save the plots to the computer')

args = sys.argv[1:]
try:
    opts, args = getopt.getopt(args,"hqs", ["help", "quiet", "save"])
except getopt.GetoptError:
    if args != []:
        help(args[0])
    else:
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
if args == []:
    help()
    sys.exit(2)

for r in args:
    fig = plt.gcf()
    fig.set_size_inches(11,8.5)
    r = int(r)
    f = plt.figure(1)
    my = 0
    for p in range(3):
        n = r*(4**p)
        plt.subplot(311 + p)
        if p == 0:
            plt.title("Random values on [0, %d]" % (r-1))
        xs = []
        ys = []
        for i in range(n):
            start = time()
            xs += [randrange(r)]
            ys += [(time() - start)*1000000]

        plt.plot(xs, ys, "ro")
        if max(ys) > my:
            my = max(ys)
        plt.ylabel("Time (mu s)")
        plt.xlabel("Value")
    for p in (plt.subplot(311), plt.subplot(312), plt.subplot(313)):
        p.axis([0,r,0,my])
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
