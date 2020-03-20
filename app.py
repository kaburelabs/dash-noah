import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_table as dt
from datetime import datetime
import time
import pandas as pd
import numpy as np
import plotly_express as px
from random import random
from dash.exceptions import PreventUpdate


app_name = "Noah app"

## CSS EXTERNAL FILE
external_stylesheets = [#'https://codepen.io/kaburelabs/pen/xxGRXWa.css', 
                        #"https://codepen.io/chriddyp/pen/brPBPO.css",
                        'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
                        'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']


## Defining the instance of dash
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = app_name

# server instance to run map when deploying
server = app.server

# Since I am adding callbacks to elements that don’t ~
# exist in the app.layout as they are spread throughout files
app.config.suppress_callback_exceptions = True


link_logo = '/assets/logo/logo-placeholder.png'
title_var='Teste only 123 12 3 123 '

projs_list = ['proj1', 'proj2', 'proj3', 'proj4']
var_list = ['float', 'ints', 'langs', 'date']

options_projs = zip(projs_list, var_list)

print(options_projs)


def create_header(some_string):
    header_style = {
        'background-color':'#3C4240',
        'padding': '1.5rem',
        'display':'inline-block',
        'width':'100%'
        
       # 'border-style': 'dotted'
    }
    logo_trich = html.Img(
                    src=link_logo,
                    className='three columns',
                    style={
                        'height': 'auto',
                        'width': '140px', # 'padding': 1
                        'float': 'right', #'position': 'relative'
                        'margin-right': '66px', #'border-style': 'dotted'
                        'display':'inline-block'})

    title = html.H1(children=some_string, className='eight columns',
                    style={'margin':'0 0 0 36px',
                           'color':'#ffffff', 'font-size':'35px'})

    header = html.Header(html.Div([title, logo_trich]), style=header_style)

    return header


def block_1(name='Project Name', var='STATUS'):

    return html.Div([

        html.Div([
            html.P('Project Name', className='six columns',
                   style={'display':'inline-block', 'fontSize':'1.6rem', 'width':'39%'}),

            html.P(id='proj-name', className='six columns', 
                   style={'display':'inline-block', 'fontSize':'1.8rem', 'textAlign':'center', 'width':'59%'})
        ], className='row', style={'margin':'3px 12px 0', 'height':'15.5%','padding':'5px 0 0 25px'}), 

        html.Div([
            html.P('Start Date', #className='six columns', 
                    style={'display':'inline-block', 'width':'39%', 'fontSize':'1.6rem'}),
            dcc.DatePickerSingle(
                    id='starter-date-picker',
                    min_date_allowed=datetime(2000, 1, 1),
                    max_date_allowed=datetime(2020, 3, 20),
                    initial_visible_month=datetime(2000, 1, 1),
                    date=str(datetime(2000, 1, 1, 23, 59, 59)), style={'textAlign':'center', 'width':'59%'}
                )
            # html.P('01/01/2020', #className='six columns', 
            # style={'display':'inline-block', 'textAlign':'center', 'width':'59%', 'fontSize':'1.8rem'})
        ], className='row', style={'margin':'1.5px 12px 0', 'height':'15.5%','padding':'5px 0 0 25px'}), 


        html.Div([
            html.P('Total Days', #className='six columns', 
                    style={'display':'inline-block', 'width':'39%', 'fontSize':'1.6rem'}),
            html.P('20 Days', #className='six columns', 
                    style={'display':'inline-block', 'width':'59%','textAlign':'center', 'fontSize':'1.8rem'})
        ], className='row', style={'margin':'1.5px 12px 0', 'height':'16.5%','padding':'5px 0 0 25px'}), 


        html.Div([
            html.P('Final Date',  
                   style={'display':'inline-block', 'width':'39%', 'fontSize':'1.6rem'}),
            dcc.DatePickerSingle(
                    id='final-date-picker',
                    min_date_allowed=datetime(2000, 1, 1),
                    max_date_allowed=datetime(2020, 3, 20),
                    initial_visible_month=datetime(2020, 3, 20),
                    date=str(datetime(2020, 3, 20, 23, 59, 59)), style={'textAlign':'center', 'width':'59%'}
                )
            # html.P('21/01/2020', 
            #        style={'display':'inline-block', 'textAlign':'center', 'width':'59%', 'fontSize':'1.8rem'})
        ], className='row', style={'margin':'1.5px 12px 0', 'height':'15.5%', 'padding':'5px 0 0 25px'}), 


        html.Div([
            html.Button('Run MCPM', type='submit', id='sql-button',  #className='ten columns', 
                        style={'width':'70%', "background":"#0E7C7B", 'color':'rgb(212, 244, 221)', 'margin':'0 auto', 'height':'90%'})
        ], className='row', style={'height':'20.5%','padding':'0 15px', 'textAlign':'center'}),

        html.Div([
            html.P('STATUS', className='six columns', style={'display':'inline-block', 'fontWeight':'bold', 'fontSize':'1.6rem', 'paddingLeft':'25px'}),
            html.P('RUNNING', className='six columns', style={'display':'inline-block', 'textAlign':'center', 'fontSize':'1.8rem'})
        ], className='row', style={'margin':'10px 12px 0', 'height':'15.5%'}), 

    ], style={'height':'300px', 'margin':'2.5vh 0 1.5vh'})



def drop_down_graph():
    return html.Div([
        dcc.Dropdown(
            id='dropdown-graph',
            options=[
                {'label': 'Graph1', 'value': '1'},
                {'label': 'Graph2', 'value': '2'},
                {'label': 'Graph3', 'value': '3'},
                {'label': 'Problems', 'value':'4'}
            ],
        value='1'
    )
    ], style={'margin':'0.5vh auto', 'height':'100%'})

app.layout = html.Div([
    create_header("Noah - Run SQL Application"),
    html.Div([
        html.Div(id='df-sharing', style={'display': 'none'}),
        # header logo + select project
        ## One line 
        html.Div([
            html.Div([
                html.Div([
                    html.P("SELECT A PROJECT", style={'color':'rgb(212, 244, 221)','textAlign':'center'}),
                    dcc.Dropdown(
                        id='dropdown-projects',
                        options=[
                            {'label': i, 'value': n} for i, n in options_projs
                        ],
                        multi=False, 
                        placeholder="Select a Project",
                        value=None
                    )  
                ], style={'width':'100%', 'display':'inline-block'}), 

            ], className='two columns', style={'align':'right',  'padding':'0 0 0 12px', 'margin': '15px 0'}),
            html.Div([ 
                html.Button("Select", id='button-project', style={'width':'25%', "background":"#0E7C7B", 'color':'rgb(212, 244, 221)'}
                )  
                ], className='six columns', style={ 'display':'inline-block',  'padding':'40px 0 0 12px', 'margin': '5px 0'}), 

            html.Div([
                html.Img(
                    src=link_logo,
                    style={'width':'165px'})
                ], className='four columns', style={'textAlign':'right', 'padding':'15px 0', 'float':'right'})

            ], className='row', style={'width':'90%', 'height':'90px', 'background':'#4B1D3F',
                                    'padding':'12px 50px',
                                    'margin':'0px 0px 5px'}),

        # painel and graph
        # Two different blocks
        html.Div([
            # Block one
            ## Painel part
            html.Div([
                ## Main block
                html.Div([
                    html.Div([
                        block_1()
                    ])
                ], className='row', style={'background':'#D4F4DD', 'padding':'5px 0'}),

                ## Upload Tasks
                html.Div([
                        html.Div([
                            html.P("Upload Tasks"),
                        ], className='seven columns', style={'display':'inline-block', 'margin':'15px 0', 'fontSize':'1.6rem', 'padding':'0 25px'}),
                        html.Div([
                        dcc.Upload(html.Button('Upload File'), style={'width':'80%'}),
                        ], className='five columns', style={'display':'inline-block', 'margin':'5px 0'})
                ], className='row', style={'height':'10.5%', 'padding:':'5px'}),
                ## Upload Calendar
                html.Div([
                        html.Div([
                            html.P("Upload Calendar"),
                        ], className='seven columns', style={'display':'inline-block', 'margin':'15px 0', 'fontSize':'1.6rem', 'padding':'0 25px'}),
                        html.Div([
                        dcc.Upload(html.Button('Upload File')),
                        ], className='five columns', style={'display':'inline-block', 'margin':'5px 0' })
                ], className='row', style={'height':'10.5%', 'padding:':'1vh'}),
                ## Problems Report
                html.Div([
                        html.Div([
                            html.P("Problems Report"),
                        ], className='seven columns', style={'display':'inline-block', 'margin':'15px 0', 'fontSize':'1.6rem', 'padding':'0 25px'}),
                        html.Div([
                        dcc.Upload(html.Button('Download')),
                        ], className='five columns', style={'display':'inline-block', 'margin':'5px 0'})
                ], className='row', style={'height':'10.5%', 'padding:':'1vh'}),
                
                ## Download Results
                html.Div([
                        html.Div([
                            html.P("Download Results"),
                        ], className='seven columns', style={'display':'inline-block', 'margin':'15px 0', 'fontSize':'1.6rem', 'padding':'0 25px'}),
                        html.Div([
                        dcc.Upload(html.Button('Download')),
                        ], className='five columns', style={'display':'inline-block', 'margin':'5px auto'})
                ], className='row', style={'height':'10.5%', 'padding:':'1vh'}),
                
            ], className='four columns',  
            style={'height':'70vh'}),



            # Block two
            ## Graph part
            html.Div([
                html.Div([
                    # button
                    html.Div([
                        html.P("SELECT THE GRAPH: ", style={'fontWeight':'bold', 'textAlign':'center', 'color':'rgb(212, 244, 221)'}),
                        drop_down_graph()
                    ], className='five columns', style={'display':'right', 'height':'100%', 'width':'25%'} )
                ], className='row', style={'height':'80px', 'background':'#D62246', 'padding':'10px 35px', 'margin':'0px 50px'}),

                html.Div([
                    dcc.Loading(
                        id="loading-2",
                        children=[
                            html.Div([
                                dcc.Graph(id='graph-princ1', style={'width':'100%', 'height':'450px'})
                    ])], type='graph', style={'margin':'15% 0'})
                ], className='row', style={'width':'100%', 'margin':'15px auto', 'padding':'.5vh 0'}),


            ], className='eight columns')

        ], className='row', style={'width':'100%', 'height':'600px'}),

        html.Div([
            html.Div([
                    html.P(id='query-output', style={'fontSize':'20px'})
            ], className='twelve columns')
        ], className='row')

    ], className='container')

])

@app.callback(Output('proj-name','children'),
             [Input('dropdown-projects', 'value')]
              )
def _update_graph1(proj_name):

    if proj_name is None:
        return "None Selected   " 
    else: 
        return proj_name


# @app.callback(Output('df-sharing','children'),
#               [Input('dropdown-projects', 'value')],
#               [State('starter-date-picker', 'date'),
#                State('final-date-picker', 'date')]
#               )
# def _update_graph1(run_query, date_start, date_final):

#     if run_query is None:
#         raise PreventUpdate
#     else: 
#         pass

#     return

@app.callback([Output('df-sharing','children'),
               Output('query-output', 'children')],
              [Input('sql-button', 'n_clicks')],
              [State('starter-date-picker', 'date'),
               State('final-date-picker', 'date'),
               State('dropdown-projects', 'value')]
              )
def _update_graph1(run_button, date_start, date_final, proj_name):

    if run_button is None:
        raise PreventUpdate
    else: 
        pass

    date_start = pd.to_datetime(date_start)
    date_final = pd.to_datetime(date_final)

    print(f"SELECT * FROM {proj_name} WHERE date >= {date_start} and date <= {date_final}")

    # print((date_final - date_start).days)
    
    # df = pd.read_sql('SELECT * FROM tweets')
    # print('balbablablalbal', run_query, date_start, date_final)

    df = pd.DataFrame({ 
        'float': np.random.randn(50),
        'ints': np.random.choice( [5, 7, 8, 18, 20, 5, 3, 14, ], 50),
        'langs': np.random.choice( ['panda','python','shark', 'C#', 'Java', 'javascript', 'C++', 'SQL', 'Spark'], 50),
        'date': np.random.choice(pd.date_range('1/1/2011', periods=365, 
                                 freq='D'), 50, replace=False)})

    # print('run clicked', df)

    return [df.to_json(date_format='iso', orient='split'), 
            (f"QUERY SIMULATION: SELECT * FROM {proj_name} WHERE date >= {date_start} and date <= {date_final}")]
    

@app.callback(Output('graph-princ1','figure'),
              [Input('df-sharing','children'),
               Input('dropdown-graph', 'value')])
def _update_graph1(df, query):

    if df is None:
        raise PreventUpdate
    else: 
        pass

    df_ = pd.read_json(df, orient='split')

    time.sleep(3)

    if query == '2':
        val_count = df_.ints.value_counts().reset_index()
        fig = px.scatter(val_count, x='index', y='ints', title=title_var)
        fig.update_layout(title_x=.5)
        return fig
        
    elif query == '3':
        #val_count = df_.langs.value_counts().reset_index()
        fig = px.box(df_, x='langs', y='float', title=(str(title_var) + str(3)))
        fig.update_layout(title_x=.5)
        return fig
        
    elif query == '4':
        val_count = df_.date.value_counts().reset_index()
        fig = px.line(val_count, x='index', y='date', title=title_var)

        fig.update_layout(title_x=.5)
        return fig
    else: 
        val_count = df_.langs.value_counts().reset_index()
        fig = px.bar(val_count, x='index', y='langs', title=title_var)
        fig.update_layout(title_x=.5)       
        return fig





if __name__ == '__main__':
    app.run_server(debug=True)












