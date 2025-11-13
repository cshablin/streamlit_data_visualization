import streamlit as st
from PIL import Image

from BL.service_methods import clean_df
from UI.downloads import dataframe_picker
from UI.pages.Analyze import corr_page, missing_data_analysis
from UI.pages.visualize import distribution_page
from common.logger import Logger

st.set_page_config(page_icon="", page_title="Data analysis") #  , layout = "wide"

image = Image.open('resources\\my_logo.png')
st.image(
    image,
    # width=300,
)
st.title("Temporal Data Analysis")

logger = Logger()
logger.info("Temporal Data Analysis start!")

df = dataframe_picker()
df = clean_df(df)
# st.info(f"""DataFrame head view""")
# st.write(df.head())

# uploaded_file = st.file_uploader()
# if uploaded_file is not None:
#     st.caching.MemoAPI.clear()  # we have caching so we clear
#     dataframe = pd.read_csv(uploaded_file)
#     st.info(f"""DataFrame view""")
#     st.write(dataframe.head())
# else:
#     st.info(f"""👆 select csv file """)
#     st.stop()


st.markdown('<style>' + open('UI//style//bootstrap.min.css').read() + '</style>', unsafe_allow_html=True)

query_params = st.experimental_get_query_params()
tabs = ["Distribution", "Correlation", "Missing data"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Distribution"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Distribution")
    active_tab = "Distribution"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Distribution":
    distribution_page(df)
elif active_tab == "Correlation":
    corr_page(df)
elif active_tab == "Missing data":
    missing_data_analysis(df)
else:
    st.error("Something is wrong.")
