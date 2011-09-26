$(document).ready(function(){
	
	$("#content").delegate(".graph","init",function(event){
		graph = $(this)
		
		format = d3.format(",d"),
		fill = d3.scale.category20c();
		
		_w = graph.parent().width();
		_h = graph.css("height")
//		if(_h=='auto'){
			_h = _w
//		}
		var bubble = d3.layout.pack()
		.sort(null)
		.size([_w, _h]);

		var vis = d3.select(this).append("svg:svg")
		.attr("width", _w)
		.attr("height", _h)
		.attr("class", "bubble");

		graph.data("vis",vis);
		graph.data("bubble",bubble);
		graph.data("format",format);
		graph.data("fill",fill);
	}).delegate(".graph","clear",function(event){
		$("svg g",$(this)).remove();
	}).delegate(".graph","get",function(event){
		graph = $(this)
		d3.json("/words", function(json) {
			graph.trigger({type:"update",words:json['words']});
		});
	}).delegate(".graph","update",function(event){
		graph = $(this)
		words = event.words
		$("svg g",graph).each(function(){
			node = $(this);
			word = node.data('word');
			if(word in words){
				node.data('value',words[word])
			}
		})
		
		data = parse_words(words);
		
		bubbles = graph.data("vis").selectAll("g.node").data(graph.data("bubble").nodes(data)
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
		return d.word + ": " + graph.data("format")(d.value); });
		
		node.append("svg:circle").attr("r", 0).style("fill", '#FF00CC');
		
		node.append("svg:text")
		.attr("text-anchor", "middle")
		.attr("dy", ".3em")
		.text(function(d) { return d.word.substring(0, d.r / 3); });
		
		graph.trigger("animate")
	}).delegate(".graph","animate",function(event){
		AllNodes = d3.select(this).selectAll('svg g');
		AllNodes.transition().duration(400).attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")" });
		AllNodes.select('circle').transition().duration(800).attr('r',function(d){	return d.r;	})
		AllNodes.select('text').transition().duration(800).style('font-size', function(d){
		                if (d.word.length < 3)
		                    return d.r + 'px'
		                return (d.r * (2 + 0.7) / d.word.length) + 'px'
		            });	// change text size
	});
	
	$("#content .graph").trigger("init").trigger("get");
	
});


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