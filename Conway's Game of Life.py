import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec

patterns = {
    'Block': np.array([[1, 1], [1, 1]]),
    'Beehive': np.array([[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]]),
    'Loaf': np.array([[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]]),
    'Boat': np.array([[1, 1, 0], [1, 0, 1], [0, 1, 0]]),
    'Tub': np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]),
    'Blinker': np.array([[1, 1, 1]]),
    'Toad': np.array([[0, 1, 1, 1], [1, 1, 1, 0]]),
    'Beacon': np.array([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]),
    'Pulsar': np.array([
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0]
    ]),
    'Glider': np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]]),
    'LWSS': np.array([[0, 1, 1, 1, 1], [1, 0, 0, 0, 1], [0, 0, 0, 0, 1], [1, 0, 0, 1, 0]]),
    'MWSS': np.array([[0, 1, 1, 1, 1, 0], [1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0]]),
    'HWSS': np.array([[0, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0]]),
    'Diehard': np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0]]),
    'Acorn': np.array([[0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0, 0], [1, 1, 0, 0, 1, 1, 1]]),
    'Pentadecathlon': np.array([
        [0,1,1,0,0,1,1,0],
        [1,1,1,1,1,1,1,1],
        [0,1,1,0,0,1,1,0],
    ]),
}

def generate_variants(pattern):
    variants = []
    for k in range(4):
        rotated = np.rot90(pattern, k)
        variants.append(rotated)
        variants.append(np.fliplr(rotated))
        variants.append(np.flipud(rotated))
    unique = []
    for v in variants:
        if not any(np.array_equal(v, u) for u in unique):
            unique.append(v)
    return unique

pattern_variants = {k: generate_variants(v) for k, v in patterns.items()}

def count_pattern(grid, pname):
    variants = pattern_variants[pname]
    n = grid.shape[0]
    count = 0
    for pat in variants:
        ph, pw = pat.shape
        for i in range(n - ph + 1):
            for j in range(n - pw + 1):
                if np.array_equal(grid[i:i+ph, j:j+pw], pat):
                    count += 1
    return count

def init_board(size):
    return np.random.choice([0, 1], size * size, p=[0.7, 0.3]).reshape(size, size)

def count_neighbors(grid, x, y):
    n = grid.shape[0]
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return sum(grid[(x + dx) % n, (y + dy) % n] for dx, dy in neighbors)

def update_board(grid):
    n = grid.shape[0]
    new_grid = np.zeros((n, n), dtype=int)
    for x in range(n):
        for y in range(n):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y]:
                new_grid[x, y] = neighbors in [2, 3]
            else:
                new_grid[x, y] = neighbors == 3
    return new_grid

size = 50
steps = 100
grid = init_board(size)
pattern_history = {k: [] for k in patterns.keys()}

fig = plt.figure(figsize=(20, 14))
gs = GridSpec(4, 7, figure=fig, wspace=0.4, hspace=1.1)

left_axes = [fig.add_subplot(gs[i, 0]) for i in range(4)] + [fig.add_subplot(gs[i, 1]) for i in range(4)]
right_axes = [fig.add_subplot(gs[i, 5]) for i in range(4)] + [fig.add_subplot(gs[i, 6]) for i in range(4)]
pattern_axes = (left_axes + right_axes)[:len(patterns)]

sim_ax = fig.add_subplot(gs[0:3, 2:5])
im = sim_ax.imshow(grid, cmap='binary')
sim_ax.set_title("Conway's Game of Life")
sim_ax.axis('off')

bar_ax = fig.add_subplot(gs[3, 2:5])

colors = plt.cm.tab20(np.linspace(0, 1, len(patterns)))
lines = {}

for idx, (pname, ax) in enumerate(zip(patterns.keys(), pattern_axes)):
    line, = ax.plot([], [], label=pname, color=colors[idx])
    ax.set_xlim(0, steps)
    ax.set_ylim(0, size // 2)
    ax.set_title(pname, fontsize=10)
    ax.set_xlabel('Step', fontsize=9)
    ax.set_ylabel('Count', fontsize=9)
    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.legend(fontsize=7, loc='upper right')
    lines[pname] = line

bar_ax.set_title('Cumulative Pattern Counts', fontsize=12)
bar_ax.tick_params(axis='x', rotation=45, labelsize=9)
bar_ax.set_ylabel('Count', fontsize=10)

def update(frame):
    global grid
    grid = update_board(grid)
    for pname in patterns.keys():
        pattern_history[pname].append(count_pattern(grid, pname))
    im.set_array(grid)
    for pname, line in lines.items():
        line.set_data(range(len(pattern_history[pname])), pattern_history[pname])
        ax = line.axes
        max_y = max(pattern_history[pname]) if pattern_history[pname] else 1
        ax.set_ylim(0, max(max_y, 1))
    bar_ax.clear()
    cumulative_counts = [sum(pattern_history[name]) for name in patterns.keys()]
    bar_ax.bar(list(patterns.keys()), cumulative_counts, color=colors)
    bar_ax.set_title('Cumulative Pattern Counts', fontsize=12)
    bar_ax.tick_params(axis='x', rotation=45, labelsize=9)
    bar_ax.set_ylabel('Count', fontsize=10)
    return [im] + list(lines.values())

plt.subplots_adjust(left=0.04, right=0.96, top=0.92, bottom=0.07, wspace=0.4, hspace=0.1)
ani = FuncAnimation(fig, update, frames=steps, interval=5, blit=False)
plt.show()
