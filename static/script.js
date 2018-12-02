/**
  * Create bootstrap slider, from slider package
  *
  */

$('#ex1').slider({
	formatter: function(value) {
		return 'Current value: ' + value;
	}
});


/**
  * Graph Creation
  *
  */

graph={};
years=[1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]
graph.nodes=[]
for(x in years){
    graph.nodes.push({
        "label": years[x],
        "id": Number(x)+1
    })
  }
cosineSimilarity= JSON.parse(document.getElementById("cosineMatrix").innerHTML);
onChange(); // Call onChange on page Load
 /**
  * When there is a change in the value,cal this function.
  *
  **/
  function onChange(){
    cosineSimilarity= JSON.parse(document.getElementById("cosineMatrix").innerHTML);
    console.log($("#ex1").val())
    if($("#ex1").val()==null){
        range=0;
    }
    else{
    range=Number($("#ex1").val())/100
    }
    graph.links=createGraphLinks(cosineSimilarity,range)
    //console.log(graph.links)
    generateGraph(graph);
  }
   /**
    * create Graph Links when threshold is changed
    *
    **/
  function createGraphLinks(cosineSimilarity,threshold){
    links=[]
    for(x in cosineSimilarity){
            currRow=cosineSimilarity[x]
            y=x;
            for(y in currRow){
                if((currRow[y]>threshold)&(x!=y)){
                    links.push({
                        "source": Number(x)+1,
                        "target": Number(y)+1,
                        "link": (currRow[y]-threshold)*20
                    })
                }
            }
        }
    return links;
  }
  /**
   * Generate Graph, based on links and nodes.
   *
   */
  function generateGraph(graph){
    var colors = d3.scaleOrdinal(d3.schemeCategory10);
    d3.select("svg").html(null);
    var svg = d3.select("svg").attr("width", screen.width)
    .attr("height", screen.height)
    width=screen.width;
    height=screen.height;

    var simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(function (d) {return d.id;}).distance(300).strength(0.5))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

  update(graph.links,graph.nodes)

    function update(links, nodes) {
        link = svg.selectAll(".link")
            .data(links)
            .enter()
            .append("line")
            .attr("class", "link")

        node = svg.selectAll(".node")
            .data(nodes)
            .enter()
            .append("g")
            .attr("class", "node")
            .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    //.on("end", dragended)
            );

        node.append("circle")
            .attr("r", 50)
            .style("fill", function (d, i) {return colors(i);})

        node.append("title")
            .text(function (d) {return d.id;});

        node.append("text")
            .attr("dy", 0)
            .text(function (d) {return d.label;});

        simulation
            .nodes(nodes)
            .on("tick", ticked);

        simulation.force("link")
            .links(links);
    }

    function ticked() {

        link
            .attr("x1", function (d) {return d.source.x;})
            .attr("y1", function (d) {return d.source.y;})
            .attr("x2", function (d) {return d.target.x;})
            .attr("y2", function (d) {return d.target.y;})
            .style("stroke-width", function (d) {return d.link;})


        node
            .attr("transform", function (d) {return "translate(" + d.x + ", " + d.y + ")";});
    }

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart()
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }
//    function dragended(d) {
//        if (!d3.event.active) simulation.alphaTarget(0);
//        d.fx = undefined;
//        d.fy = undefined;
//    }
// With JQuery
}