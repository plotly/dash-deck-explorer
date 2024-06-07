<!--
To get started, replace
Dash Deck Explorer with your app name (e.g. Dash Super Cool App)
deck-explorer with the short handle (e.g. dash-super-cool)

If this is in dash sample apps, uncomment the second "git clone https..." and remove the first one.
If this is in dash sample apps and you have a colab demo, uncomment the "Open in Colab" link to see the badge (make sure to create a ColabDemo.ipynb) first.

-->
# Dash Deck Explorer
<!-- 
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/plotly/dash-sample-apps/blob/master/apps/deck-explorer/ColabDemo.ipynb)
 -->

 <div align="center">
  <a href="https://dash.plotly.com/project-maintenance">
    <img src="https://dash.plotly.com/assets/images/maintained-by-plotly.png" width="400px" alt="Maintained by Plotly">
  </a>
</div>


[Click here for demo](https://dash-gallery.plotly.host/dash-deck-explorer/arc-layer)

This is the companion explorer app for the [dash-deck](https://github.com/plotly/dash-deck) library. For more information, see the repo.

## Instructions

To get started, first clone this repo:

```
git clone https://github.com/plotly/dash-deck-explorer.git
cd deck-explorer
```

<!--
```
git clone https://github.com/plotly/dash-sample-apps.git
cd dash-sample-apps/apps/deck-explorer
```
-->

Create and activate a conda env:
```
conda create -n deck-explorer python=3.7.6
conda activate deck-explorer
```

Or a venv (make sure your `python3` is 3.6+):
```
python3 -m venv venv
source venv/bin/activate  # for Windows, use venv\Scripts\activate.bat
```

Install all the requirements:

```
pip install -r requirements.txt
```

You can now run the app:
```
python app.py
```

and visit http://127.0.0.1:8050/.

## Contact

Interested in building or deploying apps like this? [Reach out](https://plotly.com/contact-us/) or [get a demo](https://plotly.com/get-demo).
