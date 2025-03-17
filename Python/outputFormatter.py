import matplotlib.pyplot as plt
import numpy as np


def create(short_list, long_list, name="output.png"):

    # Combine both lists to determine the range of values
    min_value = min(min(short_list), min(long_list))
    max_value = max(max(short_list), max(long_list))

    # Prepare the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the long list as a line with points
    long_x = np.arange(len(long_list))
    long_y = long_list
    ax.plot(long_x, long_y, marker='o', color='b', label="Long list (line)")

    # Calculate width of each rectangle so that total width of rectangles matches width of points
    rectangle_width = len(long_list) / len(short_list)

    # Plot the short list as horizontally spaced rectangles
    for i, s in enumerate(short_list):
        ax.add_patch(plt.Rectangle((i * rectangle_width, s - 0.4), rectangle_width, 0.8, color='r',
                                   label="Short list (rectangles)" if i == 0 else ""))

    # Adjust the axis limits to fit the graph to the values in the lists
    ax.set_ylim(min_value - 1, max_value + 1)
    ax.set_xlim(-1, len(long_list))  # Adjust x-axis to fit the long list points

    # Remove x-axis labels
    ax.set_xticks([])

    # Labeling the graph
    ax.set_title('Graph with Rectangles and Line')
    ax.set_ylabel('Value')

    # Adding a legend
    ax.legend()

    # Show the graph
    plt.tight_layout()
    plt.savefig(name)


if __name__ == "__main__":
    create([15],
    [81, 67, 81])
