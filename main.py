# imports
from bokeh.layouts import layout
from math import sqrt
from bokeh.plotting import figure, curdoc, ColumnDataSource
from bokeh.io import show
from bokeh.models import Button, Slider
from bokeh.events import ButtonClick


def calculateFunction(kp, Ti):

    A = 1.5  # max value in m^2
    beta = 0.035  # m^(5/2)/s
    t_sim = 3600  # simulation time
    Tp = 0.1  # sampling time
    t = [0.0]  # time array
    N = int(t_sim/Tp)+1  # number of samples
    h = [1]  # initial value
    Qd = [0.05]
    Qo = [beta*sqrt(h[-1])]

    hmin = 0.0
    hmax = 5.0

    hz = [2.7]
    e = [0.0]
    u = [0.0]
    dh = 0.03

    for n in range(1, N+1):
        t.append(n*Tp)  # simulation time calc
        e.append(h[-1]-hz[-1])  # error
        u.append(kp*(kp*(e[-1]+Tp/Ti*sum(e))))  # main function
        Qd.append(A*hz[-1]*dh+beta*sqrt(h[-1]))
        h.append(min(max(Tp*(Qd[-1]-Qo[-1])/A+h[-1], hmin), hmax))
        Qo.append(beta*sqrt(h[-1]))
    print("calc", h[1:10])
    return t, h


def bokehPlot():
    doc = curdoc()
    t, h = calculateFunction(14, 1)

    data = {}
    data["time"] = t
    data["force"] = h
    source = ColumnDataSource(data)
    sliderTi = Slider(
        title="Ti value",
        start=0,
        end=15,
        step=0.1,
        value=14
    )
    sliderkp = Slider(
        title="kp value",
        start=0,
        end=3,
        step=0.01,
        value=0.01
    )
    p = figure(width=600, height=300)
    points = p.line(x='time', y='force', source=source, line_width=2)

    def buttonCallback(new):
        t, h = calculateFunction(sliderkp.value, sliderTi.value)

        data = {}
        data["time"] = t
        data["force"] = h
        source = ColumnDataSource(data)
        p.line(x='time', y='force', source=source,
               line_width=2, line_color="green")

    button = Button(label="Generate plot", button_type="success")
    button.on_event(ButtonClick, buttonCallback)

    l = layout(
        [
            [sliderTi],
            [sliderkp],
            [p],
            [button]
        ]
    )
    doc.add_root(l)

    # main operations


# calculateFunction()
# plotValues()
bokehPlot()
