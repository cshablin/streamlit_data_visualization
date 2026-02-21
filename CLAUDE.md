# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the App

```bash
streamlit run main.py
```

The app uses query params for tab navigation (`?tab=Distribution`, `?tab=Correlation`, `?tab=Missing data`).

## Setup

Python 3.8 is required (pinned in requirements.txt).

```bash
pip install -r requirements.txt
```

Key dependencies: `streamlit~=1.10.0`, `streamlit-aggrid~=0.3.2`, `pandas~=1.4.3`, `plotly~=5.9.0`, `scikit-learn~=1.1.1`, `altair<5`.

## Architecture

Three-layer architecture:

- **`main.py`** — App entry point. Handles file upload via `dataframe_picker()`, cleans the DataFrame with `clean_df()`, and routes to page functions based on the active tab.
- **`BL/service_methods.py`** — Business logic layer. All data transformation functions decorated with `@st.cache`. Exports everything via `*` (wildcard import used in UI pages).
- **`UI/`** — Presentation layer:
  - `pages/visualize.py` — `distribution_page()`: violin plots and box plots per channel.
  - `pages/Analyze.py` — `corr_page()`: correlation heatmap + multi-channel time plots; `missing_data_analysis()`: static text analysis.
  - `plotting.py` — Plotly helper functions (`create_plot`, `create_multi_channel_plot`).
  - `downloads.py` — `dataframe_picker()` for CSV file upload.
- **`common/`** — Infrastructure:
  - `config.py` / `config_base.py` — Singleton `Config` that reads/writes `data_analysis.json` in the working directory. Supports `reload()` and `update(persist=True)`.
  - `logger.py` — `Logger` wraps Python logging with rotating file handler (`log/temporal_analysis.log`).
  - `data_types.py` — `DataLoadType` enum and `DataSourcePointer` for DB connection config.
  - `jsonable.py` — Base class for objects that serialize to/from dicts.

## Data Shape

The app expects a CSV with:
- A `datetime` column (parsed with `pd.to_datetime`)
- Channel columns: `Accelerometer1RMS`, `Accelerometer2RMS`, `Current`, `Pressure`, `Temperature`, `Thermocouple`, `Voltage`, `Volume Flow RateRMS`
- A label column (second-to-last column)
- A trailing redundant column (last column, dropped on load)

`clean_df()` drops the last column, fills the first block of unlabeled rows with label `2`, fills remaining NaN with `0`, drops duplicates, and parses `datetime`.

## Known Issues

- `get_channels()` in `BL/service_methods.py` has a hardcoded return before `return list(df.columns[1:-1])`, making the channel list static rather than dynamic.
- `UI/downloads.py` uses the deprecated `st.caching.MemoAPI` API (removed in Streamlit 1.x+).
- `@st.cache` (used throughout `BL/service_methods.py`) is deprecated in newer Streamlit versions; the replacement is `@st.cache_data`.
- `main.py` uses `st.experimental_get_query_params` / `st.experimental_set_query_params`, which are deprecated.

## Configuration

`Config` is a singleton loaded from `data_analysis.json` in the working directory. On first run the file is created with defaults. Logging behavior is controlled by `PRINT_TO_CONSOLE` and `LOGGING_LEVEL` fields.
