# Introduction

We are going to start from the example of [Cynthia Huang

](https://www.cynthiahqy.com/posts/cv-html-pdf/) to see the basic framework.  She is building of the great work of [Quarto](https://quarto.org/) and [WeasyPrint](https://weasyprint.org/).  We would like to formalize a more robust resume tool.  The `Design Objectives` section has some of our goals.

## First steps

Use this repo as a template to get your base resume into the format.

### Design Objectives

- Have resume templates
- store resume information in tables for each section
- provide pythonic version for put and get data of the tables 
- build python app for the resume creation
- provide docker version for building resume
- Document local install or docker install
- build streamlit app to allow users to enter information into the tables
- provide autobuild method using Github actions
- provide AI text editing for bullets and description in the streamlit app


### Data Structure

Can we build the templates so they take from the general paradigms? 1) Schooling/Education, 2) Work Experience, 3) Community/Personal Projects, 4) Skills, 5) Publications, 6) Contact Information, 7) Teaching 

#### Schooling

- School:
- Degree:
- Graduation\Expected:
- Location:

#### Work Experience

- Position title:
- Company name:
- Location:
- start date:
- end date:
- bullets:

#### Projects

- Project Name:
- Project Purpose:
- Github repo:
- languages:
- start date:
- end date:

#### Skills

- skill:
- details:
- date start:
- projects using skill:
- work using skill:

#### publications

_Should we use a default format for these?_

- Title
- Authors
- Journal
- Publication
- date

#### Contact information

- Name:
- Email:
- github:
- linkedin:
- phonenumber:

#### Teaching

- Name:
- course id:
- Description:
- Link:
- bullets:
- semesters taught:
- date start:
- date end:
- developed:

## References

 - https://www.cynthiahqy.com/posts/cv-html-pdf/
 - https://quarto.org/docs/presentations/revealjs/index.html#multiple-columns
 - https://quarto.org/docs/computations/inline-code.html
 - https://quarto.org/docs/computations/parameters.html
 - https://quarto.org/docs/reference/formats/pdf.html
 - https://stackoverflow.com/questions/58175484/how-to-remove-margins-from-pdf-generated-using-weasyprint
 