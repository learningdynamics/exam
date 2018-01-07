#! /usr/bin/python3


import numpy as np
import matplotlib.pyplot as plt
import argparse
import pickle
from glob import glob
from math import sqrt

parser = argparse.ArgumentParser(description='Plots. Tables.')
parser.add_argument('--files', dest='glob', type=str, default="./*.pickle",
                    help='the filename unix glob (default: "./*.pickle")')
parser.add_argument('--plot', dest='plot_name', type=str, default="part1_plot.png",
                    help='the filename of the plot (default: "part1_plot.png")')
parser.add_argument('--latex', dest='table_name', type=str, default="part1_table.tex",
                    help='the filename of the LaTeX table (default: "part1_table.tex")')

args = parser.parse_args()


todo = None
files = glob(args.glob)
for fn in files:
    with open(fn, 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        new_todo = pickle.load(f)
        if todo is None:
            todo = new_todo
            for i in range(len(new_todo)):
                todo[i]["moment"] = new_todo[i]["n_samples"]*(new_todo[i]["Rs"][-1]**2)
                todo[i]["Rs"] *= new_todo[i]["n_samples"]
        else:
            for i in range(len(new_todo)):
                n_samples = new_todo[i]["n_samples"]
                todo[i]["Rs"] +=  new_todo[i]["Rs"] * n_samples
                todo[i]["time"] +=  new_todo[i]["time"] * n_samples
                todo[i]["n_samples"] += n_samples
                todo[i]["moment"] += new_todo[i]["n_samples"]*(new_todo[i]["Rs"][-1]**2)


for t in todo:
    t["Rs"] /= t["n_samples"]
    t["time"] /= t["n_samples"]
    t["moment"] /= t["n_samples"]
    t["std"] = sqrt(t["moment"] - t["Rs"][-1]**2)
    t["SE"] = t["std"] / sqrt(t["n_samples"])


                
steps = len(todo[0]["Rs"])
    
print("Plotting")
index = [i for i in range(1, steps + 1)]
#plt.ylim(-10, 120)
for t in todo:
    plt.plot(index, t["Rs"])
plt.legend([t["name"] for t in todo])
plt.ylabel('R')
plt.savefig(args.plot_name)
# plt.show()


print("Saving LaTeX table")
row_format ="{:>10} & {:>15} & {:>15} & {:>16} & {:>15}\\\\\n"
with open(args.table_name, 'w') as f:
    f.write('\\begin{tabular}{lllrr}\n')
    f.write('\\toprule\n')
    f.write(row_format.format("Learner", "Avg \\# Partners", "Speed", "Solution Quality", "95\\% Conf. Interval"))
    f.write('\\midrule\n')
    for t in todo:
        f.write( row_format.format(t["name"],
                                   "${}$".format(t["partners"]),
                                   "$\\times {:.1f}$".format(todo[-1]["time"] / t["time"]),
                                   "${:.1f}$\\%".format(t["Rs"][-1]/todo[-1]["Rs"][-1] * 100),
                                   "$\pm{:.2f}$".format(1.96 * t["SE"]) ))
    f.write('\\bottomrule\n')
    f.write("\\end{tabular}\n")
