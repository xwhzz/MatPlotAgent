"""
Gamma Process

Generate a gamma process with a given coefficient of variation and arrival rate.
"""
import argparse
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

current_file_path = Path(__file__).resolve()

parser = argparse.ArgumentParser()
parser.add_argument('--cv', type=float, default=2)
parser.add_argument('--arr', type=float, default=2)
parser.add_argument('--num_steps', type=int, default=100)
parser.add_argument('--seed', type=int, default=0)
parser.add_argument('--output', type=str, default='benchmark') 
args = parser.parse_args()

np.random.seed(args.seed)

arriving_rate = 1 / args.arr
cv = args.cv
num_steps = args.num_steps
output_dir = current_file_path.parent.parent / args.output

shape = 1 / cv**2
scale = cv**2 / arriving_rate

increments = np.random.gamma(shape, scale, num_steps)

gamma_process = np.cumsum(increments)

req_id = list(np.random.permutation(np.arange(1,101))) # array(remain)))
with open(output_dir /f'gamma_process_{args.arr}_{cv}.py', 'w') as f:
    f.write("time_point = "+ str(list(gamma_process))+ "\n"+"req_id = "+ str(req_id))

plt.eventplot(gamma_process, orientation='horizontal', colors='blue', linelengths=0.8)
plt.yticks([])  # Remove y-axis labels
plt.xlabel("Cumulative Time")
plt.title("Gamma Process Time Points")

plt.savefig(output_dir / f'gamma_process_{arriving_rate}_{cv}.png')