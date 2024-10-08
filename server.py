from typing import Annotated
from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from plotly import graph_objects as go
from random import random

from plotly.graph_objs import Figure


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

COUNT= 300
xs: list[int] = list(range(COUNT))
ys: list[float] = []

def reset_ys():
    global ys
    ys = list(float((x-COUNT//2)**2 + 500) for x in xs)
    for x in xs:
        ys[x] = ys[x] * (1 + random()/4)

reset_ys()

def plot_fig(count: int=COUNT):

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


@app.get('/hello', response_class=HTMLResponse)
def hello():
    return "<em>Hello, Good Morning!</em>"

@app.get('/plot', response_class=HTMLResponse)
def plot(count: int=COUNT):
    fig: Figure = plot_fig(count)
    return f"""<script id="plotly-json">{fig.to_json()}</script><b>Hello World</b>"""

@app.post('/reset_plot')
def reset_plot():
    reset_ys()
    return RedirectResponse(url='/plot', status_code=303)

@app.post('/update_plot')
def update_plot(xs: Annotated[list[int], Form()]):
    for x in xs:
        ys[x] = ys[x] * (1 + random() / 2)
    return RedirectResponse(url='/plot', status_code=303)

@app.post('/calculate_plot_statistics', response_class=HTMLResponse)
def calculate_plot_statistics(ys: Annotated[list[float], Form()]):
    return f'{sum(ys)/len(ys)}'
