from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse
from plotly import graph_objects as go

from plotly.graph_objs import Figure


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

COUNT= 100

def plot_fig(count: int= COUNT):
    xs = list(range(COUNT))
    ys = list((x-COUNT//2)**2 for x in xs)

    count = min(COUNT,count)
    count = max(0,count)
    trace = go.Scatter(
        x=xs[0:count-1],
        y=ys[0:count-1],
        mode='markers+lines',
        name='y = (x-50)^2',
        marker=dict(size=8, color='navy', opacity=0.5)
    )

    layout = go.Layout(
        xaxis=dict(title='x'),
        yaxis=dict(title='y'),
        dragmode='lasso',
        hovermode='closest'
    )

    fig = go.Figure(data=[trace], layout=layout)

    fig.update_layout(
        dragmode='select',
        showlegend=True,
        newshape=dict(line_color='cyan'),
        selectdirection='any'
    )

    return fig


@app.post('/plot', response_class=JSONResponse)
def plot():
    fig: Figure = plot_fig()
    return {"plotly_json": fig.to_json(), "htmx_html": '<b>Hello World</b>'}


@app.post('/hello', response_class=HTMLResponse)
def hello():
    return "<em>Hello, Good Morning!</em>"
