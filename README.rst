bubbles
******************************

A module for plotting interactive and animated bubble charts using Plotly. It is especially suitable for use in Jupyter notebooks and is designed to work with `plotly`'s offline mode such as in Kaggle kernels. 

Dependencies
------------
* Python 3.4+
* numpy
* pandas 
* plotly

Usage
-------
.. code:: python

  from __future__ import division
  from plotly.offline import init_notebook_mode, iplot
  init_notebook_mode()
  from bubbles import interactive_bubble_plot
  
  figure = interactive_bubble_plot(dataset=gapminder_indicators, x_column='gdpPercap', y_column='lifeExp', 
    dot_column='country', time_column='year', size_column='pop', category_column='continent', 
    x_title="GDP per Capita", y_title="Life Expectancy", title='Gapminder Global Indicators',
    x_logscale=True, height=650)
  iplot(figure, config={'scrollzoom': True})
    
Please refer to the `Jupyter notebook here <https://www.kaggle.com/aashita/animated-graphs-using-plotly/>`_ for illustration of the plotting function.








