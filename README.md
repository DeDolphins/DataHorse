# 🎉 Do data science and data analysis in plain english 🌟

<p align="">
  <a href="https://datahorse.ai/">
    <img src="image.png" height="">
  </a>
  <h1 align="center">
    <a href="https://datahorse.ai/">DataHorse</a>
  </h1>
</p>

<p align="center">
  <a href="https://www.linkedin.com/showcase/data-horse"> 
    <img
      src="https://img.shields.io/badge/LINKEDIN-blue.svg?style=for-the-badge&logo=read-the-docs&logoColor=white&labelColor=000000&logoWidth=20">
  </a>
</p>

🚀 **DataHorse** is an open-source tool and Python library that simplifies data science for everyone. It lets users interact with data in plain English 📝, without needing technical skills or watching tutorials 🎥 to learn how to use it. With DataHorse, you can create graphs 📊, modify data 🛠️, and even create smart systems called machine learning models 🤖 to get answers or make predictions. It’s designed to help businesses and individuals 💼 regardless of knowledge background to quickly understand their data and make smart, data-driven decisions, all with ease. ✨

## Quick Installation

```bash
pip install datahorse
```

## Examples

Setup and usage examples are available in this **[Google Colab notebook](https://colab.research.google.com/drive/1brAw2Qj_VnlTbzcfjm5sCOaQbNl7Disd?usp=sharing)**.

```python
import datahorse

df = datahorse.read('https://raw.githubusercontent.com/plotly/datasets/master/iris-data.csv')

# Data transformation
df = df.chat('convert species names to numeric codes')
df = df.chat('add a new column "petal_area" calculated as petal_length * petal_width')

# Queries
average_measurements = df.chat('what are the average sepal length and petal width for each species?')
species_count = df.chat('how many samples are there for each species?')
largest_petal_length = df.chat('which species has the largest petal length?')

# Plotting
df.chat('scatter plot of sepal length vs petal length by species')
df.chat('histogram of petal width')
df.chat('box plot of sepal length distribution by species')
```