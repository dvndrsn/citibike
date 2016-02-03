var width = 400,
    height = 500;

var rc = [-74.0031909, 40.7206499];
var homea = [-73.9970746, 40.6999351];
var homed = [-74.0496805, 40.71692];

var projection = d3.geo.mercator()
        .center([-73.94, 40.70])
        .scale(180000)
        .translate([width * 3 / 4, height * 3 / 4]);

var path = d3.geo.path()
        .projection(projection);

var svg = d3.select(".map").append("svg")
        .attr("width", width)
        .attr("height", height);

// Groups for layout of SVG Elements
var g = svg.append("g");
var hood = g.append("g").attr("class", "hood");
var mesh = g.append("g").attr("class", "mesh");
var poi = g.append("g").attr("class", "poi");
var trips = g.append("g").attr("class", "trips");

d3.json("/static/json/encoded-topo2.json", function(error, nyc) {
    // Add neighborhoods, mesh boundaries and points of interest (stations, RC office, etc.)

    // Neighborhoods
    hood.append("path")
        .datum(topojson.feature(nyc, nyc.objects.encoded2))
        .attr("d", path)
        .attr("class", "feature");

    // Mesh boundaries
    mesh.append("path")
        .datum(topojson.mesh(nyc, nyc.objects.encoded2, function(a, b) { return a !== b; }))
        .attr("class", "mesh")
        .attr("d", path);

    // Points of Interest - RC office
    poi.selectAll("circle")
        .data([rc]).enter()
        .append("circle")
        .attr("cx", function (d) { return projection(d)[0];})
        .attr("cy", function (d) { return projection(d)[1]; })
        .attr("r", "5px")
        .attr("fill", "green");

    // Points of Interest - Stations
    d3.json("/static/json/stations.json", function(error, stations) {
        poi.selectAll("circle")
            .data(stations).enter()
            .append("circle")
            .attr("cx", function(d) { p = projection([d['long'], d['lat']]); return p[0]; })
            .attr("cy", function(d) { p = projection([d['long'], d['lat']]); return p[1]; })
            .attr("r", "2px")
            .attr("fill","pink");
    });

    d3.json("/static/json/bike.json", function(error, bike) {
        var pathLine = d3.svg.line()
                .x(function(d) { p = projection(d); return p[0]; })
                .y(function(d) { p = projection(d); return p[1]; });

        // Draw the paths for each bike trip as invisible
        var paths = trips.selectAll("line")
                .data(bike).enter()
                .append("path")
                .attr("d",  function(d) {return pathLine([[d.start_long, d.start_lat], [d.end_long, d.end_lat]]);})
                .attr("class", "path")
                .style("opacity",0);

        // Magic number for length of transition per element - 200 ms.
        var magic = 200;

        // Render lines for each trip using stroke-dashoffset trick
        paths
            .each(function(d) { d.totalLength = this.getTotalLength(); })
            .attr("stroke-dasharray", function(d) { return d.totalLength + " " + d.totalLength})
            .attr("stroke-dashoffset", function(d) { return d.totalLength; })
            .transition()
        // TODO - Set duration proportional to length of distance traveled (constant speed for line drawing)
        /* .duration(function(d){ d.duration = d.totalLength * 50; return d.duration; }) */
            .duration(magic)
            .delay(function(d, i) { return i  * magic;  })
            .style("opacity", 1)
            .ease("linear")
            .attr("stroke-dashoffset", 0)
            .transition()
            .duration(magic)
            .style("opacity", .5)
            .style("stroke", "grey");

        var stats = d3.select(".stats")
            .append("svg")
            .style("background", "#ccf9fb")
            .attr({ width: width, height: height});

        stats
            .selectAll("starttext")
            .data(bike)
            .enter() 
            .append("text")
            .attr({
                x: 0,
                y: 0,
                dx: 5,
                dy: 20,
                "font-size": 18
            })
            .style("opacity", 1)
            .style("fill","#004447" )
            .transition()
            .duration(magic)
            .delay(function(d, i) { return i  * magic;  })
            .text(function(d) { return "Start station: " + d.start_name })
            .transition()
            .duration(0)
            .style("opacity", 0);

        stats
            .selectAll("endtext")
            .data(bike)
            .enter() 
            .append("text")
            .attr({
                x: 0,
                y: 0,
                dx: 5,
                dy: 50,
                "font-size": 18
            })
            .style("opacity", 1)
            .style("fill","#004447" )
            .transition()
            .duration(magic)
            .delay(function(d, i) { return i  * magic;  })
            .text(function(d) { return "End station: " + d.end_name })
            .transition()
            .duration(0)
            .style("opacity", 0);



        // Add text for each station as it is visited
        // var startstationText = stats
        //         .selectAll("text")
        //         .data(bike)
        //         .append("text")
        //         .attr({
        //             x: 0,
        //             y: 0,
        //             dx: 5,
        //             dy: 5,
        //             "font-size": 18
        //         })
        //         .style("opacity", 1)
        //         .style("fill","#004447" )
        //         .transition()
        //         .duration(magic)
        //         .delay(function(d, i) { return i  * magic;  })
        //         .text(function(d) { return "Start station:" + d.start_name })
        //         .transition()
        //         .duration(0)
        //         .style("opacity", 0);

        // var endstationText = stats
        //         .selectAll("text")
        //         .data(bike)
        //         .append("text")
        //         .attr({
        //             x: 0,
        //             y: 0,
        //             dx: 25,
        //             dy: 50,
        //             "font-size": 18
        //         })
        //         .style("opacity", 1)
        //         .style("fill","#004447" )
        //         .transition()
        //         .duration(magic)
        //         .delay(function(d, i) { return i  * magic;  })
        //         .text(function(d) {return "End station: "+ d.end_name })
        //         .transition()
        //         .duration(0)
        // //.style("text-anchor", "middle")
        //         .style("opacity", 0);
    });

});
