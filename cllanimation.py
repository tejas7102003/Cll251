import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Parameters
length = 10
inner_radius = 0.5
outer_radius = 1.0
flow_type = 'counter'  # Options: 'parallel' or 'counter'

# Create figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the viewing limits and aspect
ax.set_xlim([-length/2, length/2])
ax.set_ylim([-1.5, 1.5])
ax.set_zlim([-1.5, 1.5])
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_zticklabels([])
ax.axis('off')

# Function to draw cylindrical pipes
def draw_pipe(ax, center_z, radius, length, color):
    z = np.linspace(center_z - length/2, center_z + length/2, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    theta_grid, z_grid = np.meshgrid(theta, z)
    x_grid = radius * np.cos(theta_grid)
    y_grid = radius * np.sin(theta_grid)
    ax.plot_surface(x_grid, y_grid, z_grid, color=color, alpha=0.5, rstride=5, cstride=5, linewidth=0)

# Draw pipes
draw_pipe(ax, 0, inner_radius, length, 'red')  # Inner cylinder for hot fluid
draw_pipe(ax, 0, outer_radius, length, 'blue')  # Outer annular space for cold fluid

# Particle data for animation
num_particles = 10
particle_positions = np.linspace(-length/2, length/2, num_particles)

def update(num):
    ax.cla()
    ax.set_xlim([-length/2, length/2])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.axis('off')

    # Redraw pipes
    draw_pipe(ax, 0, inner_radius, length, 'red')
    draw_pipe(ax, 0, outer_radius, length, 'blue')

    # Update positions based on flow type
    if flow_type == 'parallel':
        z_positions_inner = particle_positions + 0.05 * num % length - length/2
        z_positions_outer = particle_positions + 0.05 * num % length - length/2
    elif flow_type == 'counter':
        z_positions_inner = particle_positions + 0.05 * num % length - length/2
        z_positions_outer = particle_positions - 0.05 * num % length + length/2

    # Draw particles, adjust radial position for outer particles
    radius_offset = (inner_radius + outer_radius) / 2
    x_inner = np.zeros(num_particles)
    y_inner = np.zeros(num_particles)
    x_outer = radius_offset * np.cos(np.linspace(0, 2 * np.pi, num_particles))
    y_outer = radius_offset * np.sin(np.linspace(0, 2 * np.pi, num_particles))

    ax.scatter(x_inner, y_inner, z_positions_inner, color='blue', s=50)
    ax.scatter(x_outer, y_outer, z_positions_outer, color='yellow', s=50)

    return ax,

# Create animation
ani = FuncAnimation(fig, update, frames=200, interval=50)

plt.show()
