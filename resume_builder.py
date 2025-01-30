import polars as pl
from IPython.display import Markdown

def print_bullets(dat):
  nbullets = dat.shape[0]

  if nbullets == 1:
    str_out = f"""
- {dat.item(0,"bullets")}
"""
  elif nbullets == 2:
    str_out = f"""
- {dat.item(0,"bullets")}
- {dat.item(1,"bullets")}
"""
  elif nbullets == 3:
    str_out = f"""
- {dat.item(0,"bullets")}
- {dat.item(1,"bullets")}
- {dat.item(2,"bullets")}
"""
  elif nbullets == 4:
    str_out = f"""
- {dat.item(0,"bullets")}
- {dat.item(1,"bullets")}
- {dat.item(2,"bullets")}
- {dat.item(3,"bullets")}
"""
  elif nbullets >= 5:
    sys.exit("Too many bullets. Must be less than 5.")
  else:
    sys.exit("No bullets found.")
  return str_out

def work_chunk(work):
  if work.shape[0] == 0:
    return Markdown('')
  else:
    p1 = work.select('position').item()
    c1 = work.select('company').item()
    l1 = work.select('location').item()
    s1 = work.select(pl.col('start').dt.to_string("%b %Y")).item()
    e1 = work.select(pl.col('end').dt.to_string("%b %Y")).item()
    b1 = work.select('bullets').item().split("- ")
    b1df = pl.DataFrame({"bullets":b1})\
      .filter(pl.col("bullets").str.len_chars() > 1)
    btext = print_bullets(b1df)
  
    return Markdown(f'''### {p1}
  ***{c1}*** [{s1} -- {e1}]{{.cvdate}}
  ''' + btext)
