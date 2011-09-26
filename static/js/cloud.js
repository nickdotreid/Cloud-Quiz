$(document).ready(function(){
	init_viz();
	
	poll_data();

})

function init_viz(){
	// add svg to page
	var r = 500,
	format = d3.format(",d"),
	fill = d3.scale.category20c();

	var bubble = d3.layout.pack()
	.sort(null)
	.size([r, r]);

	var vis = d3.select("#chart").append("svg:svg")
	.attr("width", r)
	.attr("height", r)
	.attr("class", "bubble");
	
	$("#chart").data("vis",vis);
	$("#chart").data("bubble",bubble);
	$("#chart").data("format",format);
	$("#chart").data("fill",fill);
}

function poll_data(){
	d3.json("/words", function(json) {
		updateViz(json['words'])
	})
}

function updateViz(words){
	chart = $("#chart")
	
	$("svg g").each(function(){
		node = $(this);
		word = node.data('word');
		if(word in words){
			node.data('value',words[word])
		}
	})
	
	data = parse_words(words);
	
	bubbles = chart.data("vis").selectAll("g.node").data(chart.data("bubble").nodes(data)
	.filter(function(d) { 
		return !d.children; 
	}))
	
	var node = bubbles.enter().append("svg:g")
	.attr("class", "node")
	.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
	.attr('data-word',function(d){return d.word;})
	.attr('data-value',function(d){return d.value;});
	
	
	node.append("svg:title")
	.text(function(d) { 
	return d.word + ": " + chart.data("format")(d.value); });

	node.append("svg:circle").attr("r", 0).style("fill", '#FF00CC');

	node.append("svg:text")
	.attr("text-anchor", "middle")
	.attr("dy", ".3em")
	.text(function(d) { return d.word.substring(0, d.r / 3); });
	
	updateNodes();
}

function updateNodes(){
	AllNodes = d3.selectAll('svg g');
	AllNodes.transition().duration(400).attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")" });
	AllNodes.select('circle').transition().duration(800).attr('r',function(d){	return d.r;	})
	AllNodes.select('text').transition().duration(800).style('font-size', function(d){
	                if (d.word.length < 3)
	                    return d.r + 'px'
	                return (d.r * (2 + 0.7) / d.word.length) + 'px'
	            });	// change text size
}



function parse_words(words){
	parsed = [];
	for(word in words){
		parsed.push({
			word: word,
			value: words[word]
		})
	}
	return {children:parsed};
}