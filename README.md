# htmx-plotly-bidirection
[![](https://data.jsdelivr.com/v1/package/gh/y2kbugger/htmx-plotly-bidirectional/badge)](https://www.jsdelivr.com/package/gh/y2kbugger/htmx-plotly-bidirectional)

Bidirectional communication between Plotly and HTMX.

- HTMX controls can update Plotly charts on the page.
- Plotly events can trigger HTMX updates (either on the page or the plot itself).


# Install

We assume you have correctly installed both HTMX and Plotly on your page.

To use our CDN (a passthrough to the latest version on github):

```html
<script src="https://cdn.jsdelivr.net/gh/y2kbugger/htmx-plotly-bidirectional@master/static/htmx-plotly-bidirectional.js" crossorigin="anonymous"></script>
```

# Examples
Please see `templates/index.html` for a full the front-end usage.

Find the back-end FastApi example in `server.py`
