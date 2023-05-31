import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


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

    upper_control_limit = mean + 3 * std
    lower_control_limit = mean - 3 * std

    return mean, upper_control_limit, lower_control_limit


def plot_control_chart(dataframe,
                       upper_limit,
                       mean,
                       lower_limit,
                       category = 'Complete Data',
                       y_axis = 'Normalized Area',
                       x_axis = 'Date',
                       x_axis_sep = 3):
    # Plot the data
    fig, ax = plt.subplots()
    sns.lineplot(x= x_axis, y=y_axis, data=dataframe, marker= 'o', markersize = 4, color = 'purple')

    # Plot the control limits
    ax.axhline(upper_limit, color='red', linestyle='--')
    ax.axhline(mean, color='green', linestyle='--')
    ax.axhline(lower_limit, color='blue', linestyle='--')
    plt.xticks(dataframe['Time'][::x_axis_sep], rotation = 45)

        # Add labels with fixed position
    ax.text(0.01, upper_limit + 0.2, 'Upper Control Limit', color='red')
    ax.text(0.01, mean + 0.2, 'Mean', color='green')
    ax.text(0.01, lower_limit + 0.2, 'Lower Control Limit', color='blue')

    # Add labels and title
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"Control Chart for {category}")

    # Add legend
    ax.legend()

    # Display the plot
    st.pyplot(fig)