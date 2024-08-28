import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load family connections data (dummy data)
@st.cache
def load_data():
    data = {
        "ID": [1, 2, 3, 4, 5],
        "Name": ["John", "Alice", "Bob", "Mary", "Jane"],
        "Parent_ID": [None, None, 1, 1, 2]
    }
    return pd.DataFrame(data)

df = load_data()

# Create a function to generate fan chart
def generate_fan_chart(df, selected_member):
    fig = go.Figure()

    # Add selected member to the fan chart
    fig.add_trace(go.Scatterpolar(
        r=[0.5],
        theta=[0],
        mode='markers',
        marker=dict(
            color='blue',
            size=20,
            line=dict(
                color='black',
                width=2
            )
        ),
        name=selected_member
    ))

    # Add family connections
    connections = df[df["Parent_ID"] == selected_member]["Name"].tolist()
    for i, name in enumerate(connections):
        theta = i * (360 / len(connections))
        fig.add_trace(go.Scatterpolar(
            r=[0.5],
            theta=[theta],
            mode='markers',
            marker=dict(
                color='green',
                size=10,
                line=dict(
                    color='black',
                    width=1
                )
            ),
            name=name
        ))

    # Update layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=False
            )
        ),
        showlegend=False
    )

    return fig

# Streamlit app
st.title("Family Connections Fan Chart")

# Select a family member
selected_member = st.selectbox("Select a family member", df["Name"])

# Generate fan chart
fig = generate_fan_chart(df, selected_member)
st.plotly_chart(fig, use_container_width=True)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& #


##  Plan 2  ##

import streamlit as st
import pandas as pd
import numpy as np

# Create a function to read a GEDCOM file
def read_gedcom(file_path):
  """Reads a GEDCOM file and returns a Pandas DataFrame."""

  with open(file_path, "r") as f:
    gedcom_data = f.readlines()

  # Create a Pandas DataFrame from the GEDCOM data
  df = pd.DataFrame(gedcom_data, columns=["INDI", "NAME", "SEX", "BIRT", "DEAT"])

  return df

# Create a function to create a fan chart
def create_fan_chart(df):
  """Creates a fan chart from a Pandas DataFrame."""

  # Get the number of individuals in the DataFrame
  num_individuals = df.shape[0]

  # Create a list of colors for the fan chart
  colors = np.random.rand(num_individuals)

  # Create a fan chart
  st.altair_chart(
    altair.FanChart(
      data=df,
      theta="NAME",
      radius="SEX",
      color="colors",
    )
  )

# Read the GEDCOM file
df = read_gedcom("gedcom.txt")

# Create a fan chart
create_fan_chart(df)

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& #

## Plan 3 ##

import streamlit as st
import pandas as pd
import numpy as np

# Create a function to read a GEDCOM file
def read_gedcom(file_path):
  """Reads a GEDCOM file and returns a Pandas DataFrame."""

  with open(file_path, "r") as f:
    gedcom_data = f.readlines()

  # Create a Pandas DataFrame from the GEDCOM data
  df = pd.DataFrame(gedcom_data, columns=["INDI", "NAME", "SEX", "BIRT", "DEAT"])

  return df

# Create a function to create a fan chart
def create_fan_chart(df):
  """Creates a fan chart from a Pandas DataFrame."""

  # Get the number of individuals in the DataFrame
  num_individuals = df.shape[0]

  # Create a list of colors for the fan chart
  colors = np.random.rand(num_individuals)

  # Create a fan chart
  st.altair_chart(
    altair.FanChart(
      data=df,
      theta="NAME",
      radius="SEX",
      color="colors",
    ).configure_axis(
      labelAngle=0,
      titleFontSize=16,
      labelFontSize=12,
    )
  )

# Read the GEDCOM file
df = read_gedcom("gedcom.txt")

# Create a fan chart
create_fan_chart(df)