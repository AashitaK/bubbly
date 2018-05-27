import pandas as pd
import numpy as np

def bubbleplot(dataset, x_column, y_column, dot_column, time_column, size_column=None, category_column=None, 
                            x_title=None, y_title=None, title=None, x_logscale=False, y_logscale=False, 
                            show_slider=True, show_button=True, width=None, height=None):
    ''' Makes the animated and interactive bubble charts from a given dataset.''''
    
    # Make the grid
    years = dataset[time_column].unique()
    
    if size_column:
        column_names = [x_column, y_column, dot_column, size_column]
    else:
        column_names = [x_column, y_column, dot_column]
        
    if category_column:
        categories = dataset[category_column].unique()
        col_name_template = '{}+{}+{}_grid'
        grid = make_grid_with_categories(dataset, col_name_template, column_names, 
                                         time_column, category_column, years, categories)
        showlegend=True
    else:
        col_name_template = '{}+{}_grid'
        grid = make_grid(dataset, col_name_template, column_names, time_column, years)
        showlegend=False
        
    # Set the layout
    if show_slider:          
        figure, sliders_dict = set_layout(x_title, y_title, title, x_logscale, y_logscale, 
                show_slider, years, show_button, showlegend, width, height)
    else:
        figure = set_layout(x_title, y_title, title, x_logscale, y_logscale, 
                show_slider, None, show_button, showlegend, width, height)
    
    # Add the frames
    year = min(years)
    if category_column:
        # Add the base frame
        for category in categories:
            data_dict = make_data_dictionary(grid, col_name_template, year, x_column, y_column, dot_column, size_column, category)
            figure['data'].append(data_dict)
            
        # Add time frames
        for year in years:
            frame = {'data': [], 'name': str(year)}
            for category in categories:
                data_dict = make_data_dictionary(grid, col_name_template, year, x_column, y_column, dot_column, size_column, category)
                frame['data'].append(data_dict)

            figure['frames'].append(frame) 

            if show_slider:
                add_slider_steps(sliders_dict, year)
    else:
        # Add the base frame
        data_dict = make_data_dictionary(grid, col_name_template, year, x_column, y_column, dot_column, size_column)
        figure['data'].append(data_dict)
        # Add time frames
        for year in years:
            frame = {'data': [], 'name': str(year)}
            data_dict = make_data_dictionary(grid, col_name_template, year, x_column, y_column, dot_column, size_column)
            frame['data'].append(data_dict)
            figure['frames'].append(frame) 
            if show_slider:
                add_slider_steps(sliders_dict, year) 
    
    set_axisrange(figure, dataset[x_column], dataset[y_column], x_logscale, y_logscale)            
    # Plot the animation
    if show_slider:
        figure['layout']['sliders'] = [sliders_dict]
        
    return figure


def make_grid(dataset, col_name_template, column_names, time_column, years=None):
    '''Makes the grid for the plot as a pandas DataFrame by-passing the use of `plotly.grid_objs`
    that is unavailable in the offline mode for `plotly`. The grids are designed using the `col_name_template`
    from the `column_names` of the `dataset`.'''
    
    grid = pd.DataFrame()
    if years is None:
        years = dataset[time_column].unique()
        
    for year in years:
        dataset_by_year = dataset[(dataset[time_column] == int(year))]
        for col_name in column_names:
            # Each column name is unique
            temp = col_name_template.format(year, col_name)
            if dataset_by_year[col_name].size != 0:
                grid = grid.append({'value': list(dataset_by_year[col_name]), 'key': temp}, ignore_index=True)
    return grid


def make_grid_with_categories(dataset, col_name_template, column_names, time_column, category_column, years=None, categories=None):
    '''Makes the grid for the plot as a pandas DataFrame by-passing the use of plotly.grid_objs
    that is unavailable in the offline mode for plotly. The grids are designed using the `col_name_template`
    from the `column_names` of the `dataset` using the `category_column` for catergories.'''
    
    grid = pd.DataFrame()
    if categories is None:
        categories = dataset[category_column].unique() 
    if years is None:
        years = dataset[time_column].unique()
    for year in years:
        for category in categories:
            dataset_by_year_and_cat = dataset[(dataset[time_column] == int(year)) & (dataset[category_column] == category)]
            for col_name in column_names:
                # Each column name is unique
                temp = col_name_template.format(year, col_name, category)
                if dataset_by_year_and_cat[col_name].size != 0:
                    grid = grid.append({'value': list(dataset_by_year_and_cat[col_name]), 'key': temp}, ignore_index=True) 
    return grid


def add_slider_steps(sliders_dict, year):
    '''Adds the slider steps.'''
    
    slider_step = {'args': [
        [year],
        {'frame': {'duration': 300, 'redraw': False},
         'mode': 'immediate',
       'transition': {'duration': 300}}
     ],
     'label': year,
     'method': 'animate'}
    sliders_dict['steps'].append(slider_step)
  
 
def set_layout(x_title=None, y_title=None, title=None, x_logscale=False, y_logscale=False, 
            show_slider=True, slider_scale=None, show_button=True, showlegend=False,
            width=None, height=None):
    '''Sets the layout for the figure.'''
    
    figure = {
        'data': [],
        'layout': {},
        'frames': []
    }
    
    figure['layout']['xaxis'] = {'title': x_title, 'autorange': False}
    figure['layout']['yaxis'] = {'title': y_title, 'autorange': False} 

    if x_logscale:
        figure['layout']['xaxis']['type'] = 'log'
    if y_logscale:
        figure['layout']['yaxis']['type'] = 'log'
        
    figure['layout']['title'] = title    
    figure['layout']['hovermode'] = 'closest'
    figure['layout']['showlegend'] = showlegend
    figure['layout']['margin'] = dict(b=200, t=100, pad=5)
    if width:
        figure['layout']['width'] = width
    if height:
        figure['layout']['height'] = height
    # Add slider for time scale
    if show_slider:
        figure['layout']['sliders'] = {
            'args': [
                'slider.value', {
                    'duration': 400,
                    'ease': 'cubic-in-out'
                }
            ],
            'initialValue': min(slider_scale),
            'plotlycommand': 'animate',
            'values': slider_scale,
            'visible': True
        }
        sliders_dict = {
            'active': 0,
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Year:',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 300, 'easing': 'cubic-in-out'},
            'pad': {'b': 10, 't': 50},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': []
        }
    
    # Add pause-play button
    if show_button:
        figure['layout']['updatemenus'] = [
            {
                'buttons': [
                    {
                        'args': [None, {'frame': {'duration': 500, 'redraw': False},
                                 'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                        'label': 'Play',
                        'method': 'animate'
                    },
                    {
                        'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                        'transition': {'duration': 0}}],
                        'label': 'Pause',
                        'method': 'animate'
                    }
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }
        ]
    
    # Return the figure object
    if show_slider: 
        return figure, sliders_dict
    else:
        return figure
    
def set_axisrange(figure, x_values, y_values, x_logscale=False, y_logscale=False): 
    ''' Sets the x-axis and y-axis ranges for the figure.'''
    
    if x_logscale:
        xmin = min(np.log10(x_values))*0.98
        xmax = max(np.log10(x_values))*1.02
    else:
        xmin = min(x_values)*0.75
        xmax = max(x_values)*1.25
        
    if y_logscale:
        ymin = min(np.log10(y_values))*0.98
        ymax = max(np.log10(y_values))*1.02
    else:
        ymin = min(y_values)*0.75
        ymax = max(y_values)*1.25
        
    figure['layout']['xaxis']['range'] = [xmin, xmax]
    figure['layout']['yaxis']['range'] = [ymin, ymax]
    
    
def make_data_dictionary(grid, col_name_template, year, x_column, y_column, dot_column, size_column=None, category=None):
    ''' Makes the dictionary for the data that can be added to the figure or time frames.'''
    
    data_dict = {
        'x': grid.loc[grid['key']==col_name_template.format(year, x_column, category), 'value'].values[0],
        'y': grid.loc[grid['key']==col_name_template.format(year, y_column, category), 'value'].values[0],
        'text': grid.loc[grid['key']==col_name_template.format(year, dot_column, category), 'value'].values[0],
        'mode': 'markers'
        }
    
    if size_column:
        data_dict['marker'] = {
            'sizemode': 'area',
            'sizeref': 200000,
            'size': grid.loc[grid['key']==col_name_template.format(year, size_column, category), 'value'].values[0],
        }
        
    if category:
        data_dict['name'] = category
    
    return data_dict
