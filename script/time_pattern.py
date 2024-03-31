"""
Gamma Process

Generate a gamma process with a given coefficient of variation and arrival rate.
"""
import argparse
import numpy as np
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--cv', type=float, default=0.5)
parser.add_argument('--arriving_rate', type=float, default=5)
parser.add_argument('--num_steps', type=int, default=100)
parser.add_argument('--seed', type=int, default=0)
args = parser.parse_args()
np.manual_seed(args.seed)

arriving_rate = args.arriving_rate
cv = args.cv
num_steps = args.num_steps

shape = 1 / cv**2
scale = cv**2 / arriving_rate

increments = np.random.gamma(shape, scale, num_steps)

gamma_process = np.cumsum(increments)

with open(f'gamma_process_{arriving_rate}_{cv}.py', 'w') as f:
    f.write("time_point = "+ str(list(gamma_process)))

plt.eventplot(gamma_process, orientation='horizontal', colors='blue', linelengths=0.8)
plt.yticks([])  # Remove y-axis labels
plt.xlabel("Cumulative Time")
plt.title("Gamma Process Time Points")

plt.savefig(f'gamma_process_{arriving_rate}_{cv}.png')