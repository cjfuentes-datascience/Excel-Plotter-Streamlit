import streamlit as st
import pandas as pd
import plotly.express as px

def generate_excel_download_link(df):
    towrite=BytesIO()
    df.to_excel(towrite, encoding='utf-8', index=False, header=True) # write to BytesIO
    towrite.seek(0) # reset pointer
    b64=base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="streamlit_data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

st.set_page_config(page_title='Excel Plotter')
st.title('Excel Plotter')
st.subheader('Feed me with your excel file: :yum:')

uploaded_file=st.file_uploader('Choose a XLSX file', type='xlsx')
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    st.dataframe(df)
    groupby_column=st.selectbox(
        'What would you like to analyze?',
        df.columns.tolist()
    )

    # -- GROUP DATAFRAME
    output_columns=groupby_column
    df_grouped=df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()

    fig = px.bar(df_grouped, x=groupby_column, y=output_columns, color=groupby_column)
    st.plotly_chart(fig)
