import streamlit
import seaborn as sns
import matplotlib.pyplot as plt
from utils import MetricsUtil


metrics = MetricsUtil()

streamlit.set_page_config(page_title="Metrics Explorer", layout="wide")
streamlit.header("Metrics Explorer")

selected_metric_name = streamlit.sidebar.selectbox(
    label="Select a metric", options=list(metrics.get_metric_names().keys())
)

selected_node_id = metrics.metrics_list[selected_metric_name]
node = metrics.manifest["metrics"][selected_node_id]
available_dimensions = node["dimensions"]
available_time_grains = node["time_grains"]

selected_dimensions_list = streamlit.sidebar.multiselect(
    "Select one or more dimensions", options=available_dimensions
)
selected_time_grain = streamlit.sidebar.selectbox(
    "Select a time grain", options=available_time_grains
)


calculation_options = [
    'metrics.period_over_period(comparison_strategy="ratio", interval=1)',
    'metrics.period_over_period(comparison_strategy="difference", interval=1)',
    'metrics.rolling(aggregate="max", interval=1)',
    'metrics.rolling(aggregate="min", interval=1)',
]
secondary_calcs_list = streamlit.sidebar.multiselect(
    "Select secondary calculations", options=calculation_options
)

DEBUG = streamlit.sidebar.checkbox("Debug Mode", value=False)

with streamlit.spinner("Building project"):
    streamlit.sidebar.button("Rerun Project", on_click=metrics._run_project())

query = metrics.populate_template_query(
    metric_name=selected_metric_name,
    time_grain=selected_time_grain,
    dimensions_list=selected_dimensions_list,
    secondary_calcs_list="[" + ",".join(secondary_calcs_list) + "]",
)

with streamlit.spinner("Fetching query results"):
    df = metrics.get_query_results(query)
    df.columns = [c.lower() for c in df.columns]

col1, col2 = streamlit.columns(2)

col1.subheader(selected_metric_name)
col1.text(node["description"])
col1.subheader("dbt Query")
col1.text(query)

if DEBUG:
    compiled = metrics._get_compiled_query(query)
    col1.text(compiled)
    col1.dataframe(df)

col2.subheader("Data Figure")
with streamlit.spinner("Plotting results"):
    fig = plt.figure(figsize=(10, 4))
    if len(selected_dimensions_list) == 0:
        sns.lineplot(x="period", y=selected_metric_name.lower(), data=df)
    else:
        sns.lineplot(
            x="period",
            y=selected_metric_name.lower(),
            hue=selected_dimensions_list[0].lower(),
            data=df,
        )
    col2.pyplot(fig)

col2.dataframe(df)
