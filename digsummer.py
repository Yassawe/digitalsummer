import json, dash
import urllib.request as httpAPI
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime

class retrieveData:
    def __init__(self, url):
        self.url=url

    def getJSONArray(self):
        response = httpAPI.urlopen(self.url)
        return json.loads(response.read())

    def getData(self):

        jsonArray=self.getJSONArray()
        devices = {}
        timebuckets = {
            "8:00-10:00": 0,
            "10:00-12:00": 0,
            "12:00-14:00": 0,
            "14:00-16:00": 0,
            "16:00-18:00": 0,
            "18:00-20:00": 0,
        }

        for i in jsonArray:
            if i['User-Agent'] in devices:
                devices[i['User-Agent']] += 1
            else:
                devices[i['User-Agent']] = 1

            hour = datetime.fromtimestamp(i['timestamp']).hour

            if 8 <= hour < 10:
                timebuckets["8:00-10:00"] += 1
            elif 10 <= hour < 12:
                timebuckets["10:00-12:00"] += 1
            elif 12 <= hour < 14:
                timebuckets["12:00-14:00"] += 1
            elif 14 <= hour < 16:
                timebuckets["14:00-16:00"] += 1
            elif 16 <= hour < 18:
                timebuckets["16:00-18:00"] += 1
            elif 18 <= hour <= 20:
                timebuckets["18:00-20:00"] += 1
        return devices, timebuckets

def runDashboard(x1,x2,y1,y2):
    dashboard = dash.Dash()
    colors = {
        'background': '#4c4c4c',
        'text': '#ff7800'
    }
    dashboard.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
        html.H1(
            children='Digital Summer дэшборд',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.Div(children='Кайнолда Яссауи', style={
            'textAlign': 'center',
            'color': colors['text']
        }),
        dcc.Graph(
            id='Graph1',
            figure={
                'data': [
                    {'x': x1, 'y': y1, 'type': 'bar'},
                ],
                'layout': {
                    'title': "Юзеры по устройствам",
                    'height': 500,
                    'width': '100%',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text'],
                        'font-size': '12px'
                    }
                }
            }

        ),
        dcc.Graph(
            id='Graph2',
            figure={
                'data': [
                    {'x': x2, 'y': y2, 'type': 'bar'},
                ],
                'layout': {
                    'title': "Нагруженность по времени",
                    'height': 500,
                    'width': '100%',
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'font': {
                        'color': colors['text'],
                        'font-size': '12px'
                    }
                }
            }

        )
    ])
    dashboard.run_server()

###############

url = "https://digital-summer.sk.kz/case_files/1585048700_IxotsoGPwgKgSWkVjzkmt4e0Wh907PJh.json"
data=retrieveData(url)
[devices, timebuckets]=data.getData()
x1=list(devices.keys())
for i in range(len(x1)):
    x1[i]=x1[i][x1[i].find("(") + 1:x1[i].find(")")]
y1=list(devices.values())

x2=list(timebuckets.keys())
y2=list(timebuckets.values())

runDashboard(x1,x2,y1,y2)