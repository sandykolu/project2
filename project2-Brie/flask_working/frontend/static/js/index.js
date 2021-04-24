// bar chart of top 10 states by casualties
d3.json("http://localhost:5000/api/top10").then(function(top10){
 
    console.log(top10)

    var layout = {
        title: "States with Highest Tornado Casualties",
        xaxis: {title: "States"},
        yaxis: {title: "Number of Casualties"}

    };

    Plotly.newPlot('bar', top10, layout);
});