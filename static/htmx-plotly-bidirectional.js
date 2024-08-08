
htmx.defineExtension('htmx-plotly-bidirectional', {
    transformResponse : (text, xhr, elt) => {
        var plotEl = htmx.closest(elt, "[hx-pb-plotid]");
        if (!plotEl) { return text }

        const payload = JSON.parse(text)
        const plotlyJson = JSON.parse(payload['plotly_json'])
        text = payload['htmx_html']

        const plotid = plotEl.getAttribute('hx-pb-plotid');
        Plotly.newPlot(plotid, plotlyJson)

        return text
    }
})
