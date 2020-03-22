## Importing the libraries.
import streamlit as st
import numpy as np
import math
import pandas as pd


## Adding the header or title
st.header("Coffee Can Investing - Buy Right and Sit Tight Approach")

## Using this to add a newline
st.markdown(' ')

st.markdown("> … the coffee can portfolio is designed to protect you against yourself—the obsession with checking stock prices, the frenetic buying and selling, the hand-wringing over the economy and bad news. It forces you to extend your time horizon. You don’t put anything in your coffee can you don’t think is a good 10-year bet. - **Chris Mayer** ")

## Using this to add a newline
st.markdown(' ')

st.markdown('Investing in stock market is not as complicated as it sounds. But like every thing in this beautiful world, simple things are not the most easiest things to do. Millions of people who want to be like Buffet know that his principles are simple but not easy to replicate. One way of replicating is investing in well run companies and sitting on it tightly for atleast 10 years without churning the portfolio which is the concept of Coffee Can Investing.')


st.markdown("Steps one could follow::")

st.markdown("- Identify the top 2 or 3 companies in the sectors you understand. Just track where you , your family and your friends spend most of their money. Companies making the products and services you are consuming month on month will be great starting point in identifying these companies.")
st.markdown("- Invest systematically through ups and downs of the market.")
st.markdown("- Stay patient and try not to churn your portfolio too often.")

## DataFrame with the Companies and their 10 year CAGR
data = pd.DataFrame({'Companies' : ['Hindustan Unilever', 'Nestle', 'Berger Paint', 'HDFC', 'Astral Poly', 'Axis Bank', 'Havells', 'Bajaj Finance', 'ITC', 'Britannia', 'Marico', 'Dabur', 'Ashok Leyland', 'Minda Industries', 'Motherson Sumi', 'Maruti Suzuki', 'Kotak Bank', 'HDFC Bank', 'Titan'],
             'CAGR(10years)' : [24, 18, 36, 13, 51, 6, 25, 58, 7, 32, 17, 18, 5, 30, 14, 14, 21, 16, 26]})

## Sorting the dataframe by company name
data = data.sort_values(by=['Companies'])

## Select the Companies 
companies_list = st.sidebar.multiselect(
	"Select the companies for your portfolio::",
	(list(data['Companies']))
)

# Add Initial Investment Slider
initial_investment = st.sidebar.slider(
    'Initial Investment',
    min_value = 0, max_value = 1000000, value= 100000, step = 10000
)

# Add Additional Investment Slider
additional = st.sidebar.slider(
    'Additional Yearly Investment',
    min_value = 1000, max_value = 100000, value= 10000, step = 1000
)

## Adding text on the sidebar
st.sidebar.markdown("Here we have assumed that these companies are growing at the same rate year on year but CAGR for 10 years does not necessarily mean it grew at the same time every year. Hence the returns might also vary a bit in real case scenario.")

### Function to calculate the Compound Interest
## Sample Example 1000 * pow(1.12, 10) + 10000 * ((pow(1.12, 11) - 1.12 ) / 0.12)
def compoundinterest(initial_investment, rate_of_return, additional, num_years):
	return round((initial_investment * pow(rate_of_return/100 + 1, 10)) + additional * ((pow(rate_of_return/100 + 1, 10 + 1) - (rate_of_return/100 + 1)) / (rate_of_return/100)), 0)

## List to store the returns
returns = []

## Sorting the company names list.
companies_list.sort()

## Calculating the returns for every company
for company in companies_list:
	returns.append(compoundinterest(initial_investment, data[data['Companies'] == company]['CAGR(10years)'].values[0], additional, 10))


## Create a dataframe to display in the page
updated = pd.DataFrame({'Companies' : companies_list, 
			'CARG(10 Years)' : list(data[data.sort_values(by=['Companies'])['Companies'].isin(companies_list)]['CAGR(10years)']), 
			'Initial Investment' : initial_investment, 
			'Additional Yearly Investment' : additional,
			'Value After 10 Years' : returns})

### Adding Text
st.markdown("Based on the selections if we had invested in these well known Indian companies 10 years back with **initial investment of " + str(initial_investment) + "** in every company along with **yearly addition of " +  str(additional) + " for 10 years**, with **total combined investment of " + str(sum(updated['Initial Investment']) + sum(updated['Additional Yearly Investment']) * 10) + "**, it would have grown to **" + str(sum(updated['Value After 10 Years'])) + "**. The value of our investment would have grown by **" + str(round(sum(updated['Value After 10 Years']) / (sum(updated['Initial Investment']) + sum(updated['Additional Yearly Investment']) * 10),0)) + " times**")

## Displaying the table. 
st.table(updated.reset_index(drop=True))