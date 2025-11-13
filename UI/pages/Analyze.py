import matplotlib.pyplot as plt
import seaborn as sns
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from BL.service_methods import *
from UI.plotting import create_multi_channel_plot, create_plot


def corr_page(df: pd.DataFrame):

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

    if selected_df.empty:
        return

    c_list = get_channels(df)
    st.header("Correlation matrix")
    fig, ax = plt.subplots()
    sns.heatmap(get_corr(df, c_list), ax=ax, annot=True)
    st.write(fig)

    # pair plot takes too much time
    # fig = sns.pairplot(df[df.columns[1:]], hue="anomaly")
    # st.pyplot(fig)

    # st.text("")
    st.header("Pairs Of Channel")

    c_list_2 = c_list.copy()
    c_list_2.insert(0, 'None')
    channel = st.selectbox("Select channel 1:", c_list)
    channel2 = st.selectbox("Select channel 2:", c_list_2)
    channels = [channel]
    if channel2 != 'None':
        channels.append(channel2)
    # 'time', 'channel', 'value', 'label'
    df_4_multi_ch = prepare_for_channel_correlation(selected_df, channels)
    st.subheader("channel over time")
    # fig = px.line(df_4_plot, x="Index", y=channels, title="", color='Date')
    fig = create_multi_channel_plot(df_4_multi_ch, channels)
    st.plotly_chart(fig)

    st.subheader('Channels Relationship')
    fig = create_plot(df_4_multi_ch, channels[0], channels[-1], plot_type="scatter", color_col='label')
    st.plotly_chart(fig)
    # fig, ax = plt.subplots()
    # sns.scatterplot(x=channels[0], y=channels[-1], hue='label', data=df_4_multi_ch, ax=ax) # hue="label"
    # st.write(fig)
    # fig = sns.lmplot(x=channels[0], y=channels[-1], hue="anomaly", data=df_4_multi_ch)


def missing_data_analysis(df: pd.DataFrame):

    # txt = st.text_area('Text to analyze', '''
    #      It was the best of times, it was the worst of times, it was
    #      the age of wisdom, it was the age of foolishness, it was
    #      the epoch of belief, it was the epoch of incredulity, it
    #      was the season of Light, it was the season of Darkness, it
    #      was the spring of hope, it was the winter of despair, (...)
    #      ''')

    with st.expander("⚙️  First section of missing labels ", expanded=True):
        st.write(
            """    
    - first 8831 samples are missing labels.
    - why filling the missing labels is dangerous:
        - filling missing labels and use them for training can be very harmful.
        - as apposed to fill missing labels, fill missing channel values is more reasonable because we have all other channels corret information we could gain from. 
        - filling missing labels to be used as ground truth for training can make the model learn incorrectly.
        - using spicules ground truth for training can hurt the model generalization.
    - if needed to fill them:
        - using only the labeled data.
        - I would perform first temporal abstraction.
            - Shapelets
            - search for frequent TIRPS (Time Intervals Related Patterns) 
            - symbolic time series - first convert the time series to PAA representation, then convert the PAA to symbols (SAX)
            - Clustering method could be performed on symbolic time series (compute pairwise distance)
        - then train ML model bsed on the new temporal features.
        - then predict for the missing samples and fill them according to probability of the trained model.
            """
        )

    with st.expander("⚙️  Second section of 'holes' in labels ", expanded=True):
        st.write(
            """    
    - after index 8831 we could see holes in the 'label' column. 
    - But after looking into the data we can see that all of those samples with missing label are duplicates of adjacent samples, so we removed them.
            """
        )