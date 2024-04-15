const URL = `${window.location.origin}`
const times = Array.from({length: 24}, (_, i) => i);

function labelFormatter(timeLabel) {
    if (timeLabel < 10) return `0${timeLabel}:00`
    else return `${timeLabel}:00`
}

document.addEventListener("DOMContentLoaded", async function() {
    const data = await fetch(`${URL}/get_events/`).then((res) => res.json()).then((data) => data)
    const events = data.events
    console.log({events});

    window.ApexCharts && (new ApexCharts(document.getElementById("events-chart"), {
        chart: {
            type: "bar",
            fontFamily: 'inherit',
            height: 240,
            parentHeightOffset: 0,
            toolbar: {
                show: false,
            },
            animations: {
                enabled: false
            },
            stacked: true,
        },
        plotOptions: {
            bar: {
                barHeight: '50%',
            }
        },
        dataLabels: {
            enabled: false,
        },
        fill: {
            opacity: 1,
        },
        series: [{
            name: "Events",
            data: events
        }],
        grid: {
            padding: {
                top: -20,
                right: 0,
                left: -4,
                bottom: -4
            },
            strokeDashArray: 4,
        },
        xaxis: {
            labels: {
                padding: 0,
                formatter: labelFormatter,
            },
            tooltip: {
                enabled: false
            },
            axisBorder: {
                show: false,
            },
            categories: times,
        },
        yaxis: {
            labels: {
                padding: 4
            },
        },
        // colors: [tabler.getColor("purple"), tabler.getColor("green"), tabler.getColor("yellow"), tabler.getColor("red"), tabler.getColor("primary")],
        legend: {
            show: true,
            position: 'bottom',
            offsetY: 12,
            markers: {
                width: 10,
                height: 10,
                radius: 100,
            },
            itemMargin: {
                horizontal: 8,
                vertical: 8
            },
        },
    })).render();
});