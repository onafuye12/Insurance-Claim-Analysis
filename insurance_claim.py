import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import base64
sns.set()

import mysql.connector as connection

db = connection.connect(host="sql8.freesqldatabase.com", database="sql8683366", user="sql8683366", passwd="xPf6Q29U8w", use_pure=True)



df = pd.read_sql_query("SELECT * FROM `TABLE 1`", db)


 #list of int columns to be coverted to integer
int_column = ['ClassCode', 'Sno','ServiceCode','QuantityofService','HNetAmt','CNetAmt','RejectAmt','FinalAmt','Duplicate_Flag','Double_claim_Flag','Consumables_Flag','Widal_Flag','New_member_Flag','Excess_Flag','Upcoding_Flag','Cluster']
    
for column in int_column:
    df[column] = df[column].astype(int)
    

date_columns = ['AdmissionDate','DischargeDate','ReviewDate','ToDate','FromDate','ClaimReceivedDate','ClaimIncurredDate']
  # List of date columns to be converted to datetime
    
for column in date_columns:
    df[column] = pd.to_datetime(df[column], errors='coerce')
    

#Data cleaning
    
for column in df.columns:
    most_frequent_value = df[column].mode()[0]
    df[column] = df[column].replace('?', most_frequent_value)

for i in df.columns:
    df.loc[df[i] == '?', i] = 'unknown'
    
# Options for the radio selection widget
options = ['About','Filter Pane','Visualisation']

# Radio selection widget
selected_option = st.sidebar.radio("Select an option:", options)

if selected_option == 'About':
    st.title('Health Anomaly Detection')
    
    st.image("AXA-Logo.svg", width=True)
    
   
    st.markdown('''Welcome to our insurance data analysis project!


In this project, we delve into a comprehensive dataset containing valuable information about insurance customers and their claims. By exploring various aspects such as customer demographics, policy details, and claim information, we aim to uncover insights that can help in understanding patterns, trends, and factors influencing insurance claims.

Through interactive visualizations and data exploration tools provided by Streamlit, we invite you to navigate through the dataset, analyze the relationships between different variables, and gain a deeper understanding of the insurance landscape.

Join us on this data-driven journey as we uncover meaningful insights from the world of insurance.''')
    
    st.markdown('''The dataset provides detailed information about insurance customers and claims. Here is a detailed summary of the data:

## About the Data

- **ClaimNo:** Unique identifier for each claim.
- **ClaimBatchNo:** Batch number associated with the claim.
- **ClaimReceivedDate:** Date when the claim was received.
- **ClaimIncurredDate:** Date when the claim was incurred.
- **ClaimType:** Type of claim (e.g., medical, insurance).
- **MemberNo:** Member identification number.
- **Name:** Name of the individual associated with the claim.
- **PolicyNo:** Policy number related to the claim.
- **FromDate:** Start date of the service covered by the claim.
- **ToDate:** End date of the service covered by the claim.
- **ClassCode:** Code representing the class of service.
- **ClassName:** Name of the class of service.
- **BasicDiagnosis:** Primary diagnosis for the claim.
- **ProviderNo:** Provider identification number.
- **ProviderName:** Name of the service provider.
- **OpdIpd:** Type of service (Outpatient or Inpatient).
- **ClaimStatus:** Status of the claim (e.g., pending, processed).
- **cdate:** Creation date of the claim record.
- **USERID:** User ID associated with the claim.
- **CreditNoteNo:** Number associated with the credit note related to the claim.
- **Sno:** Serial number or unique identifier for each service.
- **ServiceCode:** Code representing the service provided.
- **ServiceType:** Type of service provided.
- **ServiceDescription:** Description of the service provided.
- **QuantityofService:** Amount or quantity of service provided.
- **HNetAmt:** Net amount after deductions for the service.
- **CNetAmt:** Net amount after deductions for the claim.
- **RejectAmt:** Amount rejected in the claim.
- **FinalAmt:** Final approved amount for the claim.
- **DiagnosisCode:** Code representing the diagnosis.
- **DESCRIPTION:** Description associated with a diagnosis.
- **DiagnosisType:** Type of diagnosis (e.g., primary, secondary).
- **AdmissionDate:** Date of admission for inpatient services.
- **DischargeDate:** Date of discharge for inpatient services.
- **ReviewDate:** Date when the claim was reviewed.
- **ReviewerName:** Name of the person who reviewed the claim.
- **FName:** First name associated with the claim.''')
# Display the selected option

elif selected_option == 'Filter Pane':
    
    st.title('Filter')
    st.write('')
    st.header('Data Shape: ')
    
    st.header(df.shape)
    
    

    DESCRIPTION = st.selectbox('Select DESCRIPTION', ['Other viral Infections incl malaria, URTIof unspecified site',
       'Plasmodium falciparum malaria', 'Erysipelothrix sepsis',
       'Acute tonsillitis','ALL'])
    MemberNo = st.number_input('member number',step=1)
    # Date filter widget
    
    class SessionState:
        def __init__(self):
            self.start_date = None
            self.end_date = None

    state = SessionState()

    state.start_date = st.date_input("ClaimReceivedDate Start Date", state.start_date)
    state.end_date = st.date_input("ClaimReceivedDate End Date", state.end_date)

   

   
    
    Name = st.text_input("Customer's name")
   
    
    
    if DESCRIPTION:
        if DESCRIPTION == 'ALL':
            filtered_df = df
        else:
            filtered_df = df[df['DESCRIPTION'] == DESCRIPTION]

        if MemberNo:
            filtered_df = filtered_df[filtered_df['MemberNo'] == MemberNo]

        if Name:
            filtered_df = filtered_df[filtered_df['Name'] == Name]

        
            
        if state.start_date and state.end_date:
            start_date = pd.to_datetime(state.start_date)
            end_date = pd.to_datetime(state.end_date)
            filtered_df = filtered_df[(filtered_df['ClaimReceivedDate'] >= start_date) & (filtered_df['ClaimReceivedDate'] <= end_date)]
            
    st.write(filtered_df)
    
    csv1 = filtered_df.to_csv(index=False)
    st.download_button('Download filter', csv1,file_name='insurance_claim_filter.csv')



    

    
    
else:

    st.title("DATA VISUALISATION:")
    
    
    

    
    Charts = st.selectbox('Select Chart', ['Flags', 'Cluster Count'])
    
    #Bar Chart
    
    if Charts == 'Flags':
        def flags(col,df):
            grouped_df = df.groupby(col)[col].count()
            fig, ax = plt.subplots(figsize=(10, 6))

            grouped_df.plot(kind='barh', ax=ax, color='#051094', width=0.7)

            ax.set_title(f'Count of {col}', fontsize=20, c='black')
            ax.set_xlabel('Count', fontsize=20, c='black')
            ax.set_ylabel(f'{col}', fontsize=20, c='black')
            #plt.grid()

            st.pyplot(fig)
        Flag = st.selectbox('Select Flag Type', ['Duplicate Flag', 'Double claim Flag','Consumables Flag','Widal Flag','New member Flag','Excess Flag','Upcoding Flag'])
        # condition statement to select different flags
        if Flag == 'Duplicate Flag':
            flags('Duplicate_Flag',df)
            
        elif Flag == 'Double claim Flag':
            flags('Double_claim_Flag',df)
            
        elif Flag == 'Consumables Flag':
            flags('Consumables_Flag',df)
            
        elif Flag == 'Widal Flag':
            flags('Widal_Flag',df)
            
        elif Flag == 'New member Flag':
            flags('New_member_Flag',df)
            
        elif Flag == 'Excess Flag':
            flags('Excess_Flag',df)
            
        else:
            flags('Upcoding_Flag',df)

    elif Charts == 'Cluster Count':
        # Selectbox for choosing the number of provider names to display
        num_providers = st.selectbox('Select Number of Providers to Display', [1, 2, 5, 10, 15])

        # Grouping the data by 'ProviderName' and counting the occurrences of 'Cluster'
        grouped_df = df.groupby('ProviderName')['Cluster'].count().nlargest(num_providers)

        fig, ax = plt.subplots(figsize=(10, 6))

        grouped_df.plot(kind='barh', ax=ax, color='#051094', width=0.7)

        ax.set_title(f'Top {num_providers} Providers by Cluster Count', fontsize=20, c='black')
        ax.set_xlabel('Cluster Count', fontsize=20, c='black')
        ax.set_ylabel('Provider', fontsize=20, c='black')

        st.pyplot(fig)

