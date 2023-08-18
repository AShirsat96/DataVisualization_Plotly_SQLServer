# -*- coding: utf-8 -*-
"""
@author: Aniket
"""
import pyodbc
import pandas as pd
import plotly.graph_objects as go

import plotly.io as pio

# This code will show the plotly graph on a browser
pio.renderers.default = 'browser'

server = 'your_server_name'
database = 'your_database_name'
username = 'your_username'
password = 'your_password'

connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)

connection_string = f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}'
connection = pyodbc.connect(connection_string)

cursor = connection.cursor()

query = "Select 'Qtr ' + Convert(Nvarchar(10),DATEPART(QUARTER,MsgDate)) + ' - ' + Convert(Nvarchar(10),Year(EEOIDet.MsgDate)) as TPeriod, Sum(IsNull(TotalHFO,0)) as TotalHFO ,Sum(IsNull(TotalMDO,0)) as TotalMDO, Sum(IsNull(TotalLSFO,0)) as TotalLSFO, Sum(IsNull(TotalECAGO,0)) as TotalECAGO  ,Sum(CO2Emit) as TotalCO2, Sum(TransportWork) as TotalTransWork, Case When Sum(TransportWork) <> 0 Then  Round((Sum(CO2Emit)*1000000)/Sum(TransportWork),2) Else 0 End as EEOIPeriod  from  dbo.EEOIDet LEFT OUTER JOIN  dbo.VoyNo ON dbo.EEOIDet.ShipID = dbo.VoyNo.ShipID AND dbo.EEOIDet.VoyNo = dbo.VoyNo.VoyNo WHERE (VoyNo.VslLastMsgType IS NOT NULL) and (TotalHFO+TotalMDO+TotalLSFO+TotalECAGO) >0  Group by Year(EEOIDet.MsgDate),DATEPART(QUARTER,MsgDate)  Order by Year(EEOIDet.MsgDate),DATEPART(QUARTER,MsgDate)"
cursor.execute(query)

# Fetch the data into a list of tuples
rows = cursor.fetchall()

# Get column names from the cursor's description
column_names = [column[0] for column in cursor.description]

# Create a DataFrame from the fetched data and column names
dfQtrEEOI = pd.DataFrame.from_records(rows, columns=column_names)
dfQtrEEOI

dfQtrEEOI.info()

# Convert a specific column to float
dfQtrEEOI['EEOIPeriod'] = pd.to_numeric(dfQtrEEOI['EEOIPeriod'], errors='coerce').astype(float)

# Create the bar chart with adjusted label positions
fig = go.Figure(data=[go.Bar(
    x=dfQtrEEOI['TPeriod'],
    y=dfQtrEEOI['EEOIPeriod'],
    text=dfQtrEEOI['EEOIPeriod'],
    textposition='outside',  # Change this to 'inside' or 'outside' as desired
)])

# the x-axis tick angle customizes the positioning of the labels
fig.update_layout(xaxis_tickangle=290)

fig.show()
