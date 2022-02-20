import streamlit
import seaborn as sns
import matplotlib.pyplot as plt
from utils import MetricsUtil


DEBUG=True

metrics = MetricsUtil()

streamlit.set_page_config(page_title="Metrics Explorer", layout="wide")
streamlit.header("Metrics Explorer")

selected_metric_name = streamlit.sidebar.selectbox(label="Select a metric", options=list(metrics.get_metric_names().keys()))

selected_node_id = metrics.metrics_list[selected_metric_name]
node = metrics.manifest["metrics"][selected_node_id]
available_dimensions = node["dimensions"]
available_time_grains = node["time_grains"]

selected_dimensions_list = [streamlit.sidebar.selectbox("Select a dimension", options=available_dimensions)]
selected_time_grain = streamlit.sidebar.selectbox("Select a time grain", options=available_time_grains)

query = metrics.populate_template_query(
    metric_name=selected_metric_name,
    time_grain=selected_time_grain,
    dimensions_list=selected_dimensions_list
)

col1, col2 = streamlit.columns(2)

col2.text(query)

if DEBUG:
    compiled = metrics._get_compiled_query(query)
    col2.text(compiled)

df = metrics.get_query_results(query)

if DEBUG:
    col1.dataframe(df)

fig = plt.figure(figsize=(10, 4))
sns.lineplot(
    x = "PERIOD",
    y = selected_metric_name.upper(),
    hue=selected_dimensions_list[0].upper(),
    data = df
)
col1.pyplot(fig)

col1.dataframe(df)
