var data = [
  {
    name: "Cooking",
    values: [
      {date: "04/05/2018", duration: "2"},
      {date: "04/06/2018", duration: "3"},
      {date: "04/07/2018", duration: "2"},
      {date: "04/08/2018", duration: "4"},
      {date: "04/09/2018", duration: "4"},
      {date: "04/10/2018", duration: "5"},
      {date: "04/11/2018", duration: "5"},
      {date: "04/12/2018", duration: "5"},
    ]
  },
  {
    name: "Sleeping",
    values: [
      {date: "04/05/2018", duration: "7"},
      {date: "04/06/2018", duration: "9"},
      {date: "04/07/2018", duration: "11"},
      {date: "04/08/2018", duration: "11"},
      {date: "04/09/2018", duration: "10"},
      {date: "04/10/2018", duration: "12"},
      {date: "04/11/2018", duration: "12"},
      {date: "04/12/2018", duration: "12"},
    ]
  },
  {
    name: "Entertainment",
    values: [
      {date: "04/05/2018", duration: "5"},
      {date: "04/06/2018", duration: "4"},
      {date: "04/07/2018", duration: "4"},
      {date: "04/08/2018", duration: "5"},
      {date: "04/09/2018", duration: "5"},
      {date: "04/10/2018", duration: "4"},
      {date: "04/11/2018", duration: "2"},
      {date: "04/12/2018", duration: "1"},

    ]
  }
];

var width = 800;
var height = 600;
var margin = 50;
var duration = 24;

var lineOpacity = "0.25";
var lineOpacityHover = "0.85";
var otherLinesOpacityHover = "0.1";
var lineStroke = "1.5px";
var lineStrokeHover = "2.5px";

var circleOpacity = '0.85';
var circleOpacityOnLineHover = "0.25"
var circleRadius = 3;
var circleRadiusHover = 6;


/* Format Data */
var parseDate = d3.timeParse("%m/%d/%Y");
data.forEach(function(d) { 
  d.values.forEach(function(d) {
    d.date = parseDate(d.date);
    d.duration = +d.duration;    
  });
});


/* Scale */
var xScale = d3.scaleTime()
  .domain(d3.extent(data[0].values, d => d.date))
  .range([0, width-margin]);

var yScale = d3.scaleLinear()
  .domain([0, 12])
  .range([height-margin, 0]);

var color = d3.scaleOrdinal(d3.schemeCategory10);

/* Add SVG */
var svg = d3.select("#chart").append("svg")
  .attr("width", (width+margin)+"px")
  .attr("height", (height+margin)+"px")
  .append('g')
  .attr("transform", `translate(${margin}, ${margin})`);


/* Add line into SVG */
var line = d3.line()
  .x(d => xScale(d.date))
  .y(d => yScale(d.duration));

let lines = svg.append('g')
  .attr('class', 'lines');

lines.selectAll('.line-group')
  .data(data).enter()
  .append('g')
  .attr('class', 'line-group')  
  .on("mouseover", function(d, i) {
      svg.append("text")
        .attr("class", "title-text")
        .style("fill", color(i))        
        .text(d.name)
        .style("font", "30px times")
        .attr("text-anchor", "middle")
        .attr("x", (width-margin)/2)
        .attr("y", 5);
    })
  .on("mouseout", function(d) {
      svg.select(".title-text").remove();
    })
  .append('path')
  .attr('class', 'line')  
  .attr('d', d => line(d.values))
  .style('stroke', (d, i) => color(i))
  .style('opacity', lineOpacity)
  .on("mouseover", function(d) {
      d3.selectAll('.line')
					.style('opacity', otherLinesOpacityHover);
      d3.selectAll('.circle')
					.style('opacity', circleOpacityOnLineHover);
      d3.select(this)
        .style('opacity', lineOpacityHover)
        .style("stroke-width", lineStrokeHover)
        .style("cursor", "pointer");
    })
  .on("mouseout", function(d) {
      d3.selectAll(".line")
					.style('opacity', lineOpacity);
      d3.selectAll('.circle')
					.style('opacity', circleOpacity);
      d3.select(this)
        .style("stroke-width", lineStroke)
        .style("cursor", "none");
    });


/* Add circles in the line */
lines.selectAll("circle-group")
  .data(data).enter()
  .append("g")
  .style("fill", (d, i) => color(i))
  .selectAll("circle")
  .data(d => d.values).enter()
  .append("g")
  .attr("class", "circle")  
  .on("mouseover", function(d) {
      d3.select(this)     
        .style("cursor", "pointer")
        .append("text")
        .attr("class", "text")
        .text(d.duration + "hours")
        .attr("x", d => xScale(d.date) + 5)
        .attr("y", d => yScale(d.duration) - 10);
    })
  .on("mouseout", function(d) {
      d3.select(this)
        .style("cursor", "none")  
        .transition()
        .duration(duration)
        .selectAll(".text").remove();
    })
  .append("circle")
  .attr("cx", d => xScale(d.date))
  .attr("cy", d => yScale(d.duration))
  .attr("r", circleRadius)
  .style('opacity', circleOpacity)
  .on("mouseover", function(d) {
        d3.select(this)
          .transition()
          .duration(duration)
          .attr("r", circleRadiusHover);
      })
    .on("mouseout", function(d) {
        d3.select(this) 
          .transition()
          .duration(duration)
          .attr("r", circleRadius);  
      });


/* Add Axis into SVG */
var xAxis = d3.axisBottom(xScale).ticks(d3.timeDay.every(1));
var yAxis = d3.axisLeft(yScale);

svg.append("g")
  .attr("class", "x axis")
  .attr("transform", `translate(0, ${height-margin})`)
  .call(xAxis);

var h = height-margin +40
 svg.append("text")   
      .attr("transform", 
          "translate(" + 400 + "," + h + ")")          
      .style("text-anchor", "middle")
      .text("Date");

svg.append("g")
  .attr("class", "y axis")
  .call(yAxis)
  .append('text')
  .attr("y", -35)
  .attr("x", -160)
  .attr("transform", "rotate(-90)")
  .attr("fill", "#000")
  .text("Total Hours Spent")
  .style("font", "16px times");

