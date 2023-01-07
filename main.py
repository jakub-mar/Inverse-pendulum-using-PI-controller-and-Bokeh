# imports
from bokeh.layouts import layout
from bokeh.plotting import figure, curdoc, ColumnDataSource
from bokeh.io import show
from bokeh.models import Button, Slider, Span, PreText, RangeSlider
from bokeh.events import ButtonClick
import numpy as np

text = PreText(text='Autorzy: Jakub Marciniak, Szymon Sobczak')


def calculateInversePendulum(kp, Ti, targetValue, t_sim, minMomentum=-1000, maxMomentum=1000):
    m = 0.05
    l = 0.15
    g = 9.81
    b = 1.2
    Tp = 0.1

    t = [-0.2, -0.1, 0.0, ]
    N = int(t_sim/Tp) + 1

    Theta_min = -90
    Theta_max = 90
    tau_max = 1
    tau_min = -1
    Umax = 2
    Umin = -2

    tau = [0.0, 0.0]
    Theta = [90, 90, 90]
    e = [0.0, ]
    U = [0.0, ]

    for n in range(1, N):
        e.append(targetValue-Theta[-1])
        U.append(kp*(e[n]+(Tp/Ti))*sum(e))
        tau.append(np.clip(U[n], minMomentum, maxMomentum))
        t.append(n*Tp)
        Theta.append(np.clip((Tp**2 * tau[-1] - 2*m*(l**2)*Theta[-1] + m*(
            l**2)*Theta[-2] - m*g*l*np.sin(Theta[-1]))/(Tp*b - m*(l**2)), Theta_min, Theta_max))

    return Theta, t, e, U, tau


sliderTi = Slider(
    title="Wartość Ti * 100",
    start=-0.9,
    end=0.9,
    step=0.1,
    value=0.1,
    width=600,
    show_value=True
)

sliderkp = Slider(
    title="Wartość Kp",
    start=0,
    end=0.3,
    step=0.01,
    value=0.05,
    width=600,
    show_value=True
)

targetValueSlider = Slider(
    title="Kąt zadany",
    start=-90,
    end=90,
    step=1,
    value=-75
)

timeValueSlider = Slider(
    title="Czas symulacji",
    start=0,
    end=100,
    step=1,
    value=10
)

momentumRangeSlider = RangeSlider(
    start=-1000, end=1000, value=(-1000, 1000), step=1, title="Zakres momentu"
)

plot1 = figure(width=700, height=410, title='Wykres regulacji kąta w czasie')
plot1.xaxis.axis_label = 'Czas [s]'
plot1.yaxis.axis_label = 'Theta [deg]'

plot2 = figure(width=500, height=270, title='Wykres uchybu')
plot2.xaxis.axis_label = 'Czas [s]'
plot2.yaxis.axis_label = 'Wartość uchybu'

plot3 = figure(width=500, height=270, title='Wykres momentu napędowego')
plot3.xaxis.axis_label = 'Czas [s]'
plot3.yaxis.axis_label = 'Moment napędowy [Nm]'

tauSource = ColumnDataSource({"time": [0.0], "tau": [0.0]})
eSource = ColumnDataSource({"time": [0.0], "e": [0.0]})
mainSource = ColumnDataSource({'time': [0], 'angle': [0]})
prevSource = ColumnDataSource({'time': [0], 'angle': [0]})


mainPlot = plot1.line(x='time', y='angle', source=mainSource,
                      line_width=2, line_color="red", legend_label='Aktualna regulacja')
prevPlot = plot1.line(x='time', y='angle', source=prevSource,
                      line_width=2, line_color="blue", legend_label='Poprzednia regulacja')

targetPlot = Span(location=targetValueSlider.value,
                  dimension='width', line_color='green',
                  line_dash='dashed', line_width=1)

eplot = plot2.line(x='time', y='e', source=eSource)

tauPlot = plot3.line(x='time', y='tau', source=tauSource)

plot1.line([0], [0], legend_label='Kąt zadany',
           line_dash='dashed', line_color="green", line_alpha=1)
plot1.add_layout(targetPlot)


def bokehPlot():
    global mainPlot, prevPlot, mainSource, prevSource, targetPlot, eplot, eSource, tauPlot, tauSource
    doc = curdoc()
    theta, t, e, U, tau = calculateInversePendulum(0.05, 0.001, -75, 10)

    mainSource = ColumnDataSource({"time": t, "angle": theta})
    eSource = ColumnDataSource({"time": t, "e": e})
    tauSource = ColumnDataSource({"time": t, "tau": tau})

    mainPlot = plot1.line(x='time', y='angle', source=mainSource,
                          line_width=2, line_color="red", legend_label='Aktualna regulacja')
    prevPlot = plot1.line(x='time', y='angle', source=prevSource,
                          line_width=2, line_color="blue", legend_label='Poprzednia regulacja')
    eplot = plot2.line(x='time', y='e', source=eSource)
    tauPlot = plot3.line(x='time', y='tau', source=tauSource)

    button = Button(label="Generate plot", button_type="success")
    button.on_event(ButtonClick, buttonCallback)

    l = layout(
        [
            [plot1, [sliderTi, sliderkp, targetValueSlider,
                     timeValueSlider, momentumRangeSlider, button]],
            [plot2, plot3],
            [text]
        ]
    )
    doc.add_root(l)

    # main operations


def buttonCallback(new):
    global mainSource, prevPlot, mainPlot, prevSource, targetPlot, eSource, tauSource
    theta, t, e, u, tau = calculateInversePendulum(
        sliderkp.value, sliderTi.value/100, targetValueSlider.value, timeValueSlider.value, momentumRangeSlider.value[0], momentumRangeSlider.value[1])

    prevSource.data = dict(mainSource.data)
    mainSource.data = {'time': t, 'angle': theta}
    eSource.data = {'time': t, 'e': e}
    tauSource.data = {'time': t, 'tau': tau}
    targetPlot.location = targetValueSlider.value


bokehPlot()


# bokeh serve --show main.py
