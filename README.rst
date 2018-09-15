bubbly
******************************

Bubbly is a package for plotting interactive and animated *bubble charts* using *Plotly*. The animated bubble charts can accommodate up to seven variables viz. X-axis, Y-axis, Z-axis, time, bubbles, their size and their color in a compact and captivating way. Bubbly is easy to use with plenty of customization, especially suited for use in Jupyter notebooks and is designed to work with ``plotly``'s offline mode such as in Kaggle kernels. 

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
  
Usage in a Jupyter Notebook
----------------------------
.. code:: python

  from __future__ import division
  from plotly.offline import init_notebook_mode, iplot
  init_notebook_mode()
  from bubbly.bubbly import bubbleplot
  
  figure = bubbleplot(dataset=gapminder_indicators, x_column='gdpPercap', y_column='lifeExp', 
    bubble_column='country', time_column='year',  size_column='pop', color_column='continent', 
    x_title="GDP per Capita", y_title="Life Expectancy", title='Gapminder Global Indicators',
    x_logscale=True, scale_bubble=3, height=650)
  iplot(figure, config={'scrollzoom': True})

.. image:: https://github.com/AashitaK/aashitak.github.io/blob/master/images/bubblechart.gif
   
   
Please refer to the `Jupyter notebook here <https://www.kaggle.com/aashita/guide-to-animated-bubble-charts-using-plotly/>`_ for more examples and illustration of the plotting function ``bubbleplot``.








