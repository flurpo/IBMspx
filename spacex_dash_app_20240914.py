# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

## Create options for the dropdown including 'All Sites' and unique launch sites
dropdown_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()] 

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                       options=dropdown_options,
                                       value='ALL',  # Default value
                                       placeholder="Select a Launch Site here",
                                       searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',  # Set the id to 'payload-slider'
                                    min=0,  # Starting point of the slider
                                    max=10000,  # Ending point of the slider
                                    step=1000,  # Interval step of the slider
                                    marks={0: '0 kg', 1000: '1000 kg', 2000: '2000 kg', 3000: '3000 kg', 4000: '4000 kg', 
                                           5000: '5000 kg', 6000: '6000 kg', 7000: '7000 kg', 8000: '8000 kg', 9000: '9000 kg', 
                                           10000: '10000 kg'},  # Marks on the slider
                                    value=[min_payload, max_payload]  # Current selected range
                                ),
                                html.Br(),

                        

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # If ALL sites are selected, show the total success count across all sites
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Success Launches for All Sites')
        return fig
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Generate pie chart for the selected site's success vs failure
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f"Success vs Failure for site {entered_site}",
                     hole=.3)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    # Filter the dataframe based on the payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    if selected_site == 'ALL':
        # Plot scatter chart for all sites
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category', 
                         title='Correlation between Payload Mass and Launch Outcome (All Sites)',
                         labels={'class': 'Launch Outcome (0: Failure, 1: Success)'})
    else:
        # Filter the dataframe for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        # Plot scatter chart for the selected site
        fig = px.scatter(filtered_df, 
                         x='Payload Mass (kg)', 
                         y='class', 
                         color='Booster Version Category', 
                         title=f'Correlation between Payload Mass and Launch Outcome for {selected_site}',
                         labels={'class': 'Launch Outcome (0: Failure, 1: Success)'})
    
    return fig

#python3.11 spacex_dash_app.py
# Run the app
if __name__ == '__main__':
    app.run_server()
