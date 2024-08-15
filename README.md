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
We’re using an Irish dataset as an example to demonstrate how DataHorse simplifies data analysis. This example showcases how our tool can handle real-world data, making it easier to work with and understand.

Setup and usage examples are available in this **[Google Colab notebook](https://colab.research.google.com/drive/1brAw2Qj_VnlTbzcfjm5sCOaQbNl7Disd?usp=sharing)**.

```python
import datahorse

df = datahorse.read('https://raw.githubusercontent.com/plotly/datasets/master/iris-data.csv')
```

## Data transformation
Data transformation means changing data into a format that’s easier to work with. This can involve fixing errors, combining data, standardizing formats, or changing how data is organized. It helps make sure data is clean, consistent, and ready for analysis or other uses.

```python
df = df.chat('convert species names to numeric codes')
```

 <img src="#">

```python
df = df.chat('add a new column "petal_area" calculated as petal_length * petal_width')
```

<img src="#">

## Data analysis
Data analysis involves examining data to find useful patterns or insights. In DataHorse, data analysis involves using natural language to interact with and understand your data. Instead of writing complex code, you can ask questions and get insights directly. This simplifies finding patterns and making decisions from your data.

# Queries

```python
average_measurements = df.chat('what are the average sepal length and petal width for each species?')
```

<img src="#">

```python
species_count = df.chat('how many samples are there for each species?')
```

<img src="#">

```python
largest_petal_length = df.chat('which species has the largest petal length?')
```

<img src="#">

## Data visualization
Data visualization with DataHorse means turning data into easy-to-understand charts and graphs using simple language. Instead of just numbers, DataHorse creates clear visuals that highlight patterns and trends, making it simpler to understand and analyze the information quickly.

# Plotting
```python
df.chat('Display a pair plot that shows scatter plots for each pair of features and includes color-coding by species.')
```

<img src="#">

```python
df.chat('Show a pair plot that includes scatter plots for each pair of features, and histograms along the diagonal to show the distribution of each feature.')
```

<img src="#">

```python
df.chat('scatter plot of sepal length vs petal length by species')
```

<img src="#">

```python
df.chat('histogram of petal width')
```

<img src="#">

```python
df.chat('box plot of sepal length distribution by species')
```

<img src="#">

