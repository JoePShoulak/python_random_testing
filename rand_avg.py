import matplotlib.pyplot as plt
from random import randrange
from time import time
import sys, getopt

r = 100
graph = False
n_defined = False

def help(message=""):
    #print('rand: illegal option -- %s' % bad_arg.strip("-")[0])
    print
    if message != "":
        print(message)
    print('usage: rand [hg] [-r <range max>] [-n <data size>]')
    print('  -h | --help    Display this message')
    print('  -g | --graph   Graph the data plots')
    print('  -r | --range   Range to generate values on [0, n-1] (default=100)')
    print('  -n | --n-size  Number of data points in first graph (default=<range max>)')
    print

args = sys.argv[1:]
try:
    opts, args = getopt.getopt(args,"hgr:n:", ["help", "graph", "range=", "n-size="])
except getopt.GetoptError:
    help()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', "--help"):
        help()
        sys.exit()
    elif opt in ('-g', 'graph'):
        graph = True
    elif opt in ('-r', '--range'):
        r = float(eval(arg))
        if r == int(r) and r >= 1:
            r = int(r)
        else:
            help("rand: invalid argument -- r=%f Must be a positive integer" % r)
    elif opt in ('-n', '--n-size'):
        n = float(arg)
        if int(n) == n and n >= 1:
            n = int(n)
            n_defined = True
        else:
            help("rand: invalid argument -- n=%f Must be a positive integer" % n)

if not n_defined:
    n = r
    
def my_random(n):
    return randrange(n) # Change this

i = 0
py_times = []
py_points = []
while i < n:
    start = time()
    py_points += [randrange(r)] # used for graphing
    py_times += [time()-start]
    i += 1
    
i = 0
my_times = []
my_points = []
while i < n:
    start = time()
    my_points += [my_random(r)] # used for graphing
    my_times += [time() - start]
    i += 1
    

print("Python algorithm total time: %f" % sum(py_times))
print("My algorithm total time:     %f" % sum(my_times))

if graph:
    f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=True)
    ax1.plot(py_points, py_times, "ro")
    ax1.set_title('Comparative Random Variable Generation Time')
    ax2.plot(my_points, my_times, "ro")
    f.subplots_adjust(hspace=0)
    plt.show()
