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

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Contact Information", "Education", "Skills", "projects", "work", "Build Resume"])

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

  e1 = education_edit.slice(0,1)
  s1 = e1.select('school').item()
  d1 = e1.select('degree').item()
  ex1 = e1.select(pl.col('expected').dt.to_string("%b %Y")).item()
  
  st.markdown(f'**{d1}**')
  st.markdown(f'*{s1}*')
  st.markdown(f'*Expected: {ex1}*')

with tab3:
  skills_edit = st.data_editor(skills, num_rows="dynamic", hide_index=True, use_container_width=True)

  topics = skills_edit.group_by("topic", maintain_order=True).len()
  ntopics = topics.shape[0]

  slist1 = skills_edit\
    .join(topics.slice(0, 1), on='topic')\
    .with_columns(
      ("**"+pl.col("skill")+"**"+ " (" + pl.col("details") + ")")\
        .alias("skill_items"))\
    .select("skill_items").to_series().to_list()

  slist2 = skills\
    .join(topics.slice(1, 1), on='topic')\
    .with_columns(
      ("**"+pl.col("skill")+"**"+ " (" + pl.col("details") + ")")\
        .alias("skill_items"))\
    .select("skill_items").to_series().to_list()

  slist3 = skills\
    .join(topics.slice(2, 1), on='topic')\
    .with_columns(
      ("**"+pl.col("skill")+"**"+ " (" + pl.col("details") + ")")\
        .alias("skill_items"))\
    .select("skill_items").to_series().to_list()

  slist4 = skills\
    .join(topics.slice(2, 1), on='topic')\
    .with_columns(
      ("**"+pl.col("skill")+"**"+ " (" + pl.col("details") + ")")\
        .alias("skill_items"))\
    .select("skill_items").to_series().to_list()

  s1 = "- " + ", ".join(slist1)
  s2 = "- " + ", ".join(slist2)
  s3 = "- " + ", ".join(slist3)
  s4 = "- " + ", ".join(slist4)

  if ntopics == 1:
    out = f"""
  {s1}
  """
  elif ntopics == 2:
    out = f"""
  {s1}
  {s2}
  """
  elif ntopics == 3:
    out = f"""
  {s1}
  {s2}
  {s3}
  """
  elif ntopics == 4:
    out = f"""
  {s1}
  {s2}
  {s3}
  {s4}
  """
  else:
    out = "Too many topics. At most 4."

  st.markdown(out)


with tab4:
  prn_work = st.number_input("Select Project Row", 1, 5)
  projects_edit = st.data_editor(projects, num_rows="dynamic", hide_index=True, use_container_width=True)

  pr_n, pr_p, pr_g, pr_l, pr_s, pr_e = projects_dat(projects.slice(prn_work - 1, 1))

  st.markdown(f'''***{pr_n}***''')
  st.markdown(f'*{pr_p}*')
  st.markdown(f'[{pr_s} -- {pr_e}]{{.cvdate}}')
  st.markdown(f'- {pr_l}: [Github Repository]({pr_g})')




with tab5:
  rn_work = st.number_input("Select Job Row", 1, 5)
  work_edit = st.data_editor(work, num_rows="dynamic", hide_index=True, use_container_width=True)
  
  work_select = work_edit.slice(rn_work - 1,1)
  st.markdown(work_chunk(work_select, True))


with tab6:
    stab1, stab2, stab3 = st.tabs(["Build", "PDF", "HTML"])
    
    with stab1:
      lists = [a for a in os.listdir() if os.path.isdir(a) if 'tables' in a]
      pick_template = [a for a in os.listdir() if '.qmd' in a]
      wfolder = st.selectbox("Pick Data Folder", lists) 
      if st.button("Store Data"):
        if "personal_tables" not in lists:
          os.mkdir("personal_tables")
        projects_edit.write_parquet(wfolder + "/projects.parquet")
        skills_edit.write_parquet(wfolder + "/skills.parquet")
        work_edit.write_parquet(wfolder + "/work.parquet")
        education_edit.write_parquet(wfolder + "/education.parquet")
        contact_edit.write_parquet(wfolder + "/contact.parquet")

      data_folder = st.selectbox("Pick Build Folder", lists)
      qmd_file = st.selectbox("Pick Quarto Template", pick_template)

      if st.button("Build Resume", use_container_width = True, type = "primary"):
        quarto.render(qmd_file, execute_params={'dfolder':data_folder})

    with stab2:
      pdf_viewer("docs/index.pdf", width = 800, height = 1000, pages_vertical_spacing = 10)

    with stab3:
      HtmlFile = open("docs/index.html", 'r', encoding='utf-8')
      source_code = HtmlFile.read() 
      tile = st.container()
      tile.html(source_code)

