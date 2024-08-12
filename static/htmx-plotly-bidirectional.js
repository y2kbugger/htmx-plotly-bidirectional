
htmx.defineExtension('htmx-plotly-bidirectional', {
    transformResponse : (text, xhr, elt) => {
        //// 1. Update the plotly plot //
        var plotIdElement = htmx.closest(elt, "[hx-pb-plotid]");
        if (!plotIdElement) { return text }

        const payload = JSON.parse(text)
        const plotlyJson = JSON.parse(payload['plotly_json'])
        text = payload['htmx_html']

        const plotid = plotIdElement.getAttribute('hx-pb-plotid');

        // Reacting with listeners causes odd events to fire, remove them first.
        const plotElement = document.getElementById(plotid)
        if (plotElement.on !== undefined) {
            plotElement.removeAllListeners()
        }

        // Create or update the plot
        Plotly.react(plotid, plotlyJson).then(() => {})


        //// 2. Attach plotly event hooks to DOM events //
        var plotEventsElement = htmx.closest(elt, "[hx-pb-plotevents]");
        if (!plotEventsElement) { return text }

        const eventNames = plotEventsElement.getAttribute('hx-pb-plotevents').split(/, */)
        eventNames.forEach(eventName => {
            plotElement.on(eventName, function(eventData) {
                const e = new CustomEvent(eventName, { bubbles: true, detail: eventData });
                plotElement.dispatchEvent(e);
            })
        })

        return text
    }
})
