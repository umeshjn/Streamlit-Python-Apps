## Loading the Libraries
import streamlit as st
import numpy as np
import math
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from bokeh.io import show
from bokeh.layouts import row
from bokeh.models import LogColorMapper
from bokeh.palettes import Plasma3 as palette
from bokeh.plotting import figure

from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment


### List of all the states of United States of America
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

	
### Adding the text to sidebar
st.sidebar.markdown("Unemployment is one of the biggest problems of every single country in the world. How USA has been fairing and which states in USA have done better job?")	

### Adding Selectbox to the sidebar
option = st.sidebar.selectbox(
     'Select the State which you want to explore',
     states)
	 
### Filterting the dataset based on select "State" and creating the dataframe
counties = {
    code: county for code, county in counties.items() if county["state"] == option.lower()
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

county_names = [county['name'] for county in counties.values()]
county_rates = [unemployment[county_id] for county_id in counties]
color_mapper = LogColorMapper(palette=palette)

data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
)


d = pd.DataFrame(data)

tp = d[['name', 'rate']].sort_values('rate', ascending=False).head(15)
lp = d[['name', 'rate']].sort_values('rate').head(15)

### Adding the Counties with Highest and Lowest Rate
st.sidebar.markdown("County with highest rate : " + tp['name'].iloc[0])
st.sidebar.markdown("County with lowest rate : " + lp['name'].iloc[0])


### Adding the Header and plotting
st.subheader("Unemployment Rates in the State of " + option.upper())
p1 = figure(
	plot_width=550, plot_height=550,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Unemployment rate)", "@rate%"), ("(Long, Lat)", "($x, $y)")
    ])
p1.grid.grid_line_color = None
p1.hover.point_policy = "follow_mouse"

p1.patches('x', 'y', source=data,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)
st.bokeh_chart(p1)

## Highest and Lowest barplots
fig = go.Figure()
fig.add_trace(go.Bar(
    y=tp.rate,
    x=tp.name,
    name='Arrested',
    marker_color='darkblue'
))
fig.update_layout(title_text='Counties with Highest Unemployment Rate in the state of ' + option.upper())
st.plotly_chart(fig)

fig = go.Figure()
fig.add_trace(go.Bar(
    y=lp.rate,
    x=lp.name,
    name='Arrested',
    marker_color='cornflowerblue'
))
fig.update_layout(title_text='Counties with Lowest Unemployment Rate in the state of ' + option.upper())
st.plotly_chart(fig)

