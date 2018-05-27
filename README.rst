bubbles
******************************

A module for plotting interactive and animated bubble charts using Plotly.

Dependencies
------------
* Python 3.4+
* pandas 
* plotly

Usage
-------
.. code:: python

  from bubbles import interactive_bubble_plot
  interactive_bubble_plot(dataset=gapminder_indicators, x_column='gdpPercap', y_column='lifeExp', 
    dot_column='country', time_column='year', size_column='pop', category_column='continent', 
    x_title="GDP per Capita", y_title="Life Expectancy", title='Gapminder Global Indicators',
    x_logscale=True, height=650)
    
Please refer to the `Jupyter notebook here <https://www.kaggle.com/aashita/animated-graphs-using-plotly/>`_ for illustration of the plotting function.








