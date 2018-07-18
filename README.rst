bubbly
******************************

Bubbly is a package for plotting interactive and animated *bubble charts* using *Plotly*. The animated bubble charts can accommodate six variables in total viz. X-axis, Y-axis, time, dots, their size and their color in a compact and captivating way. The function ``bubbleplot`` is easy to use with plenty of customization and returns a ``figure`` object that is a dictionary in a suitable format for use with ``plotly``. Bubbly is especially suited for use in Jupyter notebooks and is designed to work with ``plotly``'s offline mode such as in Kaggle kernels. 

Dependencies
------------
* Python 3.4+
* numpy
* pandas 
* plotly

Installation
-------------
.. code:: python

  pip install bubbly
  
Usage
-------
.. code:: python

  from __future__ import division
  from plotly.offline import init_notebook_mode, iplot
  init_notebook_mode()
  from bubbly.bubbly import bubbleplot
  
  figure = bubbleplot(dataset=gapminder_indicators, x_column='gdpPercap', y_column='lifeExp', 
    dot_column='country', time_column='year', size_column='pop', category_column='continent', 
    x_title="GDP per Capita", y_title="Life Expectancy", title='Gapminder Global Indicators',
    x_logscale=True, height=650)
  iplot(figure, config={'scrollzoom': True})

<a href="https://imgflip.com/gif/2e98qu"><img src="https://i.imgflip.com/2e98qu.gif" title="made at imgflip.com"/></a>

Please refer to the `Jupyter notebook here <https://www.kaggle.com/aashita/guide-to-animated-bubble-charts-using-plotly/>`_ for illustration of the plotting function.








