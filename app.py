import streamlit
import seaborn as sns
import matplotlib.pyplot as plt
from utils import MetricsUtil



metrics = MetricsUtil()

streamlit.set_page_config(page_title="Metrics Explorer", layout="wide")
streamlit.header("Metrics Explorer")

selected_metric_name = streamlit.sidebar.selectbox(label="Select a metric", options=list(metrics.get_metric_names().keys()))

selected_node_id = metrics.metrics_list[selected_metric_name]
node = metrics.manifest["metrics"][selected_node_id]
available_dimensions = node["dimensions"]
available_time_grains = node["time_grains"]

selected_dimensions_list = streamlit.sidebar.multiselect("Select one or more dimensions", options=available_dimensions)
selected_time_grain = streamlit.sidebar.selectbox("Select a time grain", options=available_time_grains)
DEBUG=streamlit.sidebar.checkbox("Debug Mode", value=False)


query = metrics.populate_template_query(
    metric_name=selected_metric_name,
    time_grain=selected_time_grain,
    dimensions_list=selected_dimensions_list
)

with streamlit.spinner("Fetching query results"):
    df = metrics.get_query_results(query)

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
        sns.lineplot(
            x = "PERIOD",
            y = selected_metric_name.upper(),
            data = df
        )
    else:
        sns.lineplot(
            x = "PERIOD",
            y = selected_metric_name.upper(),
            hue=selected_dimensions_list[0].upper(),
            data = df
        )
    col2.pyplot(fig)

col2.dataframe(df)
