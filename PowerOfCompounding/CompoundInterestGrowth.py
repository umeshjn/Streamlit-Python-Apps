## Importing the libraries.
import streamlit as st
import numpy as np
import math
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Add a sliders to the sidebar:
initial_investment = st.sidebar.slider(
    'Initial Investment',
    min_value = 0, max_value = 100000, value= 1000, step = 1000
)

num_years = st.sidebar.slider(
    'Number of Years of Investment',
    min_value = 1, max_value = 100, value= 10, step = 1
)

rate_of_return = st.sidebar.slider(
    'Rate of Yearly Return',
    min_value = 1, max_value = 30, value= 12, step = 1
)

additional = st.sidebar.slider(
    'Additional Yearly Investment',
    min_value = 1000, max_value = 100000, value= 1000, step = 1000
)

### Function to calculate the Compound Interest
## Sample Example 1000 * pow(1.12, 10) + 10000 * ((pow(1.12, 11) - 1.12 ) / 0.12)
def compoundinterest(initial_investment, rate_of_return, additional, num_years):
	returns = []
	for i in range(0, num_years + 1):
		#st.write(round(initial_investment * math.exp((rate_of_return/100) * i), 2))
		if i == 0:
			returns.append(round(initial_investment * math.exp((rate_of_return/100) * i), 0))
		else:
			#st.write(initial_investment, pow(rate_of_return/100 + 1, i), additional, (pow(rate_of_return/100 + 1, i + 1) - (rate_of_return/100 + 1))/ (rate_of_return/100))
			returns.append(round((initial_investment * pow(rate_of_return/100 + 1, i)) + additional * ((pow(rate_of_return/100 + 1, i + 1) - (rate_of_return/100 + 1)) / (rate_of_return/100)), 0))
	return returns

## Creating the DataFrame
data = pd.DataFrame({'Number of Years' : range(0, num_years + 1), "Total Compounded Returns" : compoundinterest(initial_investment, rate_of_return, additional, num_years)})

## Adding Header and Text to the App
st.subheader('Compounded Growth of Returns on Investment')
st.markdown("Albert Einstein once said that Compound interest is the eighth wonder of the world. He who understands it, earns it ... he who doesn't ... pays it..")

st.markdown("Initial Investment of **" + str(initial_investment) + "** growing at compounded rate of **" + str(rate_of_return) + "%** with additional yearly investment of **" + str(additional) + "** becomes **" + str(round((initial_investment * pow(rate_of_return/100 + 1, num_years)) + additional * ((pow(rate_of_return/100 + 1, num_years + 1) - (rate_of_return/100 + 1)) / (rate_of_return/100)), 0)) + "** in **" + str(num_years) + "** of years")

### Adding the plot.
fig = px.line(data, x="Number of Years", y="Total Compounded Returns")
st.plotly_chart(fig)
	
	