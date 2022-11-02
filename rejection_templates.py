import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import pandas as pd
import streamlit.components.v1 as components


# Setting the app page layout
st.set_page_config(layout = "wide", page_title='Imperial College London - Spiral statistics dashboard', page_icon='https://pbs.twimg.com/profile_images/1509826209563263008/cNh9JRjd_400x400.jpg')
path='https://upload.wikimedia.org/wikipedia/en/thumb/3/32/Logo_for_Imperial_College_London.svg/2560px-Logo_for_Imperial_College_London.svg.png'
st.markdown("# Rejection templates tool")

st.sidebar.image(path, width=150)
st.sidebar.markdown("# Rejection templates tool")

# Exporting dataset
column_names = ['rejection reason', 'rejection template']
df = pd.read_csv('templates.csv', names=column_names)
df['rejection reason'] = df['rejection reason'].astype(str)
df_new = df.sort_values(by='rejection reason')

st.write('Select a rejection reason from the dropdown menu and copy the HTML template to clipboard.')

col1, col2 = st.columns([1,2])
with col1:
    clist = df_new['rejection reason'].unique()
    reason = st.selectbox("Select a reason:",clist)
    df_reason = df.loc[df_new['rejection reason']==reason, 'rejection template'].values[0]
    text_to_be_copied = df_reason
    copy_dict = {"content": text_to_be_copied}


    copy_button = Button(label="Copy the HTML template to clipboard")
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

with col2:
    with st.expander('Template view (' + reason+')', expanded=False):
        components.html(df_reason, height=1500)
    with st.expander('Template in HTML format (' + reason+')'):
        st.code(df_reason)


col1, col2 = st.columns(2)

with col1:
    st.header('Frequently used templates')
    with st.expander('Free to access link'):
        st.code(df.loc[df_new['rejection reason']=='Free to access link', 'rejection template'].values[0])

with col2:
    with st.expander('List of rejection reasons'):
        st.dataframe(df_new['rejection reason'], expanded=True)



# with col1:
#     with st.expander("Frequently used copyright statements"):
#         text_to_be_copied = df.loc[df_new['rejection reason']=='Wrong version - post-April 2016', 'rejection template'].values[0]
#         copy_dict = {"content": text_to_be_copied}

#         copy_button = Button(label="Wrong version - post-April 2016")
#         copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
#             navigator.clipboard.writeText(content);
#             """))

#         no_event = streamlit_bokeh_events(
#             copy_button,
#             events="GET_TEXT2",
#             key="get_text2",
#             refresh_on_update=True,
#             override_height=75,
#             debounce_time=0)


#         text_to_be_copied = df.loc[df_new['rejection reason']=='Free to access link', 'rejection template'].values[0]
#         copy_dict = {"content": text_to_be_copied}

#         copy_button = Button(label="Free to access link")
#         copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
#             navigator.clipboard.writeText(content);
#             """))

#         no_event = streamlit_bokeh_events(
#             copy_button,
#             events="GET_TEXT3",
#             key="get_text3",
#             refresh_on_update=True,
#             override_height=75,
#             debounce_time=0)

#         text_to_be_copied = df.loc[df_new['rejection reason']=='OAL - arXiv', 'rejection template'].values[0]
#         copy_dict = {"content": text_to_be_copied}

#         copy_button = Button(label="OAL - arXiv")
#         copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
#             navigator.clipboard.writeText(content);
#             """))

#         no_event = streamlit_bokeh_events(
#             copy_button,
#             events="GET_TEXT4",
#             key="get_text4",
#             refresh_on_update=True,
#             override_height=75,
#             debounce_time=0)

#         text_to_be_copied = df.loc[df_new['rejection reason']=='Duplicate record', 'rejection template'].values[0]
#         copy_dict = {"content": text_to_be_copied}

#         copy_button = Button(label="Duplicate record")
#         copy_button.js_on_event("button_click", CustomJS(args=copy_dict, code="""
#             navigator.clipboard.writeText(content);
#             """))

#         no_event = streamlit_bokeh_events(
#             copy_button,
#             events="GET_TEXT5",
#             key="get_text5",
#             refresh_on_update=True,
#             override_height=75,
#             debounce_time=0)