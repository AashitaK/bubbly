import pandas as pd
import numpy as np

def bubbleplot(dataset, x_column, y_column, bubble_column, time_column=None, size_column=None, color_column=None,  
                x_title=None, y_title=None, title=None, colorbar_title=None, 
                x_logscale=False, y_logscale=False, x_range=None, y_range=None, 
                scale_bubble=1, colorscale=None, width=None, height=None,
                show_slider=True, show_button=True, show_colorbar=True):
    ''' Makes the animated and interactive bubble charts from a given dataset.'''
    
    # Set category_column as None and update it as color_column only in case
    # color_column is not None and categorical, in which case set color_column as None
    category_column = None
    if color_column:
        if dataset[color_column].dtype.name in ['category', 'object', 'bool']:
            category_column = color_column
            color_column = None
        
    # Set the variables for making the grid
    years = dataset[time_column].unique()
    column_names = [x_column, y_column, bubble_column]
    
    if size_column:
        column_names.append(size_column)
    
    if color_column:
        column_names.append(color_column)
        
    # Make the grid
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
    
    if size_column:
        sizeref = 2.*max(dataset[size_column])/(scale_bubble*80**2) # Set the reference size for the bubbles
    else:
        sizeref = None
        
    # Add the frames
    year = min(years) # The earliest year for the base frame
    if category_column:
        # Add the base frame
        for category in categories:
            trace = get_trace(grid, col_name_template, year, x_column, y_column, bubble_column, 
                                             size_column, sizeref, scale_bubble, category=category)
            figure['data'].append(trace)
            
        # Add time frames
        for year in years:
            frame = {'data': [], 'name': str(year)}
            for category in categories:
                trace = get_trace(grid, col_name_template, year, x_column, y_column, bubble_column, 
                                                 size_column, sizeref, scale_bubble, category=category)
                frame['data'].append(trace)

            figure['frames'].append(frame) 

            if show_slider:
                add_slider_steps(sliders_dict, year)
    else:
        # Add the base frame
        trace = get_trace(grid, col_name_template, year, x_column, y_column, bubble_column, 
                        size_column, sizeref, scale_bubble, color_column, colorscale, show_colorbar, colorbar_title)
        figure['data'].append(trace)
        # Add time frames
        for year in years:
            frame = {'data': [], 'name': str(year)}
            trace = get_trace(grid, col_name_template, year, x_column, y_column, bubble_column, 
                            size_column, sizeref, scale_bubble, color_column, colorscale, show_colorbar, colorbar_title)
            frame['data'].append(trace)
            figure['frames'].append(frame) 
            if show_slider:
                add_slider_steps(sliders_dict, year) 
    
    # Set ranges for the axes
    if x_range is None:
        x_range = set_range(dataset[x_column], x_logscale) 
    
    if y_range is None:
        y_range = set_range(dataset[y_column], y_logscale)
        
    figure['layout']['xaxis']['range'] = x_range
    figure['layout']['yaxis']['range'] = y_range
    
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

  
 
def set_layout(x_title=None, y_title=None, title=None, x_logscale=False, y_logscale=False, 
            show_slider=True, slider_scale=None, show_button=True, showlegend=False,
            width=None, height=None):
    '''Sets the layout for the figure.'''
    
    # Define the figure object as a dictionary
    figure = {
        'data': [],
        'layout': {},
        'frames': []
    }
    
    # Start with filling the layout first
    figure['layout']['xaxis'] = {'title': x_title, 'autorange': False}
    figure['layout']['yaxis'] = {'title': y_title, 'autorange': False} 

    if x_logscale:
        figure['layout']['xaxis']['type'] = 'log'
    if y_logscale:
        figure['layout']['yaxis']['type'] = 'log'
        
    figure['layout']['title'] = title    
    figure['layout']['hovermode'] = 'closest'
    figure['layout']['showlegend'] = showlegend
    figure['layout']['margin'] = dict(b=50, t=50, pad=5)
    if width:
        figure['layout']['width'] = width
    if height:
        figure['layout']['height'] = height
    
    # Add slider for the time scale
    if show_slider: 
        sliders_dict = add_slider(figure, slider_scale)
    
    # Add a pause-play button
    if show_button:
        add_button(figure)

    # Return the figure object
    if show_slider:
        return figure, sliders_dict
    else:
        return figure
    
    
def add_slider(figure, slider_scale):
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
    return sliders_dict

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
    
def add_button(figure):
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
    
def set_range(values, logscale=False): 
    ''' Finds the axis range for the figure.'''
    
    if logscale:
        rmin = min(np.log10(values))*0.97
        rmax = max(np.log10(values))*1.04
    else:
        rmin = min(values)*0.7
        rmax = max(values)*1.4
        
    return [rmin, rmax] 
    
    
def get_trace(grid, col_name_template, year, x_column, y_column, bubble_column, size_column=None, 
                         sizeref=200000, scale_bubble=1, color_column=None, colorscale=None, show_colorbar=True,
                         colorbar_title=None, category=None):
    ''' Makes the trace for the data as a dictionary object that can be added to the figure or time frames.'''
    
    trace = {
        'x': grid.loc[grid['key']==col_name_template.format(year, x_column, category), 'value'].values[0],
        'y': grid.loc[grid['key']==col_name_template.format(year, y_column, category), 'value'].values[0],
        'text': grid.loc[grid['key']==col_name_template.format(year, bubble_column, category), 'value'].values[0],
        'mode': 'markers'
        }
    
    if size_column:
        if color_column:
            trace['marker'] = {
                'sizemode': 'area',
                'sizeref': sizeref,
                'size': grid.loc[grid['key']==col_name_template.format(year, size_column, category), 'value'].values[0],
                'color': grid.loc[grid['key']==col_name_template.format(year, color_column), 'value'].values[0],
                'colorbar': {'title': colorbar_title},
                'colorscale': colorscale
            }
        else:
            trace['marker'] = {
                'sizemode': 'area',
                'sizeref': sizeref,
                'size': grid.loc[grid['key']==col_name_template.format(year, size_column, category), 'value'].values[0],
            }
    else:
        trace['marker'] = {
            'size': 10*scale_bubble,
        }
        
    if category:
        trace['name'] = category
        
    return trace
