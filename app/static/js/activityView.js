  var w = 1000;
  var h = 400;

  var svg = d3.selectAll(".svg")
  .append("svg")
  .attr("width", w)
  .attr("height", h)
  .attr("class", "svg");

var timeScale
var colorScale
var svg = d3.select('svg');


// activity data
var dataset = appConfig.dataset;

console.log(dataset);


function render(d3Comparator) {
    if(d3Comparator) dataset = dataset.sort(function(a, b) {
        return d3[d3Comparator](a.location, b.location);
    });
}
render('ascending');


taskArray = dataset;

timeScale = d3.scaleTime()
        .domain([d3.min(taskArray, function(d) {return new Date(d.startTimeActivity);}),
                 d3.max(taskArray, function(d) {return new Date(d.endTimeActivity);})])
        .range([0,w-150]);

var categories = new Array();

for (var i = 0; i < taskArray.length; i++){
    categories.push(taskArray[i].location);
}

var catsUnfiltered = categories; //for vert labels

categories = checkUnique(categories);

console.log(categories);
makeGant(taskArray, w, h);

var title = svg.append("text")
.text("Patient's Activities")
.attr("x", w/2)
.attr("y", 25)
.attr("text-anchor", "middle")
.attr("font-size", 18)
.attr("fill", "#009FFC");


function makeGant(tasks, pageWidth, pageHeight){

var barHeight = 20;
var gap = barHeight + 4;
var topPadding = 75;
var sidePadding = 75;
var smallBaHeight = 10;
colorScale = d3.scaleLinear()
    .domain([0, categories.length])
    .range(["#F0B27A", "#85C1E9"])
    .interpolate(d3.interpolateHcl);

makeGrid(sidePadding, topPadding, pageWidth, pageHeight);
drawRects(tasks, gap, topPadding, sidePadding, barHeight, colorScale, pageWidth, pageHeight);
vertLabels(gap, topPadding, sidePadding, barHeight, colorScale);
}


var bigRects
var rectangles

// draw big rectangles + activity rectangles
function drawRects(theArray, theGap, theTopPad, theSidePad, theBarHeight, theColorScale, w, h){
var bigRects = svg.append("g")
    .selectAll("rect")
   .data(theArray)
   .enter()
   .append("rect")
   .attr("x", 0)
   .attr("y", function(d, i){
      return i*theGap + theTopPad - 2;
  })
   .attr("width", function(d){
      return w-theSidePad/2;
   })
   .attr("height", theGap)
   .attr("stroke", "none")
   .attr("fill", function(d){
    for (var i = 0; i < categories.length; i++){
        if (d.location == categories[i]){
          return d3.rgb(theColorScale(i));
        }
    }
   })
   .attr("opacity", 0.2);


     var rectangles = svg.append('g')
     .selectAll("rect")
     .data(theArray)
     .enter();


   var innerRects = rectangles.append("rect")
             .attr("rx", 3)
             .attr("ry", 3)
             .attr("x", function(d){
              return timeScale(new Date(d.startTimeActivity)) + theSidePad;
              })
             .attr("y", function(d, i){
                return i*theGap + theTopPad;
            })
             .attr("width", function(d){
                return (timeScale(new Date(d.endTimeActivity))-timeScale(new Date(d.startTimeActivity)));
             })
             .attr("height", theBarHeight)
             .attr("stroke", "none")
             .attr("fill", function(d){
              for (var i = 0; i < categories.length; i++){
                  if (d.location == categories[i]){
                    return d3.rgb(theColorScale(i));
                  }
              }
             })

          innerRects.on('mouseover', function(e) {

                   var tag = "";
                    tag = "Activity: " + d3.select(this).data()[0].activity + "<br/>" + 
                          "Starts: " + d3.select(this).data()[0].startTimeActivity + "<br/>" + 
                          "Ends: " + d3.select(this).data()[0].endTimeActivity;
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


function makeGrid(theSidePad, theTopPad, w, h){
var xAxis = d3.axisBottom(timeScale)
    .ticks(8)
    .tickSize(-h+theTopPad+20, 0, 0)
    .tickFormat(d3.timeFormat('%d%b %H:%M')); // S: change this to shift between differnt time format format for x axis

var grid = svg.append('g')
    .attr('class', 'grid')
    .attr('transform', 'translate(' +theSidePad + ', ' + (h - 50) + ')')
    .call(xAxis)
    .selectAll("text")  
            .style("text-anchor", "middle")
            .attr("fill", "#000")
            .attr("stroke", "none")
            .attr("font-size", 10)
            .attr("dy", "1em");
}

function vertLabels(theGap, theTopPad, theSidePad, theBarHeight, theColorScale){
  var numOccurances = new Array();
  var prevGap = 0;

  for (var i = 0; i < categories.length; i++){
    numOccurances[i] = [categories[i], getCount(categories[i], catsUnfiltered)];
  }

  var axisText = svg.append("g") //without doing this, impossible to put grid lines behind text
   .selectAll("text")
   .data(numOccurances)
   .enter()
   .append("text")
   .text(function(d){
    return d[0];
   })
   .attr("x", 10)
   .attr("y", function(d, i){
    if (i > 0){
        for (var j = 0; j < i; j++){
          prevGap += numOccurances[i-1][1];
         // console.log(prevGap);
          return d[1]*theGap/2 + prevGap*theGap + theTopPad;
        }
    } else{
    return d[1]*theGap/2 + theTopPad;
    }
   })
   .attr("font-size", 11)
   .attr("text-anchor", "start")
   .attr("text-height", 14)
   .attr("fill", function(d){
    for (var i = 0; i < categories.length; i++){
        if (d[0] == categories[i]){
        //  console.log("true!");
          return d3.rgb(theColorScale(i)).darker();
        }
    }
   });

}

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
