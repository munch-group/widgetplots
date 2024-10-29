
def foo(x, y=1):
    """
    The sum of two numbers.

    Parameters
    ----------
    x : int
        The first number
    y: int, default=1
        The second number.

    Returns
    -------
    int
        Sum of two numbers.


    See Also
    --------
    scripts.bar : "Printing hello world".     

    """
    return x + y


import sys
import pandas as pd
import numpy as np
import ipywidgets 
import seaborn as sns
import matplotlib.pyplot as plt 
# %config InlineBackend.figure_format = 'retina'

graphics = [
    sns.boxplot, 
    sns.scatterplot, 
    sns.violinplot,
    sns.boxenplot, 
    sns.swarmplot,
    sns.stripplot,
    sns.kdeplot,
    sns.barplot,
]

def interactive_plot(df, defaults, graphics=graphics, strings_as_cats=False, palette="colorblind"):
    def plot(selected_x, selected_y, selected_hue=None, selected_plot=graphics[0]):
        plt.close('all')
        fig, ax = plt.subplots(1, 1, figsize=(8,4))
        sns.set_style('ticks')
        kwargs = dict(x=df[selected_x], y=df[selected_y])
        if selected_hue in df:
            kwargs['hue'] = df[selected_hue]
            kwargs['palette'] = palette
        try:
            selected_plot(**kwargs, ax=ax)
        except TypeError as e:
            print(f"{str(e).split(',')[0]}. That does not compatible with {selected_plot.__name__}", file=sys.stderr)
            plt.close('all')            
            return
        plt.title(f'{selected_plot.__name__.capitalize()} of {selected_y} for {selected_x}')
        handles, labels = ax.get_legend_handles_labels()
        if labels:
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        sns.despine()
        plt.show()
    
    categorical_col_names = df.columns[(df.map(type) == str).all(0)].to_list()

    dropdowns = {}
    if 'plot' in defaults:
        plot_options = [(g.__name__, g) for g in graphics]
        names, funs = zip(*plot_options)
        i = names.index(defaults['plot'])
        options = plot_options[i:i+1] + plot_options[:i] + plot_options[i+1:] 
        drop_down_plot = ipywidgets.Dropdown(options=options, description='Plot:', disabled=False)
        dropdowns['selected_plot'] = drop_down_plot
    if 'x' in defaults:
        x_options = df.columns.to_list()
        drop_down_x = ipywidgets.Dropdown(options=x_options, value=defaults['x'], description='X variable:', disabled=False)
        dropdowns['selected_x'] = drop_down_x
    if 'y' in defaults:
        if strings_as_cats:
            y_options = df.drop(categorical_col_names,axis=1).columns
        else:
            y_options = df.columns.to_list()
        drop_down_y = ipywidgets.Dropdown(options=y_options, value=defaults['y'], description='Y variable:', disabled=False)
        dropdowns['selected_y'] = drop_down_y
    if 'hue' in defaults:
        if strings_as_cats:
            hue_options = df.columns[(df.map(type) == str).all(0)]
        else:
            hue_options = df.columns.to_list()
        drop_down_hue= ipywidgets.Dropdown(options=hue_options, value=defaults['hue'], description='Hue:', disabled=False)
        dropdowns['selected_hue'] = drop_down_hue

    display(ipywidgets.HBox(list(dropdowns.values())),
            ipywidgets.interactive_output(plot, dropdowns))