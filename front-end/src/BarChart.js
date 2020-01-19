/* eslint-disable default-case */
import React, {Component} from 'react';
import * as d3 from "d3";

class BarChart extends Component {
  componentDidMount() {
    this.drawChart();
  }

  drawChart() {
    
    var margin = {top: 20, right: 160, bottom: 35, left: 30};

    var width = 1100 - margin.left - margin.right,
        height = 700 - margin.top - margin.bottom;

    var svg = d3.select("body")
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    /* Data in strings like it would be if imported from a csv */

    

    // var data = [
    //   { year: "2006", happy: "10", sad: "15", angry: "9", excited: "6", relaxed: "17", neutral: "7" },
    //   { year: "2007", happy: "12", sad: "18", angry: "9", excited: "4", relaxed: "17", neutral: "7" },
    //   { year: "2008", happy: "5", sad: "20", angry: "8", excited: "2", relaxed: "17", neutral: "7" },
    //   { year: "2009", happy: "1", sad: "15", angry: "5", excited: "4", relaxed: "17", neutral: "7" },
    //   { year: "2010", happy: "2", sad: "10", angry: "4", excited: "2", relaxed: "17", neutral: "7" },
    //   { year: "2011", happy: "3", sad: "12", angry: "6", excited: "3", relaxed: "17", neutral: "7" },
    //   { year: "2012", happy: "4", sad: "15", angry: "8", excited: "1", relaxed: "17", neutral: "7" },
    //   { year: "2013", happy: "6", sad: "11", angry: "9", excited: "4", relaxed: "17", neutral: "7" },
    //   { year: "2014", happy: "10", sad: "13", angry: "9", excited: "5", relaxed: "17", neutral: "7" },
    //   { year: "2015", happy: "16", sad: "19", angry: "6", excited: "9", relaxed: "17", neutral: "7" },
    //   { year: "2016", happy: "19", sad: "17", angry: "5", excited: "7", relaxed: "17", neutral: "7" },
    // ];


    // Transpose the data into layers
    // var dataset = d3.stack()(["happy", "sad", "angry", "excited", "relaxed", "neutral"].map(function(mood) {
    //   return data.map(function(d) {
    //     return {x: d.year, y: +d[mood]};
    //   });
    // }));

    var data = [
      { year: new Date(2006, 1, 1), happy: 10, sad: 15, angry: 9, excited: 6, relaxed: 17, neutral: 7 },
      { year: new Date(2007, 1, 1), happy: 12, sad: 18, angry: 9, excited: 4, relaxed: 17, neutral: 7 },
      { year: new Date(2008, 1, 1), happy: 5, sad: 20, angry: 8, excited: 2, relaxed: 17, neutral: 7 },
      { year: new Date(2009, 1, 1), happy: 1, sad: 15, angry: 5, excited: 4, relaxed: 17, neutral: 7 },
      { year: new Date(2010, 1, 1), happy: 2, sad: 10, angry: 4, excited: 2, relaxed: 17, neutral: 7 },
      { year: new Date(2011, 1, 1), happy: 3, sad: 12, angry: 6, excited: 3, relaxed: 17, neutral: 7 },
      { year: new Date(2012, 1, 1), happy: 4, sad: 15, angry: 8, excited: 1, relaxed: 17, neutral: 7 },
      { year: new Date(2013, 1, 1), happy: 6, sad: 11, angry: 9, excited: 4, relaxed: 17, neutral: 7 },
      { year: new Date(2014, 1, 1), happy: 10, sad: 13, angry: 9, excited: 5, relaxed: 17, neutral: 7 },
      { year: new Date(2015, 1, 1), happy: 16, sad: 19, angry: 6, excited: 9, relaxed: 17, neutral: 7 },
      { year: new Date(2016, 1, 1), happy: 19, sad: 17, angry: 5, excited: 7, relaxed: 17, neutral: 7 },
    ];

    // var data = [
    //   {month: new Date(2015, 0, 1), apples: 3840, bananas: 1920, cherries: 960, dates: 400},
    //   {month: new Date(2015, 1, 1), apples: 1600, bananas: 1440, cherries: 960, dates: 400},
    //   {month: new Date(2015, 2, 1), apples:  640, bananas:  960, cherries: 640, dates: 400},
    //   {month: new Date(2015, 3, 1), apples:  320, bananas:  480, cherries: 640, dates: 400}
    // ];

    // var stack = d3.stack()
    //   .keys(["apples", "bananas", "cherries", "dates"])
    //   .order(d3.stackOrderNone)
    //   .offset(d3.stackOffsetNone);

    // var dataset = stack(data);
    
    var stack = d3.stack()
      .keys(["happy", "sad", "angry", "excited", "relaxed", "neutral"])
      .order(d3.stackOrderNone)
      .offset(d3.stackOffsetNone);
    
    var dataset = stack(data);

    var formatYear = d3.timeFormat("%Y");

    console.log(dataset);
    console.log(dataset[0].map((d) => formatYear(d.data.year)));
    
    // Set x, y and colors
    var x = d3.scaleBand()
      .domain(dataset[0].map((d) => formatYear(d.data.year)))
      .rangeRound([10, width-10])
      .padding(0.02);

    var y = d3.scaleLinear()
      .domain([0, 100])
      .range([height, 0]);

    var colors = ["#98abc5", "#8a89a6", "#7b6888", "#6b486b", "#a05d56", "#d0743c"]; //todo: ADD MORE

    // Define and draw axes
    var yAxis = d3.axisLeft(y)
      .ticks(5)
      .tickSize(-width, 0, 0);

    var xAxis = d3.axisBottom(x);
      // .tickArguments([dataset[0].map((d) => d.data.year), d3.timeFormat("%Y")]);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis);

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

    // Create groups for each series, rects for each segment 
    var groups = svg.selectAll("g.numSongs")
      .data(dataset)
      .enter().append("g")
      .attr("class", "numSongs")
      .style("fill", function(d, i) { return colors[i]; });

    var rect = groups.selectAll("rect")
      .data(dataset)
      .enter()
      .append("rect")
      .attr("x", function(d, i) { console.log(d[i].data.year); return x(formatYear(d[i].data.year));})
      .attr("y", function(d, i) { console.log(y(d[i][0])); return y(d[i][0]); })
      .attr("height", function(d, i) { return y(d[i][0]) - y(d[i][1]); })
      .attr("width", x.bandwidth())
      .on("mouseover", function() { tooltip.style("display", null); })
      .on("mouseout", function() { tooltip.style("display", "none"); })
      .on("mousemove", function(d) {
        var xPosition = d3.mouse(this)[0] - 15;
        var yPosition = d3.mouse(this)[1] - 25;
        tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
        tooltip.select("text").text(d.y);
      });

    // Draw legend
    var legend = svg.selectAll(".legend")
      .data(colors)
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });
    
    legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", function(d, i) {return colors.slice().reverse()[i];});
    
    legend.append("text")
      .attr("x", width + 5)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "start")
      .text(function(d, i) { 
        switch (i) {
          case 0: return "Happy";
          case 1: return "Relaxed";
          case 2: return "Neutral";
          case 3: return "Sad";
          case 4: return "Excited";
          case 5: return "Angry";
        }
      });

    // Prep the tooltip bits, initial display is hidden
    var tooltip = svg.append("g")
      .attr("class", "tooltip")
      .style("display", "none");
        
    tooltip.append("rect")
      .attr("width", 30)
      .attr("height", 20)
      .attr("fill", "white")
      .style("opacity", 0.5);

    tooltip.append("text")
      .attr("x", 15)
      .attr("dy", "1.2em")
      .style("text-anchor", "middle")
      .attr("font-size", "12px")
      .attr("font-weight", "bold");

  }

  render(){
    return <div id={"#" + this.props.id}></div>
  }
};

export default BarChart;