import datetime
import plotly.express as px
import plotly.graph_objects as go
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from BL.service_methods import *


def distribution_page(df: pd.DataFrame):

    c29, c30 = st.columns([1.3, 6])
    with c29:
        # st.info("Filter dates")
        import datetime as dt
        _from, _to = get_time_range(df)
        _to += dt.timedelta(minutes=1)
        begin_date = st.time_input('Start time', _from)
        begin_time = st.date_input("Start date", value=_from, min_value=_from, max_value=_to, key=None, help=None, on_change=None)
        end_date = st.time_input('End time', _to)
        end_time = st.date_input("End date", value=_to, min_value=_from, max_value=_to, key=None, help=None, on_change=None)
    with c30:

        begin = datetime.combine(begin_time, begin_date)
        end = datetime.combine(end_time, end_date)
        df_filtered = df[(df['datetime'] >= begin) & (df['datetime'] <= end)]
        from st_aggrid import GridUpdateMode, DataReturnMode
        gb = GridOptionsBuilder.from_dataframe(df_filtered)
        # enables pivoting on all columns, however i'd need to change ag grid to allow export of pivoted/grouped data, however it select/filters groups
        gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
        gb.configure_selection(selection_mode="multiple", use_checkbox=True)
        gb.configure_side_bar()  # side_bar is clearly a typo :) should by sidebar
        grid_options = gb.build()

        st.success(
            f"""
                💡 Tip! Hold the shift key when selecting multiple rows!
                """
        )

        response = AgGrid(
            df_filtered,
            gridOptions=grid_options,
            enable_enterprise_modules=True,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            fit_columns_on_grid_load=False,
        )

        selected_df = pd.DataFrame(response["selected_rows"])

        # st.subheader("Filtered data 👇 used for analysis")
        # st.text("")
        # df_head = selected_df.head()
        # # st.table(df_head.iloc[:, :-3])
        # st.table(df_head)
        # st.text("")

    c29, c30 = st.columns([1.3, 6])

    with c29:
        # select channels for distribution show
        if selected_df.empty:
            return
        else:
            l_list = get_labels(selected_df)
            l_list.insert(0, 'All')
            selected_channel = st.selectbox("Select label/s:", l_list)

    # st.text("")
    st.header("Channels normalized Distributions")
    df_4_distribution = prepare_for_distribution_per_channel(selected_df)
    if selected_channel != 'All':
        df_4_distribution = df_4_distribution[df_4_distribution['label'] == selected_channel]
    # 'channel', 'value', 'label'
    fig = px.violin(df_4_distribution, x="channel", y="value", color='label')
    st.plotly_chart(fig)

    c29, c30 = st.columns([1.3, 6])

    with c30:
        st.header("General statistics per channel")
        channels = get_channels(df)
        for channel in channels:
            fig = go.Figure()
            fig.add_trace(go.Box(
                y=df[channel],
                name=channel,
                boxmean='sd'  # represent mean and standard deviation
            ))

            # fig = px.box(df, y=channel)
            st.plotly_chart(fig)
