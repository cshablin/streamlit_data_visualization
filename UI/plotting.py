from typing import List
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots


def create_plot(df: pd.DataFrame, x_col: str, y_col: str, plot_type: str = "line", color_col: str = None):
    if plot_type == 'line':
        return px.line(df, x=x_col, y=y_col, title="", color=color_col)
    elif plot_type == 'scatter':
        return px.scatter(df, x=x_col, y=y_col, title="", color=color_col)


def create_multi_channel_plot(df_4_plot: pd.DataFrame, channels: List[str]):
    # 'time', 'channel1', 'channel1', 'label'
    if len(channels) == 1:
        return create_plot(df_4_plot, 'time', channels[0], plot_type="line", color_col='label')
        # return create_plot(df_4_plot, "Index", channels[0], plot_type="line", color_col='Date')
        # return px.line(df_4_plot, x="Index", y=channels[0], title="", color='Date')
    channel_1 = channels[0]
    channel_2 = channels[1]
    subfig = make_subplots(specs=[[{"secondary_y": True}]], shared_yaxes=True)

    # create two independent figures with px.line each containing data from multiple columns
    fig = create_plot(df_4_plot, "time", channel_1, plot_type="line", color_col='label')
    fig2 = create_plot(df_4_plot, "time", channel_2, plot_type="line", color_col='label')
    # fig = px.line(df_4_plot, x="Index", y=channel_1, title="", color='Date')
    # fig2 = px.line(df_4_plot, x="Index", y=channel_2, title="", color='Date')
    fig2.update_traces(yaxis="y2")
    traces = fig.data + fig2.data

    subfig.add_traces(traces)
    subfig.update_layout(hovermode='x unified')
    # subfig.update_layout(hovermode='x')

    subfig.layout.xaxis.title = "Time"
    subfig.layout.yaxis.title = channels[0]
    subfig.layout.yaxis2.title = channels[1]
    # recoloring is necessary otherwise lines from fig und fig2 would share each color
    subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
    return subfig
