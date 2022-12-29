# imports
from bokeh.layouts import layout
from math import sqrt
from bokeh.plotting import figure, curdoc, ColumnDataSource
from bokeh.io import show
from bokeh.models import Button, Slider
from bokeh.events import ButtonClick
import math
import numpy as np
import matplotlib.pyplot as plt
import copy


def calculateInversePendulum(kp, Ti):
    m = 0.05
    l = 0.15
    g = 9.81
    b = 1.2
    Tp = 0.1
    t_sim = 10

    t = [-0.2, -0.1, 0.0, ]
    N = int(t_sim/Tp) + 1

    Theta_min = -90
    Theta_max = 90
    tau_max = 1
    tau_min = -1
    Umax = 2
    Umin = -2

    Theta_zad = -75
    tau = [0.0, 0.0]
    Theta = [90, 90, 90]
    e = [0.0, ]
    U = [0.0, ]

    for n in range(1, N):
        e.append(Theta_zad-Theta[-1])
        U.append(kp*(e[n]+(Tp/Ti))*sum(e))
        tau.append(U[n])
        t.append(n*Tp)
        Theta.append(np.clip((Tp**2 * tau[-1] - 2*m*(l**2)*Theta[-1] + m*(
            l**2)*Theta[-2] - m*g*l*np.sin(Theta[-1]))/(Tp*b - m*(l**2)), Theta_min, Theta_max))

    return Theta, t


sliderTi = Slider(
    title="Ti value * 100",
    start=0,
    end=1,
    step=0.05,
    value=0.1
)
sliderkp = Slider(
    title="kp value",
    start=0,
    end=0.3,
    step=0.01,
    value=0.05
)
plot1 = figure(width=600, height=300)
plot2 = figure(width=600, height=300)
data = {'time': [0], 'angle': [0]}
data2 = {'time': [0], 'angle': [0.0]}
mainSource = ColumnDataSource(data)
prevSource = ColumnDataSource(data2)

mainPlot = plot1.line(x='time', y='angle', source=mainSource,
                      line_width=2, line_color="red")
prevPlot = plot2.line(x='time', y='angle', source=prevSource,
                      line_width=2, line_color="blue")


def bokehPlot():
    global mainPlot, prevPlot, mainSource, prevSource
    doc = curdoc()
    theta, t = calculateInversePendulum(0.05, 0.001)

    data = {}
    data["time"] = t
    data["angle"] = theta
    mainSource = ColumnDataSource(data)

    mainPlot = plot1.line(x='time', y='angle', source=mainSource,
                          line_width=2, line_color="red")
    prevPlot = plot2.line(x='time', y='angle', source=prevSource,
                          line_width=2, line_color="blue")

    button = Button(label="Generate plot", button_type="success")
    button.on_event(ButtonClick, buttonCallback)

    l = layout(
        [
            [sliderTi],
            [sliderkp],
            [plot1, plot2],
            [button]
        ]
    )
    doc.add_root(l)

    # main operations


def buttonCallback(new):
    global mainSource, prevPlot, mainPlot, prevSource
    theta, t = calculateInversePendulum(sliderkp.value, sliderTi.value/100)

    newData = {}
    newData["time"] = t
    newData["angle"] = theta

    prevSource.data = dict(mainSource.data)
    mainSource.data = newData


bokehPlot()


# bokeh serve --show main.py
