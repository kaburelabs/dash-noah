import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_table as dt
from datetime import datetime
import base64
import io
import time
import pandas as pd
import numpy as np
import plotly_express as px
from random import random
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
import psycopg2
from sqlalchemy_utils import database_exists, create_database
from decouple import config

app_name = "Noah app"


DATABASE_URL = config('DATABASE_URL')

DEVELOPER = config('DEVELOPER', default=False, cast=bool)

engine = create_engine(DATABASE_URL)
con = psycopg2.connect(DATABASE_URL)

csv_file = "../Upwork1-Noah-APP/data_simulation.csv"
df = pd.read_csv(csv_file, index_col=[0])

if DEVELOPER:
    # if the database does not exist
    if not database_exists(engine.url):
        # create a new database
        create_database(engine.url)

try:
    df.to_sql("projs", engine, if_exists='fail', index=False )
    del df
except:
    del df
    print("An exception occurred")


# print(df_to_db)
## CSS EXTERNAL FILE
external_stylesheets = [dbc.themes.BOOTSTRAP, 
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

regions = ['regions0', 'regions1', 'regions2', 'regions3', 'regions4',
           'regions5', 'regions6', 'regions7', 'regions8', 'regions9',
           'regions10', 'regions11', 'regions12', 'regions13', 'regions14',
           'regions15', 'regions16', 'regions17', 'regions18', 'regions19']

link_logo = '/assets/logo/logo-placeholder.png'
title_var='Teste only 123 12 3 123 '


def create_header(some_string):
    header_style = {
        'background-color':'#3C4240',
        'padding': '1.5rem',
        'display':'inline-block',
        'width':'100%'
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

def block_1():
    return html.Div([

        html.Div([
            html.P('Project Name', className='six columns',
                   style={'display':'inline-block', 'fontSize':'17px', 'width':'39%'}),
            html.P(id='proj-name', className='six columns', 
                   style={'display':'inline-block', 'fontSize':'18px', 'textAlign':'center', 'width':'59%'})
        ], className='row-m', style={'margin':'1.5px 12px 0', 'height':'15.5%'}), 

        html.Div([
            html.P('Start Date', #className='six columns', 
                    style={'display':'inline-block', 'width':'45%', 'fontSize':'17px'}),
            html.P(id='dateStart', style={'textAlign':'center', 'width':'54%', 'float':'right', 'fontSize':'18px'})
            # dcc.DatePickerSingle(
            #         id='starter-date-picker',
            #         min_date_allowed=datetime(2019, 1, 1),
            #         max_date_allowed=datetime.today().strftime('%Y, %m, %d'),
            #         initial_visible_month=datetime(2019, 1, 1),
            #         placeholder='Select Date',
            #         #date=str(datetime(2019, 1, 1, 23, 59, 59)),
            #         style={'textAlign':'right', 'width':'59%', 'float':'right'})
        ], className='row-m', style={'margin':'1.5px 12px 0', 'height':'15.5%'}), 

        html.Div([
            html.P('Length (months)', #className='six columns', 
                    style={'display':'inline-block', 'width':'45%', 'fontSize':'17px'}),
            html.P(id='days-diff', #className='six columns', 
                    style={'display':'inline-block', 'width':'54%','textAlign':'center', 'fontSize':'18px'})
        ], className='row-m', style={'margin':'1.5px 12px 0', 'height':'16.5%'}), 


        html.Div([
            html.P('Final Date',  
                   style={'display':'inline-block', 'width':'45%', 'fontSize':'17px'}),
            html.P(id='dateFinal', style={'textAlign':'center', 'width':'54%', 'float':'right', 'fontSize':'18px'})
            # dcc.DatePickerSingle(
            #         id='final-date-picker',
            #         min_date_allowed=datetime(2019, 1, 1),
            #         max_date_allowed=datetime.today().strftime('%Y-%m-%d'),
            #         initial_visible_month=datetime.today().strftime('%Y-%m-%d'),
            #         placeholder="Select Date", 
            #         #date=str(datetime(2020, 3, 20, 23, 59, 59)),
            #         style={'textAlign':'right', 'width':'59%', 'float':'right', })
        ], className='row-m', style={'margin':'1.5px 12px 0', 'height':'15.5%'}), 

        html.Div([
            html.Button('Run MCPM', type='submit', id='sql-button',  #className='ten columns', 
                        style={'width':'70%', "background":"#0E7C7B", 'color':'rgb(212, 244, 221)', 'margin':'0 auto', 'height':'90%'})
        ], className='row-m', style={'height':'20.5%','padding':'0 30px', 'textAlign':'center', 'margin':'0 24px 0 0'}),

        html.Div([
            html.P('STATUS', className='six columns', style={'display':'inline-block', 'fontWeight':'bold', 'fontSize':'17px', 'paddingLeft':'25px'}),
            html.P('RUNNING', className='six columns', style={'display':'inline-block', 'textAlign':'right', 'fontSize':'18px', 'paddingRight':'25px'})
        ], className='row-m', style={'margin':'10px 12px 0', 'height':'15.5%'}), 

    ], style={'height':'300px', 'margin':'15px 15px'})



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
        placeholder="Select a Graph"
    )
    ], style={'margin':'0.5vh auto', 'height':'100%'})

app.layout = html.Div([
    #create_header("Noah - Run SQL Application"),
    html.Div([
        html.Div(id='df-sharing', style={'display': 'none'}),
        # header logo + select project
        ## One line 
        html.Div([

            html.Div([
                html.Img(
                    src=link_logo,
                    style={'width':'120px'})
                ], className='seven columns', style={ 'padding':'15px 0',}),

        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        # html.P("SELECT A PROJECT", style={'color':'rgb(212, 244, 221)','textAlign':'center'}),
                        dcc.Dropdown(
                            id='dropdown-projects',
                            multi=False, 
                            placeholder="Select a Project",
                            value=None
                        )  
                    ], style={'width':'100%', 'display':'inline-block'}), 
                ], className='six columns', style={'align':'right'}),

                html.Div([ 
                    # html.Button("New Project", id='button-project', 
                        dbc.Button("+ Add Project", id="open", style={'width':'100%', "background":"#0E7C7B",
                                       'color':'rgb(212, 244, 221)'}),
                        dbc.Modal(
                            [
                                dbc.ModalHeader("New Project", style={'background':'rgb(62, 58, 61)', 'color':'rgb(212, 244, 221)'}),
                                dbc.ModalBody(
                                    html.Div([
                                        html.Div([
                                            html.Div([
                                                dcc.Input(id='proj-name-new', 
                                                          placeholder='Write the Project Name', 
                                                          style={'width':'100%'})
                                                ], className='eight columns mr-4'),
                                            html.Div([
                                                dcc.Dropdown(id='region-new', 
                                                                options=[
                                                                    {'label': i, 'value': i} for i in regions
                                                                ], placeholder="Select a region" )
                                            ], className='four columns'),
                                        ], className='row-m'),

                                        html.Div([
                                            html.Div([
                                                dcc.DatePickerRange(
                                                id='my-date-picker-range',
                                                min_date_allowed=datetime(2015, 1, 1),
                                                max_date_allowed=datetime.today().strftime('%Y-%m-%d'),
                                                initial_visible_month=datetime(2019, 1, 1),

                                                end_date=datetime.today().strftime('%Y-%m-%d'))
                                            ], className='eight columns', style={ 'float':'left', 'fontSize':'17px'}),
                                            html.Div([
                                                html.Button('Submit', id='submit-new', style={ 'background':'#0E7C7B', 'color':'rgb(212, 244, 221)'})
                                            ], className='four columns', style={'float':'right', 'textAlign':'center'})
                                        ], className='row-m m-4')
                                    ]), style={'background':'#D4F4DD'}),
                                dbc.ModalFooter(
                                    dbc.Button("Close", id="close")
                                ),
                            ],
                            id="modal", centered=True
                        ),
                    ], className='six columns', style={ 'display':'inline-block',  'float':'right'}), 
                ])
                ], className='five columns', style={'float':'right', 'padding':'25px 25px'})
            ], className='row-m', style={ 'height':'90px', 
                                       'background':'rgb(62, 58, 61)',
                                       'padding':'12px 50px',
                                       'margin':'0px 0px 24px'}),

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
                ], className='row-m', style={'background':'#D4F4DD', 'padding':'5px 0', 'margin':'0 0 24px'}),

                ## Upload Tasks
                html.Div([
                        html.Div([
                            html.P("Upload Tasks", style={'margin':'8px 0'}),
                        ], className='seven columns', style={'fontSize':'1.6rem'}),
                        html.Div([
                            dcc.Upload(id='upload-tasks', children=html.Button('Upload File'), multiple=True, style={'width':'80%'}),
                        ], className='five columns')
                ], className='row-m', style={'paddingBottom':'16px'}),

                ## Upload Calendar
                html.Div([
                        html.Div([
                            html.P("Upload Calendar", style={'margin':'8px 0'}),
                        ], className='seven columns', style={'fontSize':'1.6rem', }),
                        html.Div([
                        dcc.Upload(html.Button('Upload File')),
                        ], className='five columns')
                ], className='row-m', style={'paddingBottom':'16px'}),

                ## Problems Report
                html.Div([
                        html.Div([
                            html.P("Problems Report", style={ 'margin':'8px 0'}),
                        ], className='seven columns', style={'fontSize':'1.6rem', }),
                        html.Div([
                        dcc.Upload(html.Button('Download', style={'width':'146px'})),
                        ], className='five columns', )
                ], className='row-m', style={'paddingBottom':'16px'}),
                
                ## Download Results
                html.Div([
                        html.Div([
                            html.P("Download Results", style={'margin':'8px 0' }),
                        ], className='seven columns', style={'fontSize':'1.6rem'}),
                        html.Div([
                        dcc.Upload(html.Button('Download', style={'width':'146px'})),
                        ], className='five columns')
                ], className='row-m'),

            ], className='four columns', style={
                                                'marginBottom':'24px'}),

            # Block two
            ## Graph part
            html.Div([
                # button
                html.Div([
                    html.Div([
                        # html.P("SELECT THE GRAPH: ", style={'fontWeight':'bold', 'textAlign':'center', 'color':'rgb(212, 244, 221)'}),
                        drop_down_graph()
                    ], className='eight columns', style={'display':'right', 'height':'100%', 'width':'40%'} )
                ], className='row-m', style={'background':'#4B1D3F', 'padding':'24px 35px'   }),
                ## Graph
                html.Div([
                    dcc.Loading(
                        id="loading-2",
                        children=[
                            html.Div([
                                dcc.Graph(id='graph-princ1', style={'width':'100%', 'height':'450px'})
                    ])], type='graph', style={'margin':'100px'})
                ], className='row-m', style={'width':'100%', 'margin':'15px auto', 'padding':'.5vh 0'}),
            ], className='eight columns', style={'marginLeft':'4%'})
        ], className='row-m', style={'width':'100%',}),

        html.Div([
            html.Div([
                html.P(id='query-output', style={'fontSize':'20px'})
            ], className='twelve columns')
        ], className='row-m'),
        html.Div([
            html.Div([
                html.P(id='query-output2', style={'fontSize':'20px'})
            ], className='twelve columns')
        ], className='row-m'),
        html.Div([
            html.Div([
                html.Div(id='query-output3', style={'fontSize':'20px', 'width':'100%'})
            ], className='twelve columns')
        ], className='row-m')
    ], className='container')

], style={'overflow':'hidden'})


@app.callback([Output('proj-name','children'),
               Output('dateStart','children'),
               Output('days-diff','children'),
               Output('dateFinal','children')],
             # [Input('button-project', 'n_clicks')],
             [Input('dropdown-projects', 'value')]
              )
def _update_graph1(proj_name):

    if proj_name is None:
        return ["None Selected", "-", "-", "-" ]
    else: 
        pass

    df = pd.read_sql_query("SELECT * FROM projs", con)
    mask = df["project_name"] == proj_name
    print(proj_name)

    df['StartDate'] = pd.to_datetime(df['StartDate'])
    df['FinalDate'] = pd.to_datetime(df['FinalDate'])

    df['diff'] = ((df['FinalDate'] - df['StartDate']) / np.timedelta64(1, 'M'))
    df['diff'] = df['diff'].astype(int)

    final = df[mask].to_dict('row')[0]

    return [final['project_name'], 
            final['StartDate'].strftime('%d-%m-%Y'), 
            final['diff'], 
            final['FinalDate'].strftime('%d-%m-%Y')]



@app.callback([Output('df-sharing','children'),
               Output('query-output', 'children'),
               #Output('days-diff', 'children')
               ],
              [Input('sql-button', 'n_clicks')],
              [State('dateStart', 'children'),
               State('dateFinal', 'children'),
               State('proj-name', 'children')]
              )
def _update_graph1(run_button, date_start, date_final, proj_name):

    if run_button is None:
        raise PreventUpdate
    else: 
        pass
    print()
    date_start = pd.to_datetime(date_start, )
    date_final = pd.to_datetime(date_final)
    days_diff = round((date_final - date_start).days / 30)
    date_start = date_start.date()
    date_final = date_final.date()
    print(f"SELECT * FROM {proj_name} WHERE date >= {date_start} and date <= {date_final}")


    # df = pd.read_sql('SELECT * FROM tweets')
    # print('balbablablalbal', run_query, date_start, date_final)

    df = pd.DataFrame({ 
        'float': np.random.randn(50),
        'ints': np.random.choice( [5, 7, 8, 18, 20, 5, 3, 14, ], 50),
        'langs': np.random.choice( ['panda','python','shark', 'C#', 'Java', 'javascript', 'C++', 'SQL', 'Spark'], 50),
        'date': np.random.choice(pd.date_range('1/1/2011', periods=365, 
                                 freq='D'), 50, replace=False)})

    return [df.to_json(date_format='iso', orient='split'), 
            (f"QUERY SIMULATION: SELECT * FROM {proj_name} WHERE date >= {date_start} and date <= {date_final}")]
    

@app.callback(Output('dropdown-projects', 'options'),
              [Input('submit-new', 'n_clicks')],
               [State('dropdown-projects', 'options')])
def _update_dropdown_proj(n_click, two):
    # print('botão dropdown', n_click)
    # print('botão dropdown2', two)
    time.sleep(1)
    df = pd.read_sql_query("SELECT * FROM projs", con)

    options=[{'label': i, 'value': i} for i in df['project_name'].to_list()]   
    # print(options)
    return options


@app.callback(Output('query-output2', 'children'),
              [Input('submit-new', 'n_clicks')],
              [State('proj-name-new','value'),
               State('region-new', 'value'),
               State('my-date-picker-range', 'end_date'),
               State('my-date-picker-range', 'start_date')])
def _update_graph1(click, name, region, end, start):
    print(click)
    if None in [name, region, start, end]:
        raise PreventUpdate
    else:
        pass

    print(start)

    vals = {'project_name': [name], 'StartDate': [start], 'FinalDate':[end], 'Region': [region]}

    df = pd.DataFrame(vals)

    df.to_sql("projs", engine, if_exists='append', index=False )

    print(df )
    
    return name





@app.callback(Output('graph-princ1','figure'),
              [Input('df-sharing','children'),
               Input('dropdown-graph', 'value')])
def _update_graph1(df, graph):

    if df is None:
        raise PreventUpdate
    else: 
        pass

    if graph is None:
        raise PreventUpdate
    else: 
        pass

    df_ = pd.read_json(df, orient='split')

    time.sleep(2)

    if graph == '2':
        val_count = df_.ints.value_counts().reset_index()
        fig = px.scatter(val_count, x='index', y='ints', title=title_var)
        fig.update_layout(title_x=.5)
        return fig
        
    elif graph == '3':
        #val_count = df_.langs.value_counts().reset_index()
        fig = px.box(df_, x='langs', y='float', title=(str(title_var) + str(3)))
        fig.update_layout(title_x=.5)
        return fig
        
    elif graph == '4':
        val_count = df_.date.value_counts().reset_index()
        fig = px.line(val_count, x='index', y='date', title=title_var)

        fig.update_layout(title_x=.5)
        return fig

    else: 
        val_count = df_.langs.value_counts().reset_index()
        fig = px.bar(val_count, x='index', y='langs', title=title_var)
        fig.update_layout(title_x=.5)       
        return fig


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"),
     Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# def parse_contents(contents, filename, date):

#     content_type, content_string = contents.split(',')

#     decoded = base64.b64decode(content_string)
#     try:
#         if 'csv' in filename:
#             # Assume that the user uploaded a CSV file
#             df = pd.read_csv(
#                 io.StringIO(decoded.decode('utf-8')))
#         elif 'xls' in filename:
#             # Assume that the user uploaded an excel file
#             df = pd.read_excel(io.BytesIO(decoded))
#     except Exception as e:
#         print(e)
#         return html.Div([
#             'There was an error processing this file.'
#         ])

#     return html.Div([
#                 html.H5(filename),
#                 html.H6(datetime.datetime.fromtimestamp(date)),
#                 dash_table.DataTable(
#                     data=df.head().to_dict('records'),
#                     columns=[{'name': i, 'id': i} for i in df.columns]
#                 )
#                 ])

# @app.callback(Output('query-output3', 'children'),
#               [Input('upload-tasks', 'contents')],
#               [State('upload-tasks', 'filename'),
#                State('upload-tasks', 'last_modified')])
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     print('upload tasks ',list_of_contents)
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
#         ]
#         return children


def parse_contents(contents, filename, date):
    
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H3(f'File Name: {filename}', style={'textAlign':'center'}),
        html.H6(f"Last Modification Date: {datetime.fromtimestamp(date)}"),

        dt.DataTable(
            data=df.head().to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns], 
            style_table={'overflowX': 'scroll'}, 
            style_cell={"minWidth":"20px"},
        )
    ])

@app.callback(Output('query-output3', 'children'),
              [Input('upload-tasks', 'contents')],
              [State('upload-tasks', 'filename'),
               State('upload-tasks', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)












