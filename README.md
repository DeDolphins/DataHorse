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
- `seed=int`: Ensures that the generated function is reproducible across different runs.
- `cache_req=True`: Enables caching for the API request, ensuring that identical prompts won't trigger unnecessary API calls.

```python
df = df.chat('convert species names to numeric codes', seed=int, cache_req=True)
```
 <img src="images/Species names to numeric codes.jpeg">


## Data analysis
Data analysis involves examining data to find useful patterns or insights. In DataHorse, data analysis involves using natural language to interact with and understand your data. Instead of writing complex code, you can ask questions and get insights directly. This simplifies finding patterns and making decisions from your data.

# Queries

```python
average_measurements = df.chat('what are the average sepal length and petal width for each species?')
```

<img src="images/avarage.jpeg">


## Data visualization
Data visualization with DataHorse means turning data into easy-to-understand charts and graphs using simple language. Instead of just numbers, DataHorse creates clear visuals that highlight patterns and trends, making it simpler to understand and analyze the information quickly.

# Plotting
```python
df.chat('Display a pair plot that shows scatter plots for each pair of features and includes color-coding by species.')
```

<img src="images/pair_scatter_plots.png">

```python
df.chat('Show a pair plot that includes scatter plots for each pair of features, and histograms along the diagonal to show the distribution of each feature.')
```

<img src="images/scatter_histograms.png">

# Guide for running the DataHorse WebUI
## Clone the repository
```bash
git clone https://github.com/DeDolphins/DataHorse.git
```
## Go to the directory
```bash
cd DataHorseUI
```
## Install the requirements
```bash
pip install -r requirements.text
```
## Run DataHorse WebUI
```bash
streamlit run app.py
```
<img src="demo/datahorseUI.gif">

## Contribute

Found a bug or have an improvement in mind? Fantastic!

Got a solution ready? That's even better!

Ready to share it with us? We're all ears!

Start at the [contributing guide](https://github.com/DeDolphins/DataHorse/blob/main/CONTRIBUTION.md)!
