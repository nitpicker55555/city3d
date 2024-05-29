import matplotlib.pyplot as plt


def plot_multiple_lists(x, y_lists, labels=None, title="Multiple Line Plot", xlabel="X-axis", ylabel="Y-axis"):
    """
    Plots multiple y-lists against a single x-list as separate lines on the same plot.

    Parameters:
    x : list
        A single list of x values.
    y_lists : list of lists
        Each sublist contains y values to be plotted against the x values.
    labels : list of str, optional
        Labels for each y-list to be used in the legend.
    title : str, optional
        Title of the plot.
    xlabel : str, optional
        Label for the X-axis.
    ylabel : str, optional
        Label for the Y-axis.
    """
    for i, y in enumerate(y_lists):
        plt.plot(x, y, label=labels[i] if labels else f'Line {i + 1}')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if labels:
        plt.legend()
    plt.grid(True)
    plt.show()


# 示例使用
x = [0, 1, 2, 3, 4]
y1 = [1, 2, 3, 4, 5]
y2 = [2, 3, 4, 5, 6]
y3 = [3, 4, 5, 6, 7]

y_lists = [y1, y2, y3]
plot_multiple_lists(x, y_lists, labels=['List 1', 'List 2', 'List 3'], title="Example Plot", xlabel="X-axis",
                    ylabel="Y-axis")
