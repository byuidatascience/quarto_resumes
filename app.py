import os
import shutil
import zipfile
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

st.text("This simple app let's you store your resume information as tables. You can then build your resume as an html page and a pdf page.")

folder = st.radio("Select your data", ['Use default', 'Use personal', 'Upload my own'])

if folder == 'Use default':
  pfolder = 'tables_default'
elif folder == 'Use personal':
  pfolder = 'tables_personal'
else:
  pfolder = 'tables_ud'

if folder == 'Upload my own':
  uploaded_file = st.file_uploader("Choose your Zip file", type=['zip', 'ZIP'])
  if uploaded_file is not None:
    with zipfile.ZipFile(uploaded_file, 'r') as z:
      z.extractall('tables_ud')
  
# %%
projects = pl.read_csv(f"{pfolder}/projects.csv",
  schema=pl.Schema([
    ('name', pl.String()),
    ('purpose', pl.String()),
    ('github', pl.String()),
    ('languages', pl.String()),
    ('start', pl.Date()),
    ('end', pl.Date())]))

skills = pl.read_csv(f"{pfolder}/skills.csv",
  schema=pl.Schema([
    ('topic', pl.String()),
    ('skill', pl.String()),
    ('details', pl.String()),
    ('start', pl.Date()),
    ('projects', pl.String()),
    ('company', pl.String())]))

work = pl.read_csv(f"{pfolder}/work.csv",
  schema=pl.Schema([
    ('position', pl.String()),
    ('company', pl.String()),
    ('location', pl.String()),
    ('start', pl.Date()),
    ('end', pl.Date()),
    ('bullets', pl.String())]))

education = pl.read_csv(f"{pfolder}/education.csv",
  schema=pl.Schema([
    ('school', pl.String()),
    ('location', pl.String()),
    ('degree', pl.String()),
    ('start', pl.Date()),
    ('end', pl.Date())]))

contact = pl.read_csv(f"{pfolder}/contact.csv",
  schema=pl.Schema([
    ('name', pl.String()),
    ('email', pl.String()),
    ('github', pl.String()),
    ('linkedin', pl.String()),
    ('phone', pl.String())]))

education = make_ymd_columns(education)
work = make_ymd_columns(work)
projects = make_ymd_columns(projects)
skills = make_ymd_columns(skills)

set_columns = (3, 2)

tab1, tab2 = st.tabs(["Enter/Update Information", "Build Resume Website and PDF"])
with tab1:

  left, right = st.columns(set_columns)
  left.markdown("## Contact Information")
  left.text('Enter your name and header information for your resume. ')
  contact_edit = left.data_editor(contact,
    num_rows="dynamic",
    hide_index=True,
    use_container_width=True)

  name_id = contact_edit.select("name").item()
  email_id = contact_edit.select("email").item()
  github_id = contact_edit.select("github").item()
  linkedin_id = contact_edit.select("linkedin").item()
  telephone_id = contact_edit.select("phone").item()

  right.markdown(f'##  {name_id}')  
  col1, col2, col3 = right.columns(3)
  col1.markdown(f'[{telephone_id}](tel:{telephone_id}) | [{email_id}](mailto:{email_id})')

  col2.markdown(f'_[Github](https://github.com/{github_id})_ | _[LinkedIn.com](https://www.linkedin.com/in/{linkedin_id}/)_')

  left, right = st.columns(set_columns)
  left.markdown("## Education Information")
  left.text("Enter your education information")
  education_edit1 = left.data_editor(education,
    num_rows="dynamic",
    column_order=('school', 'location', 'degree'),
    hide_index=True,
    use_container_width=True)
  education_edit2 = left.data_editor(education_edit1,
    num_rows="dynamic",
    column_order=('school', 'start_year', 'start_month', 'end_year', 'end_month'),
    hide_index=True,
    use_container_width=True)
  
  education_edit = education_edit2.with_columns(
    pl.date(pl.col('end_year'), pl.col('end_month'), pl.lit(15)).alias('end'),
    pl.date(pl.col('start_year'), pl.col('start_month'), pl.lit(15)).alias('start')
  )

  e1 = education_edit.slice(0,1)
  s1 = e1.select('school').item()
  d1 = e1.select('degree').item()
  ex1 = e1.select(pl.col('end').dt.to_string("%b %Y")).item()

  right.markdown("----")

  right.markdown('### Education')
  right.markdown(education_stuff(education_edit, 0))
  right.markdown(education_stuff(education_edit, 1))

  left, right = st.columns(set_columns)
  left.markdown("## Skills")
  left.text("Enter your skills")

  skills_edit = left.data_editor(skills,
    num_rows="dynamic",
    column_order=('topic', 'skill', 'details', 'start_year', 'start_month', 'start_day'),
    hide_index=True,
    use_container_width=True)

  skills_edit = skills_edit.with_columns(
    pl.date(pl.col('start_year'), pl.col('start_month'), pl.col('start_day')).alias('start')
  )

  topics = skills_edit.group_by("topic", maintain_order=True).len()
  ntopics = topics.shape[0]

  if ntopics >= 1:
    slist1 = skills_edit\
      .join(topics.slice(0, 1), on='topic')\
      .with_columns(
        ("**"+pl.col("skill")+"**"+ " (" + pl.col("details") + ")")\
          .alias("skill_items"))\
      .select("skill_items").to_series().to_list()
    s1 = "- " + ", ".join(slist1)

  if ntopics >= 2:
    slist2 = skills_edit\
      .join(topics.slice(1, 1), on='topic')\
      .with_columns(
        ("**"+pl.col("skill")+"**"+ " (" + pl.col("details") + ")")\
          .alias("skill_items"))\
      .select("skill_items").to_series().to_list()
    s2 = "- " + ", ".join(slist2)

  if ntopics >= 3:
    slist3 = skills_edit\
      .join(topics.slice(2, 1), on='topic')\
      .with_columns(
        ("**"+pl.col("skill")+"**"+ " (" + pl.col("details") + ")")\
          .alias("skill_items"))\
      .select("skill_items").to_series().to_list()
    
    s3 = "- " + ", ".join(slist3)
  
  if ntopics >= 4:
    st.text(slist3)
    slist4 = skills_edit\
      .join(topics.slice(3, 1), on='topic')\
      .with_columns(
        ("**"+pl.col("skill")+"**"+ " (" + pl.col("details") + ")")\
          .alias("skill_items"))\
      .select("skill_items").to_series().to_list()
  
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

  right.markdown("----")
  right.markdown(out)

  left, right = st.columns(set_columns)

  left.markdown("## Projects")
  left.text("List personal projects that were not done for a client.")

  prn_work = left.number_input("Select Project Row", 1, 5)

  projects_edit1 = left.data_editor(projects,
    num_rows="dynamic",
    column_order=('name', 'purpose', 'github', 'languages'),
    hide_index=True,
    use_container_width=True)
  projects_edit2 = left.data_editor(projects_edit1,
    num_rows="dynamic",
    column_order=('name', 'start_year', 'start_month', 'end_year', 'end_month'),
    hide_index=True,
    use_container_width=True)
  
  projects_edit = projects_edit2.with_columns(
    pl.date(pl.col('end_year'), pl.col('end_month'), pl.lit(15)).alias('end'),
    pl.date(pl.col('start_year'), pl.col('start_month'), pl.lit(15)).alias('start')
  )

  pr_n, pr_p, pr_g, pr_l, pr_s, pr_e = projects_dat(projects_edit.slice(prn_work - 1, 1))

  right.markdown("-----")
  right.markdown(f'''***{pr_n}***''')
  right.markdown(f'*{pr_p}*')
  right.markdown(f'[{pr_s} -- {pr_e}]{{.cvdate}}')
  right.markdown(f'- {pr_l}: [Github Repository]({pr_g})')

  left, right = st.columns(set_columns)

  left.markdown("## Work")
  left.text("List work done for a client (paid or unpaid)")

  rn_work = left.number_input("Select Job Row", 1, 5)
  work_edit1 = left.data_editor(work,
    num_rows="dynamic",
    column_order=('company', 'position', 'location', 'bullets'),
    hide_index=True,
    use_container_width=True)
  work_edit2 = left.data_editor(work_edit1,
    num_rows="dynamic",
    column_order=('company', 'start_year', 'start_month', 'end_year', 'end_month'),
    hide_index=True,
    use_container_width=True)
  
  work_edit = work_edit2.with_columns(
    pl.date(pl.col('end_year'), pl.col('end_month'), pl.lit(15)).alias('end'),
    pl.date(pl.col('start_year'), pl.col('start_month'), pl.lit(15)).alias('start')
  )

  work_select = work_edit.slice(rn_work - 1,1)
  right.markdown("----")
  right.markdown(work_chunk(work_select, True))


with tab2:
    
    st.markdown("__Download Tables:__ Click `Save Tables` to save your most recent edits. Then you can click `Download ZIP` to get your csv tables in a `.zip` file.")

    c1, c2 = st.columns(2)
  
    lists = [a for a in os.listdir() if os.path.isdir(a) if 'tables' in a]
    pick_template = [a for a in os.listdir('qmd_templates') if '.qmd' in a]
    if c1.button("Save Data in `personal_tables`", use_container_width=True, type="primary"):
      if "tables_personal" not in lists:
        os.mkdir("tables_personal")
      wfolder = 'tables_personal'
      projects_edit\
        .select(pl.all().exclude(
          ["end_day", "end_month", "end_year",
           "start_day", "start_month", "start_year"]))\
        .write_csv(wfolder + "/projects.csv")
      skills_edit\
        .select(pl.all().exclude(
          ["end_day", "end_month", "end_year",
           "start_day", "start_month", "start_year"]))\
        .write_csv(wfolder + "/skills.csv")
      work_edit\
        .select(pl.all().exclude(
          ["end_day", "end_month", "end_year",
           "start_day", "start_month", "start_year"]))\
        .write_csv(wfolder + "/work.csv")
      education_edit\
        .select(pl.all().exclude(
          ["end_day", "end_month", "end_year",
           "start_day", "start_month", "start_year"]))\
        .write_csv(wfolder + "/education.csv")
      contact_edit\
        .select(pl.all().exclude(
          ["end_day", "end_month", "end_year",
           "start_day", "start_month", "start_year"]))\
        .write_csv(wfolder + "/contact.csv")
      shutil.make_archive('resume_tables', 'zip', wfolder)

      with open("resume_tables.zip", "rb") as fp:
        btn = c2.download_button(
          label="Download ZIP",
          data=fp,
          file_name="resume_tables.zip",
          mime="application/zip",
          use_container_width=True,
          type="primary"
          )

data_folder = c1.selectbox("Pick Data Folder to use for Resume Build", lists)
qmd_file = c1.selectbox("Pick Quarto Template", pick_template)
css_file = qmd_file.replace('qmd', 'css')
if c1.button("Build Resume", use_container_width = True, type = "primary"):
  shutil.copyfile(f'qmd_templates/{qmd_file}', 'index.qmd')
  shutil.copyfile(f'qmd_templates/{css_file}', css_file)
  c1.text("Template copied. Quarto rendering")
  quarto.render('index.qmd', execute_params={'dfolder':data_folder})
  c1.text("Rendering complete.")
  os.remove('index.qmd')
  os.remove(css_file)

with c2:
  pdf_viewer("docs/index.pdf", width = 800, height = 1000, pages_vertical_spacing = 10)

