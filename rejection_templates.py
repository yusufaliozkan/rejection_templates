import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import pandas as pd
import streamlit.components.v1 as components


# Setting the app page layout
st.set_page_config(layout = "wide", page_title='Spiral rejection templates tool', page_icon='https://pbs.twimg.com/profile_images/1509826209563263008/cNh9JRjd_400x400.jpg')
path='https://upload.wikimedia.org/wikipedia/en/thumb/3/32/Logo_for_Imperial_College_London.svg/2560px-Logo_for_Imperial_College_London.svg.png'
# st.image('header_full.png')
st.image(path, width=200)
st.markdown("# Rejection templates tool")

# st.sidebar.markdown("# Rejection templates tool") 

# Exporting dataset
column_names = ['rejection reason', 'rejection template']
df = pd.read_csv('templates.csv', names=column_names)
df['rejection reason'] = df['rejection reason'].astype(str)
df_new = df.sort_values(by='rejection reason')

tab1, tab2 = st.tabs(["Rejection templates", "HTML editor"])

with tab1:
    st.write('Select a rejection reason from the dropdown menu and copy the HTML template to clipboard.')

    col1, col2 = st.columns([1,2])
    with col1:
        clist = df_new['rejection reason'].unique()
        reason = st.selectbox("Select a reason:",clist)
        df_reason = df.loc[df_new['rejection reason']==reason, 'rejection template'].values[0]
        text_to_be_copied = df_reason
        copy_dict = {"content": text_to_be_copied}


        copy_button = Button(label="Copy HTML template to clipboard")
        copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
            navigator.clipboard.writeText(content);
            """))

        no_event = streamlit_bokeh_events(
            copy_button,
            events="GET_TEXT",
            key="get_text",
            refresh_on_update=True,
            override_height=75,
            debounce_time=0)

        public_gsheets_url = 'https://docs.google.com/spreadsheets/d/1Nx8rt1LXVnqjb4eLyo6wuw3YkrI8Bm9qqdpRoojcDVQ/edit#gid=0'
        csv_export_url = public_gsheets_url.replace('/edit#gid=', '/export?format=csv&gid=')
        df_am = pd.read_csv(csv_export_url)

        df_am['Publisher'] = df_am['Publisher'].astype(str)
        df_am2 = df_am.sort_values(by='Publisher')

        with st.expander('Publisher AAM examples*'):
            clist = df_am2['Publisher'].unique()
            publisher = st.selectbox("Select a publisher:",clist)
            df_eg1 = df_am2.loc[df_am2['Publisher']==publisher, 'Link'].values[0]
            df_eg2 = df_am2.loc[df_am2['Publisher']==publisher, 'Example File'].values[0]
            df_eg3 = df_am2.loc[df_am2['Publisher']==publisher, 'Example Image'].values[0]
            df_eg4 = df_am2.loc[df_am2['Publisher']==publisher, 'Example File/2nd Image'].values[0]
            
            st.write(df_eg1)
            st.write(df_eg2)
            st.write(df_eg3)
            st.write(df_eg4)
            st.write('*Publisher Accepted Manuscript statements in [UKCORR knowledgebase](https://www.ukcorr.org/knowledgebase/) is used')
    with col2:
        with st.expander('View template (' + reason+')', expanded=False):
            components.html(df_reason, height=800, scrolling=True)
        with st.expander('View template in HTML format (' + reason+')'):
            st.code(df_reason)

    st.subheader('Frequently used templates')
    col1, col2 = st.columns([1,2])

    with col1:
        df_frequent = df.loc[df_new['rejection reason'].isin(['Wrong version - post-April 2016', 'Free to access link', 'OAL - arXiv', 'Duplicate record', 'Blank template'])]
        frequently = st.radio('Choose a rejection reason to display the statement', df_frequent['rejection reason'])
        text_to_be_copied = df.loc[df_new['rejection reason']==frequently, 'rejection template'].values[0]
        copy_dict = {"content": text_to_be_copied}

        copy_button = Button(label="Copy HTML template to clipboard")
        copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
            navigator.clipboard.writeText(content);
            """))

        no_event = streamlit_bokeh_events(
            copy_button,
            events="GET_TEXT2",
            key="get_text2",
            refresh_on_update=True,
            override_height=75,
            debounce_time=0)

    with col2:
        display = st.checkbox('Display the rejection statement')
        if display:
            components.html(text_to_be_copied, height=800, scrolling=True)
        st.subheader('List of rejection reasons')
        df_reasons_only = df_new['rejection reason'].reset_index(drop = True)
        st.dataframe(df_reasons_only)
        # with st.expander('View template (' + frequently+')', expanded=False):
        #     components.html(text_to_be_copied, height=800, scrolling=True)
        

    # with col2:
    #     st.subheader('List of rejection reasons')
    #     df_reasons_only = df_new['rejection reason'].reset_index(drop = True)
    #     st.dataframe(df_reasons_only)

with tab2:
    components.iframe("https://jsonformatter.org/html-viewer", height=800)