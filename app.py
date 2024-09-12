import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from employee_db_helper import insert_employee_data


load_dotenv('conexion.env')  


st.title("Insurance Company Employee Data Upload")

personal_data = None
performance_data = None
employee_data = None  


def load_excel(file):
    """Carga un archivo de Excel y lo convierte en un DataFrame"""
    try:
        return pd.read_excel(file)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


col1, col2, _ = st.columns([3, 1, 1])

with col1:
    
    tab1, tab2 = st.tabs(["Personal Data", "Employee Performance"])

with col2:
    
    combine_button = st.button("Combine DataFrames")


with tab1:
    st.markdown("### Upload Personal Data Excel File")
    personal_file = st.file_uploader("Choose the personal data Excel file", type=['xlsx'], key="personal")

    if personal_file:
        personal_data = load_excel(personal_file)
        if personal_data is not None:
            st.markdown("### Personal Data Table")
            st.dataframe(personal_data)
        else:
            st.error("There was an error loading the personal data file.")

#
with tab2:
    st.markdown("### Upload Employee Performance Excel File")
    performance_file = st.file_uploader("Choose the employee performance Excel file", type=['xlsx'], key="performance")

    if performance_file:
        performance_data = load_excel(performance_file)
        if performance_data is not None:
            st.markdown("### Employee Performance Data Table")
            st.dataframe(performance_data)
        else:
            st.error("There was an error loading the employee performance file.")


if combine_button:
    if personal_data is not None and performance_data is not None:
        
        st.write("Personal Data Columns:", personal_data.columns)
        st.write("Employee Performance Columns:", performance_data.columns)

        
        personal_data = personal_data.rename(columns={'Id': 'ID'})

        
        performance_data = performance_data.rename(columns={'Id': 'ID'})

        
        employee_data = pd.merge(personal_data, performance_data, on='ID', how='inner')

        
        st.write("Columns in Combined DataFrame:", employee_data.columns)

        
        selected_columns = ['ID', 'Age', 'Income', 'Expenses', 'Weekly_Hours']

        
        missing_columns = [col for col in selected_columns if col not in employee_data.columns]
        if missing_columns:
            st.error(f"Missing columns in the DataFrame: {', '.join(missing_columns)}")
        else:
            employee_data = employee_data[selected_columns]

            
            st.markdown("### Employee Data Table")
            st.dataframe(employee_data)

            
            if st.button("Save Data to Database"):
                if not employee_data.empty:
                    
                    st.write("Data to be saved:", employee_data)

                    
                    insert_employee_data(employee_data)
                    st.success("Data has been successfully saved to the database.")
                else:
                    st.error("No data to save. Please check the combined DataFrame.")
    else:
        st.error("Please upload both Personal Data and Employee Performance files first.")
