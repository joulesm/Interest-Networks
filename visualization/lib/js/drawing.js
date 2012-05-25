// define width and height of space
var width = 2500;
var height = 1700;

// list of 20 pre-defined colors
var color = ["placeholder", "#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c", "#98df8a",
"#d62728", "#ff9896", "#9467bd", "#c5b0d5", "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", 
"#7f7f7f", "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"];

// initialize view
var vis = d3.select("#canvas").append("svg:svg")
    .attr("width", width)
    .attr("height", height)
    .attr("pointer-events", "all")
    .append("svg:g")
    .call(d3.behavior.zoom().on("zoom", redraw))
    .append("svg:g");
    
// rectangle to zoom and pan in
vis.append("svg:rect")
    .attr("width", width)
    .attr("height", height)
    .attr("fill", "#FFFFFF");

// get data from json file
d3.json("temp/company_Intel/nodesandlinks.json", function(json) {
    var force = self.force = d3.layout.force()
        .nodes(json.nodes)
        .links(json.links)
        .charge(-200)
        .linkDistance(function(d) { return (700 - 1000 * Math.abs(d.value))/7 })
        .linkStrength(function(d) { return Math.min(Math.abs(d.value)*20, 4)})
        .gravity(.025)
        .size([width, height])
        .start();
 
    var link = vis.selectAll("line.link")
        .data(json.links)
        .enter().append("svg:line")
        .attr("class", "link")
        .attr("source", function(d) { return d.source; })
        .attr("target", function(d) { return d.target; })
        .style("stroke-width", function(d) {return Math.max(d.value*30, 1); })
        .style("stroke", "#666");

    var linkedByIndex = {};

    link.each(function(d){
        s = d.source.index;
        t = d.target.index;

        if (s in linkedByIndex) {
            linkedByIndex[s].push(t);
        } else {
            linkedByIndex[s] = [t];
        }
        
        if (t in linkedByIndex) {
            linkedByIndex[t].push(s);
        } else {
            linkedByIndex[t] = [s];
        }
    });

    function handleNeighbors(currNode, on) {
        var currIndex = currNode.attr("index");
        var neighborIndexes;
        if ( currIndex in linkedByIndex ) {
            neighborIndexes = linkedByIndex[currIndex];
        }
        else {
            return;
        }

        for(var j = 0; j < neighborIndexes.length; j++) {
            var neighbor = vis.selectAll("g.node").filter(function(d, i) {
                return i == neighborIndexes[j]
            });

            if( on ) {
                neighbor.select("text").attr("visibility", "visible");
                neighbor.select("text").attr("opacity", 0.3);
                neighbor.select("circle").style("stroke-width",1);
            } else {
                if (neighbor.attr("clicked") == "false") {
                    neighbor.select("text").attr("visibility", "hidden");
                    neighbor.select("text").attr("opacity", 1.0);
                    neighbor.select("circle").style("stroke-width",0);
                } else {
                    neighbor.select("text").attr("visibility", "visible");
                    neighbor.select("text").attr("opacity", 1.0);
                    neighbor.select("circle").style("stroke-width",2);
                }
            }
        }
    }

    // create node object, a container for a circle and text
    var node = vis.selectAll("g.node")
        .data(json.nodes)
        .enter().append("svg:g")
        .attr("class", "node")
        .attr("clicked", "false")
        .attr("name", function(d) { return d.name; })
        .attr("index", function(d,i) { return i; })
        .on("mouseover", function(d) {
            onMouseOverNode(d3.select(this));
            handleNeighbors(d3.select(this), true);
        })
        .on("mouseout", function(d) {
            onMouseOutNode(d3.select(this));
            handleNeighbors(d3.select(this), false);
        })
        .on("click", function(d) {
            onClickNode(d3.select(this));
        })
        .call(force.drag);

    // add circle
    node.append("svg:circle")
        .attr("class", "circle")
        .attr("r", function(d) { return d.size; })
        .attr("name", function(d) { return d.name; })
        .style("stroke", "white")
        .style("stroke-width", 0)
        .style("opacity", 0.7)
        .style("fill", function(d) { return color[d.group]; });

    // add text
    node.append("svg:text")
        .style("pointer-events", "none")
        .style("font", "Arial")
        .style("fill", "black")
        .attr("visibility", "hidden")
        .attr("class", "nodetext")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .attr("font-size", 20)
        .text(function(d, i) { return d.name; });

    // add title (mouse over text)
    node.append("svg:title") 
        .text(function(d) { return d.name; }); 
 
    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
 
        node.attr("transform", function(d) { 
            return "translate(" + d.x + "," + d.y + ")"; });
    });
});
    
// fade in
vis.style("opacity", 1e-6) 
    .transition() 
    .duration(1000) 
    .style("opacity", 1); 

// called when you mouse over a node.
function onMouseOverNode(currNode) {
    if( currNode.attr("clicked") == "false" ) {
        currNode.select("text").attr("visibility", "visible");
        currNode.select("circle").style("opacity", 1);
        currNode.select("circle").style("stroke-width", 3);
    };
}

// called when you mouse out of a node.
function onMouseOutNode(currNode) {
    if( currNode.attr("clicked") == "false" ) {
        currNode.select("text").attr("visibility","hidden");
        currNode.select("circle").style("opacity", 0.7);
        currNode.select("circle").style("stroke-width", 0);
    }
}

// called when you click on a node.
function onClickNode(currNode) {
    var isClicked = "";
    if( currNode.attr("clicked") == "false" ) {
        isClicked = "true";
    }
    else {
        isClicked = "false";
    }

    if( isClicked == "true" ) {
        currNode.select("text").attr("visibility", "visible");
        currNode.select("circle").style("opacity", 1);
        currNode.select("circle").style("stroke-width", 3);
    }
    else {
        currNode.select("text").attr("visibility","hidden");
        currNode.select("circle").style("opacity", 0.7);
        currNode.select("circle").style("stroke-width", 0);
    }

    currNode.attr("clicked", isClicked);
}

// redraw called when you pan or zoom
function redraw() {
    vis.attr("transform",
        "translate(" + d3.event.translate + ")" 
        + " scale(" + d3.event.scale + ")");
}

// find neighboring nodes function.... doesn't work as of now
/*
    function neighboringNodes(n) {
        var neighNodes = [];
        var circle = n.select("circle");

        vis.selectAll('line[target="' + circle.attr("id") + '"]').each(function() {
            neighNodes.push(vis.select('circle[id="' + d3.select(this).attr("source")+'"]'));
            alert(vis.select('circle[id="' + d3.select(this).attr("source")+'"]'));
        });

        vis.selectAll('line[source="' + circle.attr("id") + '"]').each(function() {
            neighNodes.push(vis.select('circle[id="' + d3.select(this).attr("target")+'"]'));
        });

        return neighNodes;
    }

*/