// Create performance comparison chart
function createPerformanceChart() {
    const timeData = [{
        x: ['Original', 'Optimized'],
        y: [benchmarkData.time.original, benchmarkData.time.optimized],
        type: 'bar',
        marker: {
            color: ['#dc3545', '#28a745']
        },
        text: [
            benchmarkData.time.original.toFixed(2) + 's',
            benchmarkData.time.optimized.toFixed(2) + 's'
        ],
        textposition: 'auto',
    }];

    const timeLayout = {
        title: 'Average Processing Time (seconds)',
        yaxis: {
            title: 'Time (seconds)'
        },
        showlegend: false
    };

    Plotly.newPlot('timeChart', timeData, timeLayout);
}

// Create resource usage chart
function createResourceChart() {
    const resourceData = [{
        x: ['CPU Time', 'Memory Usage (MB)'],
        y: [benchmarkData.cpu.original, benchmarkData.memory.original],
        name: 'Original',
        type: 'bar'
    }, {
        x: ['CPU Time', 'Memory Usage (MB)'],
        y: [benchmarkData.cpu.optimized, benchmarkData.memory.optimized],
        name: 'Optimized',
        type: 'bar'
    }];

    const resourceLayout = {
        title: 'Resource Usage Comparison',
        barmode: 'group',
        yaxis: {
            title: 'Usage'
        }
    };

    Plotly.newPlot('resourceChart', resourceData, resourceLayout);
}

// Create iteration comparison chart
function createIterationChart() {
    const iterations = benchmarkData.detailedResults.map(r => r.name);
    const originalTimes = benchmarkData.detailedResults.map(r => r.original.time);
    const optimizedTimes = benchmarkData.detailedResults.map(r => r.optimized.time);

    const iterationData = [{
        x: iterations,
        y: originalTimes,
        name: 'Original',
        type: 'scatter',
        mode: 'lines+markers'
    }, {
        x: iterations,
        y: optimizedTimes,
        name: 'Optimized',
        type: 'scatter',
        mode: 'lines+markers'
    }];

    const iterationLayout = {
        title: 'Processing Time by Iteration',
        xaxis: {
            title: 'Iteration'
        },
        yaxis: {
            title: 'Time (seconds)'
        }
    };

    Plotly.newPlot('iterationChart', iterationData, iterationLayout);
}

// Initialize all charts
function initCharts() {
    createPerformanceChart();
    createResourceChart();
    createIterationChart();
}