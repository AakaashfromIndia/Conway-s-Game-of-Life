# Conway's Game of Life

![Game of life - Made with Clipchamp (1)](https://github.com/user-attachments/assets/ee79c8c6-9fb3-415a-8e18-bf5c5aa1f1e1)

## Overview

This project implements **Conway's Game of Life**, a classic cellular automaton devised by mathematician John Conway. The simulation features a grid of cells that evolve based on a simple set of rules, leading to complex, emergent patterns such as still lifes, oscillators, and gliders.

The interactive dashboard visualizes the game's evolution and tracks the appearance and frequency of canonical Life patterns across the board.

Contains Pattern counters for:
- Still lifes (Block, Beehive, Loaf, Boat, Tub)
- Oscillators (Blinker, Toad, Beacon, Pulsar, Pentadecathlon)
- Spaceships (Glider, LWSS, MWSS, HWSS)
- Methuselahs (Diehard, Acorn)

## How it works

- **Survival**: A **live** cell with **2 or 3 live neighbors** remains alive.
- **Underpopulation**: A **live** cell with **fewer than 2 live neighbors** dies.
- **Overpopulation**: A **live** cell with **more than 3 live neighbors** dies.
- **Reproduction**: A **dead** cell with **exactly 3 live neighbors** becomes alive.

## Summary Table

| Current State | Live Neighbors | Next State | Reason           |
|---------------|----------------|------------|------------------|
| Alive         | < 2            | Dead       | Underpopulation  |
| Alive         | 2 or 3         | Alive      | Survival         |
| Alive         | > 3            | Dead       | Overpopulation   |
| Dead          | Exactly 3      | Alive      | Reproduction     |

## Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AakaashfromIndia/Conway-s-Game-of-Life.git
   ```

2. **Install dependencies:**
   ```bash
   pip install numpy matplotlib
   ```

3. **Run the simulation:**
   ```bash
   python Conway-s-Game-of-Life.py
   ```

4. Visualize pattern evolution and frequency statistics on the dashboard.

## Dependencies

- Python 3.x
- NumPy
- Matplotlib
