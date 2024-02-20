import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go


def split_dataframe(df, column_name):
    dataframes= {}

    unique_values = df[column_name].unique()
    for value in unique_values:
        dataframes[value] = df[df[column_name] == value]
    
    return dataframes


def control_chart(data, column_name):
    data[column_name] = pd.to_numeric(data[column_name], errors='coerce')
    mean = data[column_name].mean()
    std = data[column_name].std()

    upper_control_limit = mean + 2 * std
    lower_control_limit = mean - 2 * std

    return mean, upper_control_limit, lower_control_limit


def plot_control_chart(dataframe,
                       upper_limit,
                       mean,
                       lower_limit,
                       category,
                       y_axis,
                       x_axis_sep = 5):
    # Create the Plotly figure
    fig = go.Figure()

    # Define the hover template
    hover_template = '<b>Date:</b> %{customdata[3]}<br><b>Area:</b> %{customdata[0]}<br>' \
                     '<b>Tailing:</b> %{customdata[1]}<br>' \
                     '<b>Rt_min:</b> %{customdata[2]}<extra></extra>'

    # Plot the data
    fig.add_trace(go.Scatter(
        x=list(range(1, dataframe.shape[0] + 1)),
        y=dataframe[y_axis],
        mode='lines+markers',
        marker=dict(size=6, color='#ed9439'),
        hovertemplate=hover_template,
        customdata=dataframe[['area','tailing', 'rt_min' , 'date']].values,
        # customdata=dataframe[['Area','Tailing', 'RT [min]']].values,
    ))

 # Plot the control limits as horizontal lines
     # Add vertical lines for control limits
    fig.add_hline(y=upper_limit, line_width=3, line_dash="dash", line_color="red", name='Upper Control Limit')
    fig.add_hline(y=mean, line_width=3, line_dash="dash", line_color="green", name='Mean')
    fig.add_hline(y=lower_limit, line_width=3, line_dash="dash", line_color="blue", name='Lower Control Limit')

    tickvals = list(range(1, len(dataframe) + 1, x_axis_sep))
    # Customize x-axis tick labels
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=tickvals, tickangle=0))
    # fig.update_layout(xaxis=dict(tickmode='array', tickvals=dataframe[x_axis][::x_axis_sep], tickangle=45))

    # Set axis labels and title
    fig.update_layout(xaxis_title= "Data Points", yaxis_title=y_axis, title=f"Control Chart for {category}")


    fig.update_layout(
    hoverlabel=dict(
        bgcolor="white",
        font_color="purple",))
    
    # Render the plot
    st.plotly_chart(fig, use_container_width=True)


# def plot_control_chart_test(dataframe, upper_limit, mean, lower_limit, category, y_axis, x_axis, x_axis_sep=3):
#     # Create the Plotly figure
#     fig = go.Figure()

#     # Define the hover template
#     hover_template = '<b>Date:</b> %{x}<br><b>RT [min]:</b> %{y}<br>' \
#                      '<b>Area:</b> %{customdata[0]}<br>' \
#                      '<b>Tailing:</b> %{customdata[1]}<br><extra></extra>'

#     # Group data by date
#     grouped_data = dataframe.groupby(x_axis)

#     # Plot each date with its associated values
#     for date, group in grouped_data:
#         fig.add_trace(go.Scatter(
#             x=group[x_axis],
#             y=group[y_axis],
#             mode='lines+markers',
#             name=f'Date: {date}',
#             hovertemplate=hover_template,
#             customdata=group[['area', 'tailing']].values,
#         ))

#     # Plot the control limits as horizontal lines
#     fig.add_hline(y=upper_limit, line_width=3, line_dash="dash", line_color="red", name='Upper Control Limit')
#     fig.add_hline(y=mean, line_width=3, line_dash="dash", line_color="green", name='Mean')
#     fig.add_hline(y=lower_limit, line_width=3, line_dash="dash", line_color="blue", name='Lower Control Limit')

#     # Customize x-axis tick labels
#     fig.update_layout(xaxis=dict(tickmode='array', tickvals=dataframe[x_axis][::x_axis_sep], tickangle=45))

#     # Set axis labels and title
#     fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis, title=f"Control Chart for {category}")

#     fig.update_layout(
#         hoverlabel=dict(
#             bgcolor="white",
#             font_color="purple",
#         )
#     )

#     # Render the plot
#     st.plotly_chart(fig, use_container_width=True)





