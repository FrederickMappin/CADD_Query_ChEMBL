import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Title of the Streamlit app
st.title('Bioactivity Data Dashboard')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Calculate total and unique molecule_chembl_id counts
    total_molecules = data['molecule_chembl_id'].count()
    unique_molecules = data['molecule_chembl_id'].nunique()

    # Display total and unique molecule_chembl_id counts
    st.subheader('Total vs Unique Molecule ChEMBL IDs')
    st.bar_chart(pd.DataFrame({
        'Count': [total_molecules, unique_molecules]
    }, index=['Total Molecules', 'Unique Molecules']))

    # Calculate the counts of each bioactivity type
    bioactivity_counts = data['bioactivity'].value_counts()

    # Display bioactivity counts
    st.subheader('Counts of Bioactivity Types')
    st.bar_chart(bioactivity_counts)

    # Convert 'standard_value' to numeric, coercing errors to NaN (if any non-numeric values are present)
    data['standard_value'] = pd.to_numeric(data['standard_value'], errors='coerce')

    # Cap the standard_value at 10000 for the histogram
    capped_standard_values = np.where(data['standard_value'] > 10000, 10000, data['standard_value'])

    # Display histogram for the capped standard_value column
    st.subheader('Distribution of Standard Values (Capped at 10000)')
    fig, ax = plt.subplots()
    ax.hist(capped_standard_values, bins=30, color='purple', edgecolor='black')
    ax.set_title('Distribution of Standard Values (Capped at 10000)')
    ax.set_xlabel('Standard Value')
    ax.set_ylabel('Count')
    st.pyplot(fig)

    # Calculate the number of occurrences of each molecule_chembl_id
    molecule_counts = data['molecule_chembl_id'].value_counts()

    # Calculate the average standard_value for each unique molecule_chembl_id
    average_standard_values = data.groupby('molecule_chembl_id')['standard_value'].mean()

    # Create a DataFrame for plotting
    plot_data = pd.DataFrame({
        'molecule_chembl_id': molecule_counts.index,
        'count': molecule_counts.values,
        'average_standard_value': average_standard_values.values
    })

    # Display scatter plot
    st.subheader('Number of Occurrences vs Average Standard Value of Molecule ChEMBL IDs')
    fig, ax = plt.subplots()
    ax.scatter(plot_data['average_standard_value'], plot_data['count'], alpha=0.6)
    ax.set_title('Number of Occurrences vs Average Standard Value of Molecule ChEMBL IDs')
    ax.set_xlabel('Average Standard Value')
    ax.set_ylabel('Number of Occurrences')
    ax.grid(True)
    st.pyplot(fig)

    # Round the average_standard_value to a whole number
    average_standard_values = average_standard_values.round()

    # Create a DataFrame for plotting
    plot_data = pd.DataFrame({
        'molecule_chembl_id': molecule_counts.index,
        'count': molecule_counts.values,
        'average_standard_value': average_standard_values.values
    })

    # Select the top 20 most occurring molecule_chembl_id
    top_20_plot_data = plot_data.nlargest(20, 'count')

    # Display graphical table
    st.subheader('Top 20 Molecule ChEMBL IDs based on occurrences')
    st.table(top_20_plot_data)

# Run the Streamlit app with `streamlit run app.py`