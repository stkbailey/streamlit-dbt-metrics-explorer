import streamlit
import seaborn as sns
import matplotlib.pyplot as plt
from utils import MetricsUtil


metrics = MetricsUtil()

streamlit.set_page_config(page_title="Metrics Explorer", page_icon="🔥")
streamlit.header("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥")
streamlit.header("The X-treme MetriX X-plorer (XMXX)")

selected_metric_name = streamlit.sidebar.selectbox(
    label="Select a metric", options=sorted(list(metrics.get_metric_names().keys()))
)

selected_node_id = metrics.metrics_list[selected_metric_name]
node = metrics.manifest["metrics"][selected_node_id]
available_dimensions = node["dimensions"]
available_time_grains = node["time_grains"]

selected_dimension = streamlit.sidebar.radio(
    "Select a dimension", options=["none"] + available_dimensions
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

# with streamlit.spinner("Running Models"):
#     streamlit.sidebar.button("Rerun Models", on_click=metrics._run_project())
streamlit.sidebar.markdown("🔥 [Blog](https://stkbailey.substack.com/p/kicking-the-tires-on-dbt-metrics?r=a3d32&utm_campaign=app&utm_medium=web)")
streamlit.sidebar.markdown("🔥 [GitHub](https://github.com/stkbailey/streamlit-dbt-metrics-explorer)")
streamlit.sidebar.markdown("🔥 [Theme Song](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
streamlit.sidebar.image("assets/fire-2.jpeg")
DEBUG = streamlit.sidebar.checkbox("Debug Mode", value=False)


def get_min_max_dates(metric_name):
    if "substack" in metric_name:
        return "2021-12-01", "2022-03-01"
    return "2016-01-01", "2021-10-01"


min_date, max_date = get_min_max_dates(selected_metric_name)
if selected_dimension == "none":
    selected_dimensions_list = []
else:
    selected_dimensions_list = [selected_dimension]
query = metrics.populate_template_query(
    metric_name=selected_metric_name,
    time_grain=selected_time_grain,
    dimensions_list=selected_dimensions_list,
    secondary_calcs_list="[" + ",".join(secondary_calcs_list) + "]",
    min_date=min_date,
    max_date=max_date,
)

with streamlit.spinner("Fetching query results"):
    df = metrics.get_query_results(query)
    df.columns = [c.lower() for c in df.columns]

streamlit.subheader(node["label"])
streamlit.markdown(node["description"])
streamlit.markdown(f'This metric is based on the model {node["model"]}. It is a {node["type"]} metric based on the column {node["sql"]}.')


if DEBUG:
    compiled = metrics._get_compiled_query(query)
    streamlit.subheader("Compiled SQL")
    streamlit.text(compiled)

with streamlit.spinner("Plotting results"):
    fig, ax = plt.subplots(1, 1, figsize=(10, 4))
    if selected_dimension == "none" == "none":
        sns.lineplot(x="period", y=selected_metric_name.lower(), data=df)
    else:
        sns.lineplot(
            x="period",
            y=selected_metric_name.lower(),
            hue=selected_dimension.lower(),
            data=df,
        )
    ax.set_title(selected_metric_name)
    streamlit.pyplot(fig,  title=selected_metric_name)

streamlit.subheader("Data Table")
streamlit.dataframe(df)

streamlit.subheader("dbt Query")
streamlit.text(query)


streamlit.image("assets/fire-header.jpeg", use_column_width="always")
