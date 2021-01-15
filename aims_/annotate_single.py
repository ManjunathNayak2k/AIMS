import base64
import datetime
import dash
import json
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_canvas
import dash_table
import pandas as pd
from dash_canvas.utils import parse_jsonstring_rectangle
from dash_canvas.components import image_upload_zone
from PIL import Image
from io import BytesIO
import base64
from numpy import asarray
import os
from aims_ import app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dashapp = dash.Dash(name='annotateapp', server=app, url_base_pathname='/annotateinv/',external_stylesheets=external_stylesheets)

list_columns = ['width', 'height', 'left', 'top', 'label']
columns = [{'name': i, "id": i} for i in list_columns]
columns[-1]['presentation'] = 'dropdown'
list_preferred = ['Company Name','Company Address','Invoice Number','Start of Table','End of Table','Subtotal','Tax','Discount','Total']
shortlists = [{'label': i, 'value': i} for i in list_preferred]

dashapp.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=[
            'Drag and Drop or ',
            html.A('Select an Image')],
        style={'width': str(100) + '%',
               'height': '50px',
               'lineHeight': '50px',
               'borderWidth': '1px',
               'borderStyle': 'dashed',
               'borderRadius': '5px',
               'textAlign': 'center'
               },
        accept='image/*',
        multiple=False,
    ),
    dash_canvas.DashCanvas(
                            id='canvas',
                            width=1000,
                            tool='rectangle',
                            lineWidth=2,
                            lineColor='rgba(255,0, 0, 0.5)',
                            hide_buttons=['pencil', 'line'],
                            goButtonTitle='Label'
                            ),
    html.Div([
        html.Div([
                html.H3('Label images with bounding boxes'),
                ]),
        html.Div([
                dash_table.DataTable(
                                    id='table',
                                    columns=columns,
                                    editable=True,
                                    dropdown = {'label': {'options': shortlists}},
                                    ),
                ])
    ]),
    dcc.Input(
            id="input_columns",
            type="number",
            placeholder="Number of columns",
        ),
    dcc.Input(
            id="input_filename",
            type="text",
            placeholder="File name",
        ),
    html.Button('Done', id='done', n_clicks=0),
    html.Div(id = 'done-output')
])

prev = None

def checkprev(imgsrc):
    global prev
    if prev==imgsrc or prev==None:
        return True
    else:
        return False

def update_prev(imgsrc):
    global prev
    prev = imgsrc
    return prev

#---callbacks---
invoice_name = None

@dashapp.callback(Output('canvas', 'image_content'),[Input('upload-data', 'contents')],[State('upload-data', 'filename'),State('upload-data', 'last_modified')], prevent_initial_call=True)
def update_canvas_upload(image_string,image_name,image_lm):
    global invoice_name
    invoice_name = image_name.split('.')[0]
    if image_string is None:
        raise ValueError
    if image_string is not None:
        return image_string
    else:
        return None

@dashapp.callback(Output('table', 'data'), [Input('canvas', 'json_data'),Input('canvas', 'image_content')], [State('table','data')],prevent_initial_call=True)
def show_string(json_data,img_content,table_data):
    if checkprev(img_content):
        update_prev(img_content)
        j = json.loads(json_data)
        if len(j["objects"])>0:
            box_coordinates = parse_jsonstring_rectangle(json_data)
            if len(box_coordinates)>0:
                df = pd.DataFrame(box_coordinates, columns=list_columns[:-1])
                stdt = df.to_dict('records')
                if table_data!=None:
                    for i in range(len(table_data)):
                        if 'label' in table_data[i]:
                            stdt[i]['label'] = table_data[i]['label']
                return stdt
        raise dash.exceptions.PreventUpdate
    else:
        update_prev(img_content)
        return None

@dashapp.callback(Output('done-output','children'),[Input('done','n_clicks')],[State('table','data'),State('canvas','image_content'),State('input_columns','value'),State('input_filename','value')],prevent_initial_call=True)
def updateout(_,tab_data,img_content,no_of_columns,filename):
    global invoice_name
    if img_content!=None and no_of_columns!=None and no_of_columns>0:
        if filename==None or filename=='':
            filename = invoice_name
        no_of_columns = int(no_of_columns)
        tab_data.append({"width":no_of_columns,"height":no_of_columns,"left":no_of_columns,"top":no_of_columns,"label":"No of Columns"})
        pd.DataFrame.from_records(tab_data).to_csv(os.path.join(app.root_path, 'static/coordinates',filename+'.csv'),index=False)
        return html.H3('Annotation results saved as {}'.format(filename))
    elif img_content==None:
        return html.H3('Load a receipt to annotate and save results')
    elif no_of_columns==None or no_of_columns<=0:
        return html.H3('Enter appropriate number of columns in table')
