# Import streamlit to make frontend components
import streamlit as st

# Import functions from other files, where the View is created
from architecture import archfunc
from home import homefunc
from analysis import requirements, results

# Set page configuration, page title is the titlebar content, icon also appears on title bar
st.set_page_config(page_title="Satellite System Dashboard", page_icon="🛰️", layout="wide")

# main entrypoint of the application, gets called when the app runs
def main():

    # For the heading on the page
    st.header("🛰️ Dashboard", divider="violet")

    # create the list of tabs in a list
    TABS = ["Home", "Requirements", "Architecture", "Analysis Summary"]
    # pass the list to make a tab component
    tabs = st.tabs(TABS)

    # call each tab and call the function that containes the Page view under the tab section
    with tabs[0]:
        homefunc()
    with tabs[1]:
        requirements()
    with tabs[2]:
        archfunc()
    with tabs[3]:
        results()


if __name__ == "__main__":
    main()