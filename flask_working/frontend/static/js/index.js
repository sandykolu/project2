// // mongo import data
// d3.json("http://localhost:5000/api/mongo").then(function(geo) {
//     console.log("mongo endpoint")
//     console.log(geo)
// })

// bar chart of top 10 states by casualties
d3.json("http://localhost:5000/api/top10").then(function(top10){
 
    console.log(top10)

    var layout = {
        title: "Highest Tornado Casualties (2010 - 2015)",
        xaxis: {title: "States"},
        yaxis: {title: "Number of Casualties"}

    };

    Plotly.newPlot('bar', top10, layout);
});