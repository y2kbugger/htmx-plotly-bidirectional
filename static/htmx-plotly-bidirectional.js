
htmx.defineExtension('htmx-plotly-bidirectional', {
    transformResponse : (text, xhr, elt) => {
        var plotIdElement = htmx.closest(elt, "[hx-pb-plotid]");
        if (!plotIdElement) { return text }

        const payload = JSON.parse(text)
        const plotlyJson = JSON.parse(payload['plotly_json'])
        text = payload['htmx_html']

        const plotid = plotIdElement.getAttribute('hx-pb-plotid');
        // if plot already exists (div not empty), update it with react
        if (document.getElementById(plotid).children.length > 0) {
            // Plotly.react(plotid, plotlyJson)
            // return text
            Plotly.newPlot(plotid, plotlyJson)
        } else {
            Plotly.newPlot(plotid, plotlyJson)
        }


        var plotEventsElement = htmx.closest(elt, "[hx-pb-plotevents]");
        if (!plotEventsElement) { return text }

        const plotElement = document.getElementById(plotid)
        const eventNames = plotEventsElement.getAttribute('hx-pb-plotevents').split(/, */)

        eventNames.forEach(eventName => {
            plotElement.on(eventName, function(eventData) {
                console.log('Event:', eventName, eventData);
                const domevent = new CustomEvent(eventName, { bubbles: true, detail: eventData });
                plotElement.dispatchEvent(domevent);
            })
        })

        return text
    }
})
