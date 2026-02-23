import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import pandas as pd
import streamlit.components.v1 as components
from st_copy_to_clipboard import st_copy_to_clipboard

# Setting the app page layout
st.set_page_config(layout = "wide", page_title='Spiral rejection templates tool', page_icon='https://github.com/yusufaliozkan/rejection_templates/blob/main/Ilogo.PNG?raw=true')
path='https://github.com/yusufaliozkan/rejection_templates/blob/main/IMPERIAL_logo_RGB_Blue_2024.png?raw=true'
st.image(path, width=400)
st.markdown("# Rejection templates tool")

# Exporting dataset
column_names = ['rejection reason', 'rejection template']
df = pd.read_csv('templates.csv', names=column_names)
df['rejection reason'] = df['rejection reason'].astype(str)
df_new = df.sort_values(by='rejection reason')

column_names_plain = ['rejection reason', 'rejection template plain text']
df_plain = pd.read_csv('rejection_templates_plain_text.csv', names=column_names_plain)
df_plain['rejection reason'] = df_plain['rejection reason'].astype(str)
df_plain_new = df_plain.sort_values(by='rejection reason')


df_new = pd.merge(df_new, df_plain_new, on='rejection reason', how='left')

tab1, tab2 = st.tabs(["Rejection templates", "HTML editor"])

with tab1:
    st.write('Select a rejection reason from the dropdown menu and copy the template to clipboard.')

    clist = df_new['rejection reason'].unique()
    reason = st.selectbox("Select a reason:", clist)
    df_new

    toggle = st.toggle('HTML text')

    col1, col2 = st.columns([1, 3])
    with col1:
        # Get the correct template based on the reason selected
        df_reason = df_new.loc[df_new['rejection reason'] == reason, 'rejection template'].values[0]
        df_reason_plain_text = df_new.loc[df_new['rejection reason'] == reason, 'rejection template plain text'].values[0]

        # Setting up the copy button logic
        if toggle:
            col12, col22 = st.columns([2,1])
            with col12:
                st.write('Copy HTML format to clipboard:')
            with col22:
                st_copy_to_clipboard(df_reason)
                # button_label = "Copy HTML template to clipboard"
                # text_to_be_copied = df_reason  # HTML template
        else:
            col12, col22 = st.columns([2,1])
            with col12:
                st.write('Copy plain text to clipboard:')
            with col22:
                st_copy_to_clipboard(df_reason_plain_text)
                # button_label = "Copy plain text template to clipboard"
                # text_to_be_copied = df_reason_plain_text  # Plain text template

        # copy_dict = {"content": text_to_be_copied}

        # # Create the copy button once
        # copy_button = Button(label=button_label)
        # copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
        #     navigator.clipboard.writeText(content);
        # """))

        # no_event = streamlit_bokeh_events(
        #     copy_button,
        #     events="GET_TEXT",
        #     key="get_text",
        #     refresh_on_update=True,
        #     override_height=75,
        #     debounce_time=0
        # )

    with col2:
        if toggle:
            with st.expander('View template (' + reason + ')', expanded=True):
                components.html(df_reason, height=400, scrolling=True)
            with st.expander('View template in HTML format (' + reason + ')'):
                st.code(df_reason)
        else:
            with st.expander('View template in plain text (' + reason + ')', expanded=True):
                st.write(df_reason_plain_text)

    st.divider()

    col1, col2 = st.columns([1, 2])
    with col1:
        public_gsheets_url = 'https://docs.google.com/spreadsheets/d/1Nx8rt1LXVnqjb4eLyo6wuw3YkrI8Bm9qqdpRoojcDVQ/edit#gid=0'
        csv_export_url = public_gsheets_url.replace('/edit#gid=', '/export?format=csv&gid=')
        df_am = pd.read_csv(csv_export_url)

        df_am['Publisher'] = df_am['Publisher'].astype(str)
        df_am2 = df_am.sort_values(by='Publisher')

        with st.expander('Publisher AAM examples*'):
            clist = df_am2['Publisher'].unique()
            publisher = st.selectbox("Select a publisher:", clist)
            df_eg1 = df_am2.loc[df_am2['Publisher'] == publisher, 'Link'].values[0]
            df_eg2 = df_am2.loc[df_am2['Publisher'] == publisher, 'Example File'].values[0]
            df_eg3 = df_am2.loc[df_am2['Publisher'] == publisher, 'Example Image'].values[0]
            df_eg4 = df_am2.loc[df_am2['Publisher'] == publisher, 'Example File/2nd Image'].values[0]
            
            st.write(df_eg1)
            st.write(df_eg2)
            st.write(df_eg3)
            st.write(df_eg4)
            st.write('*Publisher Accepted Manuscript statements in [UKCORR knowledgebase](https://www.ukcorr.org/knowledgebase/) is used')

    with col2:
        with st.expander('List of rejection reasons', expanded=False):
            df_reasons_only = df_new['rejection reason'].reset_index(drop=True)
            st.dataframe(df_reasons_only)

    st.divider()

    st.subheader('Frequently used templates')
    col1, col2 = st.columns([1, 2])

    with col1:
        df_frequent = df_new.loc[df_new['rejection reason'].isin(
            ['Wrong version - post-April 2016', 'Free to access link', 'OAL - arXiv (pre Jan 2025)', 'OAL - arXiv (post Jan 2025)', 'Duplicate record', 'Blank template'])]
        frequently = st.radio('Choose a rejection reason to display the statement', df_frequent['rejection reason'])
        text_to_be_copied = df_new.loc[df_new['rejection reason'] == frequently, 'rejection template'].values[0]
        text_to_be_copied_plain = df_new.loc[df_new['rejection reason'] == frequently, 'rejection template plain text'].values[0]

        copy_dict = {"content": text_to_be_copied}
        copy_dict_plain = {"content": text_to_be_copied_plain}

        # Copy HTML template button
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
            debounce_time=0
        )

        # Copy plain text template button
        copy_button_plain = Button(label="Copy plain text template to clipboard")
        copy_button_plain.js_on_event("button_click", CustomJS(args=copy_dict_plain, code="""
            navigator.clipboard.writeText(content);
        """))
        no_event = streamlit_bokeh_events(
            copy_button_plain,
            events="GET_PLAIN_TEXT2",
            key="get_plain_text2",
            refresh_on_update=True,
            override_height=75,
            debounce_time=0
        )

    with col2:
        display = st.checkbox('Display the rejection statement')
        if display:
            components.html(text_to_be_copied, height=800, scrolling=True)

with tab2:
    components.iframe("https://jsonformatter.org/html-viewer", height=800)