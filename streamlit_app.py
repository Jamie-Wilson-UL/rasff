import pandas as pd
import streamlit as st

# Sample DataFrames (assuming they are already created as per previous discussions)
# pivot_df, pivot_ireland_df, sorted_grouped_df1, sorted_grouped_df2, sorted_grouped_df3

# For demonstration purposes, let's recreate the DataFrames
rasff = pd.read_csv('rasff.csv')

# Convert all relevant columns to string
rasff['origin'] = rasff['origin'].astype(str)
rasff['NCSP Category (Search output)'] = rasff['NCSP Category (Search output)'].astype(str)
rasff['Food Search Output (Description)'] = rasff['Food Search Output (Description)'].astype(str)

# Group by 'origin', 'NCSP Category (Search output)', and 'Food Search Output (Description)' and count the number of notifications
grouped_df1 = rasff.groupby(['origin', 'NCSP Category (Search output)', 'Food Search Output (Description)']).size().reset_index(name='count')
sorted_grouped_df1 = grouped_df1.sort_values(by=['origin', 'count'], ascending=[True, False])

# Group by 'NCSP Category (Search output)', 'Food Search Output (Description)', and 'origin' and count the number of notifications
grouped_df2 = rasff.groupby(['NCSP Category (Search output)', 'Food Search Output (Description)', 'origin']).size().reset_index(name='count')
sorted_grouped_df2 = grouped_df2.sort_values(by=['NCSP Category (Search output)', 'count'], ascending=[True, False])

# Group by 'Food Search Output (Description)', 'NCSP Category (Search output)', and 'origin' and count the number of notifications
grouped_df3 = rasff.groupby(['Food Search Output (Description)', 'NCSP Category (Search output)', 'origin']).size().reset_index(name='count')
sorted_grouped_df3 = grouped_df3.sort_values(by=['Food Search Output (Description)', 'count'], ascending=[True, False])

# Pivot tables
pivot_df = rasff.pivot_table(index='NCSP Category (Search output)', columns='origin', aggfunc='size', fill_value=0)

# Add a column for the total counts per substance
pivot_df['Total'] = pivot_df.sum(axis=1)

# Add a row for the total counts per country
total_row = pd.DataFrame(pivot_df.sum(axis=0)).T
total_row.index = ['Total']

# Concatenate the total row to the pivot table
pivot_df = pd.concat([pivot_df, total_row])

# Reset the index to turn the index into a column
pivot_df.reset_index(inplace=True)

# Rename the column that was the index
pivot_df.rename(columns={'index': 'NCSP Category (Search output)'}, inplace=True)

# Sort the rows by the 'Total' column
pivot_df = pivot_df.sort_values(by='Total', ascending=False)

# Ensure 'Total' is the last column
cols = [col for col in pivot_df.columns if col != 'Total'] + ['Total']
pivot_df = pivot_df[cols]

# Sort the columns by the total row
sorted_columns = pivot_df.set_index('NCSP Category (Search output)').T.sort_values(by='Total', ascending=False).T.columns
pivot_df = pivot_df[['NCSP Category (Search output)'] + sorted_columns.tolist()]

# Ensure 'Total' is the last column again
if 'Total' in pivot_df.columns:
    cols = [col for col in pivot_df.columns if col != 'Total'] + ['Total']
    pivot_df = pivot_df[cols]

# Move the Total row to the end if it's not already
total_row_data = pivot_df[pivot_df['NCSP Category (Search output)'] == 'Total']
pivot_df = pivot_df[pivot_df['NCSP Category (Search output)'] != 'Total']
pivot_df = pd.concat([pivot_df, total_row_data], ignore_index=True)

# Filter the dataframe for rows where notifying_country is 'Ireland'
ireland_rasff = rasff[rasff['notifying_country'] == 'Ireland']

# Create a pivot table
pivot_ireland_df = ireland_rasff.pivot_table(index='NCSP Category (Search output)', columns='origin', aggfunc='size', fill_value=0)

# Add a column for the total counts per substance
pivot_ireland_df['Total'] = pivot_ireland_df.sum(axis=1)

# Add a row for the total counts per country
total_row_ireland = pd.DataFrame(pivot_ireland_df.sum(axis=0)).T
total_row_ireland.index = ['Total']

# Concatenate the total row to the pivot table
pivot_ireland_df = pd.concat([pivot_ireland_df, total_row_ireland])

# Reset the index to turn the index into a column
pivot_ireland_df.reset_index(inplace=True)

# Rename the column that was the index
pivot_ireland_df.rename(columns={'index': 'NCSP Category (Search output)'}, inplace=True)

# Sort the rows by the 'Total' column
pivot_ireland_df = pivot_ireland_df.sort_values(by='Total', ascending=False)

# Ensure 'Total' is the last column
cols = [col for col in pivot_ireland_df.columns if col != 'Total'] + ['Total']
pivot_ireland_df = pivot_ireland_df[cols]

# Sort the columns by the total row
sorted_columns = pivot_ireland_df.set_index('NCSP Category (Search output)').T.sort_values(by='Total', ascending=False).T.columns
pivot_ireland_df = pivot_ireland_df[['NCSP Category (Search output)'] + sorted_columns.tolist()]

# Ensure 'Total' is the last column again
if 'Total' in pivot_ireland_df.columns:
    cols = [col for col in pivot_ireland_df.columns if col != 'Total'] + ['Total']
    pivot_ireland_df = pivot_ireland_df[cols]

# Move the Total row to the end if it's not already
total_row_data_ireland = pivot_ireland_df[pivot_ireland_df['NCSP Category (Search output)'] == 'Total']
pivot_ireland_df = pivot_ireland_df[pivot_ireland_df['NCSP Category (Search output)'] != 'Total']
pivot_ireland_df = pd.concat([pivot_ireland_df, total_row_data_ireland], ignore_index=True)


# Streamlit App
st.title('RASFF Notifications Tables')

# Display pivot_df
st.header('Pivot Table')
st.dataframe(pivot_df)

# Display pivot_ireland_df
st.header('Pivot Table Ireland')
st.dataframe(pivot_ireland_df)

# Display sorted_grouped_df1
st.header('Sorted Grouped DF1')
st.dataframe(sorted_grouped_df1)

# Display sorted_grouped_df2
st.header('Sorted Grouped DF2')
st.dataframe(sorted_grouped_df2)

# Display sorted_grouped_df3
st.header('Sorted Grouped DF3')
st.dataframe(sorted_grouped_df3)
