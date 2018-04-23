
var svg = d3.selectAll("#viz")
.append("svg")
.attr("width", "100%")
.attr("height", "100%")
.attr("class", "svg");

var w=$("svg").width();
var h=$("svg").height();

var timeScale;
var colorScale;
var svg = d3.select('svg');

var taskArray = appConfig.dataset[0];
var taskArray2 = appConfig.dataset[1];
var extra = appConfig.dataset[2];
console.log(taskArray2)

function render(d3Comparator) {
    if(d3Comparator) taskArray = taskArray.sort(function(a, b) {
        return d3[d3Comparator](a.location, b.location);
    });
}
render('ascending');

timeScale = d3.scaleTime()
        .domain([d3.min(taskArray, function(d) {return new Date(d.startTime);}),
                 d3.max(taskArray, function(d) {return new Date(d.endTime);})])
        .range([0,w-225]);


var categories = d3.map(taskArray, function(d){return d.location;}).keys();
var categories2 = d3.map(taskArray2, function(d){return d.sensor;}).keys();

var locations = {};
for (var i = 0; i < categories.length; i++) {
  category = categories[i];
  locations[category] = i;
}

var location_levels = {};

makeGant(taskArray, taskArray2, locations, categories, categories2, w, h);

function makeGant(tasks, tasks2, locations, categories, categories2, width, height){
  var vertPad = 25;
  var horiPad = 175;
  var sectionHeight = (height-vertPad*1.5)/categories.length;
  
  var barHeight = sectionHeight/8;

  colorScale = d3.scaleLinear()
      .domain([0, categories.length])
      .range(["#F0B27A", "#85C1E9"])
      .interpolate(d3.interpolateHcl);

  makeGrid(horiPad, vertPad, width, height);
  console.log(tasks)
  console.log(tasks2)
  console.log(locations)
  console.log(categories)
  console.log(categories2)
  drawSections(categories, vertPad, sectionHeight, width, height);
  //drawSectionLabels(categories, sectionHeight, colorScale);
  drawBars(tasks, locations, categories, horiPad, sectionHeight, barHeight, width, height, "locationBar", "gray", 0);
  for (var i = 0; i < categories2.length; i++) {
    category = categories2[i]
    tempTasks = [];
    for (var j = 0; j < tasks2.length; j++) {
      task = tasks2[j];
      if (task.sensor == category) {
        tempTasks.push(task);
      }
    }
    // tempTasks = d3.map(tasks2, function(d){ 
    //   if (d.sensor == category) {
    //     return d;
    //   }
    // })
    console.log(tempTasks);
    loc = tempTasks[0].location
    if (loc in location_levels) {
      location_levels[loc] += 1;
    } else {
      location_levels[loc] = 1;
    }

    drawBars(tempTasks, locations, categories2, horiPad, sectionHeight, barHeight, width, height, "sensorBar-" + category, d3.rgb(colorScale(locations[loc])), location_levels[loc], true);
  }
  
}

function makeGrid(leftPad, vertPad, width, height){
  var xAxis = d3.axisBottom(timeScale)
      .ticks(8)
      .tickSize(-height+vertPad, 0, 0)
      .tickFormat(d3.timeFormat('%d%b %H:%M')); // S: change this to shift between differnt time format format for x axis

  var grid = svg.append('g')
      .attr('class', 'grid')
      .attr('transform', 'translate(' + leftPad + ', ' + (height - vertPad) + ')')
      .call(xAxis)
      .selectAll("text")  
        .style("text-anchor", "middle")
        .attr("fill", "#000")
        .attr("stroke", "none")
        .attr("font-size", 12)
        .attr("dy", "1em");
}

var sections;
var bars;

// draw bigger rectangle
function drawSections(categories, vertPad, sectionHeight, width, height){

  sections = svg.selectAll(".section")
      .data(categories)
      .enter()
      .append("g")
      .attr("class", "section")
      .attr("transform", function(d, i) {
          return "translate(0," + (i*sectionHeight) + ")";
      })
      .attr("x", 0)
      .attr("y", function(d, i){
        return i*sectionHeight;
      });
      

  sections.append("rect")
      .attr("stroke", "none")
      .attr("fill", function(d, i){
        return d3.rgb(colorScale(i));
      })
      .attr("opacity", 0.4)
      .attr("width", function(d){
        return width;
      })
      .attr("height", sectionHeight);
      
  sections.append("text")
      .text(function(d) {
        return d;
      })
      .attr("x", 10)
      .attr("y", function(d, i) {
        return sectionHeight/2;
      })
      .attr("font-size", 14)
      .attr("text-anchor", "start")
      .attr("text-height", 14)
      .attr("fill", function(d, i){
        return "gray";
      });
}

function drawBars(tasks, locations, categories, horiPad, sectionHeight, barHeight, width, height, className, color, level, sensors) {

  console.log(tasks)

  bars = svg.selectAll("." + className)
      .data(tasks)
      .enter()
      .append("rect")
      .attr("class", className + " bar")
      .attr("x", function(d) {
        console.log(d)
        return timeScale(new Date(d.startTime)) + horiPad;
      })
      .attr("y", function(d, i) {
        index = locations[d.location]
        console.log(index)
        console.log(sectionHeight)
        return ((index)*sectionHeight)+(level*barHeight)+(barHeight);
      })
      .attr("width", function(d){
        return (timeScale(new Date(d.endTime))-timeScale(new Date(d.startTime)));
      })
      .attr("height", barHeight)
      .attr("stroke", "none")
      .attr("fill", color);

  bars.on('mouseover', function(e) {

    var tag = "";
    if (sensors) {
      tag = "Sensor: " + d3.select(this).data()[0].sensor + "<br/>" +
        "Location: " + d3.select(this).data()[0].location + "<br/>" + 
        "Starts: " + d3.select(this).data()[0].startTime + "<br/>" + 
        "Ends: " + d3.select(this).data()[0].endTime;
    } else {
      tag = "Location: " + d3.select(this).data()[0].location + "<br/>" + 
        "Starts: " + d3.select(this).data()[0].startTime + "<br/>" + 
        "Ends: " + d3.select(this).data()[0].endTime;
    }
    var output = document.getElementById("tag");

    var x = (this.x.animVal.value + this.width.animVal.value/2) + "px";
    var y = this.y.animVal.value + 25 + "px";

    output.innerHTML = tag;
    output.style.top = y;
    output.style.left = x;
    output.style.display = "block";
    }).on('mouseout', function() {
      var output = document.getElementById("tag");
      output.style.display = "none";

  });

}

// function drawSectionLabels(categories, sectionHeight, colorScale){
//   var numOccurances = new Array();
//   var prevGap = 0;

//   for (var i = 0; i < categories.length; i++){
//     numOccurances[i] = [categories[i], getCount(categories[i], catsUnfiltered)];
//   }

//   var axisText = svg.append("g") //without doing this, impossible to put grid lines behind text
//    .selectAll("text")
//    .data(numOccurances)
//    .enter()
//    .append("text")
//    .text(function(d){
//     return d[0];
//    })
//    .attr("x", 10)
//    .attr("y", function(d, i){
//     // if (i > 0){
//     //     for (var j = 0; j < i; j++){
//     //       prevGap += numOccurances[i-1][1];
//     //      // console.log(prevGap);
//     //       return d[1]*theGap/2 + prevGap*theGap + theTopPad;
//     //     }
//     // } else{
//     // return d[1]*theGap/2 + theTopPad;
//     // }
//     index = categories.findIndex(x => x==d[0])
//     console.log(index)
//     console.log(theGap)

//     return index*(theGap*1.2) + theTopPad;
//    })
//    .attr("font-size", 11)
//    .attr("text-anchor", "start")
//    .attr("text-height", 14)
//    .attr("fill", function(d){
//     for (var i = 0; i < categories.length; i++){
//         if (d[0] == categories[i]){
//         //  console.log("true!");
//           return d3.rgb(theColorScale(i)).darker();
//         }
//     }
//    });

// }

// draw location rectangles







//from this stackexchange question: http://stackoverflow.com/questions/1890203/unique-for-arrays-in-javascript
function checkUnique(arr) {
    var hash = {}, result = [];
    for ( var i = 0, l = arr.length; i < l; ++i ) {
        if ( !hash.hasOwnProperty(arr[i]) ) { //it works with objects! in FF, at least
            hash[ arr[i] ] = true;
            result.push(arr[i]);
        }
    }
    return result;
}

//from this stackexchange question: http://stackoverflow.com/questions/14227981/count-how-many-strings-in-an-array-have-duplicates-in-the-same-array
function getCounts(arr) {
    var i = arr.length, // var to loop over
        obj = {}; // obj to store results
    while (i) obj[arr[--i]] = (obj[arr[i]] || 0) + 1; // count occurrences
    return obj;
}

// get specific from everything
function getCount(word, arr) {
    return getCounts(arr)[word] || 0;
}
