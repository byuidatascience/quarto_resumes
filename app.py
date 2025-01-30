import os
import shutil
import pandas as pd
import polars as pl
import polars.selectors as cs
from great_tables import GT, md, html, style, loc
import pyarrow as pa
import pyarrow.parquet as pq
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from streamlit import session_state as ss
from streamlit.connections import ExperimentalBaseConnection
from streamlit_pdf_viewer import pdf_viewer
import quarto
import duckdb
# https://pypi.org/project/streamlit-pdf-viewer/
from resume_builder import *

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="BYU-I DS Resume Builder",
    layout="wide"
)
 
# Add Title
st.title("Build your resume")

projects = pl.read_parquet("default_tables/projects.parquet")
skills = pl.read_parquet("default_tables/skills.parquet")
work = pl.read_parquet("default_tables/work.parquet")
education = pl.read_parquet("default_tables/education.parquet")
contact = pl.read_parquet("default_tables/contact.parquet")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Contact Information", "Education", "Skills", "projects", "work"])

with tab1:
  contact_edit = st.data_editor(contact, num_rows="dynamic", hide_index=True, use_container_width=True)

  name_id = contact_edit.select("name").item()
  email_id = contact_edit.select("email").item()
  github_id = contact_edit.select("github").item()
  linkedin_id = contact_edit.select("linkedin").item()
  telephone_id = contact_edit.select("phone").item()


st.markdown(f'[{email_id}](mailto:{email_id})')
st.markdown(f'[Github](https://github.com/{github_id})')
st.markdown(f'[LinkedIn.com](https://www.linkedin.com/in/{linkedin_id}/)')
st.markdown(f'[{telephone_id}](tel:{telephone_id})')


with tab2:
  education_edit = st.data_editor(education, num_rows="dynamic", hide_index=True, use_container_width=True)

with tab3:
  skills_edit = st.data_editor(skills, num_rows="dynamic", hide_index=True, use_container_width=True)

with tab4:
  projects_edit = st.data_editor(projects, num_rows="dynamic", hide_index=True, use_container_width=True)

with tab5:
  work_edit = st.data_editor(work, num_rows="dynamic", hide_index=True, use_container_width=True)


# pdf_viewer("pricing_request_typst.pdf", width = 800, height = 1000, pages_vertical_spacing = 10)