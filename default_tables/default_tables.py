# %%
import polars as pl
import pandas as pd
# %%
#### Contact information: Name, Email, github, linkedin, phonenumber, 
contact = pl.DataFrame({
  "name": "Joseph Smith",
  "email": "smithj@msdn.com",
  "github": "smithj",
  "linkedin": "smithj",
  "phone":"208.656.8301"
})

#### Schooling: School, Degree, Graduation\Expected, Location, 
# Each row is a school, sorted after creation by descending date
education = pl.DataFrame({
  "school": ["Brigham Young University - Idaho"],
  "location": ["Rexburg, ID"],
  "degree": ["Data Science"],
  "expected": ["2024-12-01"]}).with_columns(pl.col("expected").str.to_date()).sort("expected", descending=True)
### Work Experience: Position title, Company name, Location, start date, end date, bullets
work = pl.DataFrame({
  "position": ["Jnr. Data Scientist"],
  "company": ["EventX Developers"],
  "location": ["Provo, UT"],
  "start": ["2024-04-01"],
  "end": ["2100-12-31"],
  "bullets": ["- Supported the transition from PowerBI to Streamlit for dashboarding.- Leveraged Streamlit, Polars, Plotly, and GT to build a fully pythonic dashboard framework.- Automated dashboard development pipeline to save over 300 hours a month in employee time."]
}).with_columns(pl.col("start").str.to_date(), pl.col("end").str.to_date())

#### Projects: Project Name, Project Purpose, Github repo, languages, start date, end date, 
projects = pl.DataFrame({
  "name": ["Data Informed Resumes"],
  "purpose": ["Automated resume creation based on position using a table centric approach."],
  "github": ["https://github.com/byuidatascience/quarto_resumes"],
  "languages": ["Python (Polars, Streamlit, GT), JS (React), SQL"],
  "start": ["2024-01-01"],
  "end": ["2024-04-01"]
}).with_columns(pl.col("start").str.to_date(), pl.col("end").str.to_date())
#### Skills: skill, details, date start, projects using skill, work using skill, 

skills = pl.DataFrame({
  "topic": ["languages", "languages", "languages", "leadership", "leadership"],
  "skill": ["Python", "R", "SQL", "Team Management", "Product Design"],
  "details": ["Polars, Streamlit, Plotly, LetsPlot, Pandas",
    "dplyr, ggplot2, lubridate, purrr, furrr",
    "Spark, Postgres",
    "Consulting, Team Lead, Project Management, Teacher",
    "Course developer, Design Thinking, Software Design"],
  "start":["2023-09-15", "2023-01-15", "2022-09-10", "2020-09-10", "2020-09-10"],
  "projects": ["Data Informed Resumes", pl.Null(), "Data Informed Resumes", pl.Null(), pl.Null()],
  "company":["EventX Developers", pl.Null(), "EventX Developers", pl.Null(), pl.Null()]
}, strict=False).with_columns(pl.col("start").str.to_date())
#### publications: Title, Authors, Journal, Publication, date
#### Teaching: Name, course id, Description, Link, bullets, semesters taught, date start, date end, developed,



# %%
projects.write_parquet("projects.parquet")
skills.write_parquet("skills.parquet")
work.write_parquet("work.parquet")
education.write_parquet("education.parquet")
contact.write_parquet("contact.parquet")
# %%
