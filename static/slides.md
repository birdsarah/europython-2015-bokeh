
# Getting started with Bokeh 
Let's build an interactive data visualization for the web...

## in Python! 

#### Sarah Bird - Europython 2015

![Bokeh logo](images/logo.svg)

---
<a href="http://localhost:5000">Live demo....</a>
![Sneak Peak](images/dashboard.png)

---

### app

github.com/birdsarah/gtimelog-viz

### slides

birdsarah.github.io/europython-2015-bokeh

### me

@birdsarah

---

# Bokeh
<img class="slide_image" src="images/gallery-screenshot.png">

* data visualization library
 * d3.js & many more
 * matplotlib / seaborn
* web
* interactive
* dynamic & data-driven
* roots in data science

---

# Why bokeh?

from data science:

* interactive
* web - publishing & portability

from web dev:

* python vs javascript
* mid-sized data 1-10k | 10-100k

both:

* intuitive
* server-side processing & updating
* fully open-source

---

![Sneak Peak](images/dashboard.png)

---

![How it works](images/bokeh_basic.svg)

---

![Tentacles](images/bokeh_with_tentacle.svg)

---

![Mockup](images/dashboard_v1.png)

---

![Mockup](images/dashboard_v1_comments.png)

---


`conda install bokeh`

`pip install bokeh`

****
optional

`conda install ipython-notebook pandas`

`pip install "ipython[notebook]" pandas`


---

## bokeh.models (high customization)


* The lowest level
* Offers you the most control
* Do all the work yourself

<p></p>

## bokeh.plotting

* Tries to pick sensible defaults
* You organize your data, it organizes your plot
<p></p>

## bokeh.charts (high speed)

* One-line charts
* Processes your data & spits out a chart

---

* data
* io
* charts 
* plotting 
* models 
* layout
* embedding
* styling
* interactive

.... and there's more in a couple of hours - Fabio Pliger's talk.
---

# Data.....

At the heart of Bokeh is the `ColumnDataSource`

| 'column of xs' | 'column of ys'
|---|---
|0|1 
|1|2
|3|4

[notebooks/ColumnDataSource.ipynb](http://localhost:8888/notebooks/notebooks/ColumnDataSource.ipynb)

---

and the `Plot`

```python
from bokeh.models import Plot
p = Plot
```
```python
from bokeh.plotting import figure
p = figure()
```
```python
from bokeh.plotting import Chart
p = Chart()
```
They're basically the same thing with the same key methods/attributes on them.

[notebooks/Plot.ipynb](http://localhost:8888/notebooks/notebooks/Plot.ipynb)

---
# chart

![Bar chart](images/bar_chart.png)

[notebooks/Chart.ipynb](http://localhost:8888/notebooks/notebooks/Chart.ipynb)

---
# io

output_notebook
```python
from bokeh.io import output_notebook, show
output_notebook()

bar = Bar(bar_df, stacked=True, palette=['purple', 'gray'])

show(bar)
```

output_file
```python
from bokeh.io import output_file, show
output_file('my_bar_chart.html', mode='cdn')  # CDN mode keeps your output small

bar = Bar(bar_df, stacked=True, palette=['purple', 'gray'])

show(bar)  # Also see save(bar)
```

---

# Plotting

![Plotting](images/plotting.png)

[notebooks/Plotting.ipynb](http://localhost:8888/notebooks/notebooks/Plotting.ipynb)

---

# Plotting
````python
source = ColumnDataSource(data)
p = figure(
    x_range=Range1d(start, end),  # start & end time for x_range 
    y_range=FactorRange(factors=activities), # list of categoeis for y_range
    plot_height=300, plot_width=800
)
p.quad(left='start', right='end', top='activity_top', bottom='activity_bottom', source=source)
````
---


---

Which one should I pick?

* Making your website - models
* Poking data - charts
* More complex poking or presenting to colleagues - plotting

They're all the same thing though

---

# Further reading

* Exporting & Embedding - [bokeh.pydata.org/docs/reference/resources_embedding.html](http://bokeh.pydata.org/docs/reference/resources_embedding.html)
* User guide - [bokeh.pydata.org/docs/user_guide.html](http://bokeh.pydata.org/docs/user_guide.html)
* Tutorial notebooks - [github.com/bokeh/bokeh-notebooks/tutorial](http://github.com/bokeh/bokeh-notebooks/tutorial)
