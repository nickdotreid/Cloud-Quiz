$(document).ready(function(){
	$(".graph").bind("get",function(event){
		graph = $(this);
		graph.trigger("clear");
		clone = graph.clone().addClass("clone").appendTo(graph).css("left",(0-graph.width()+"px"));
		graph.addClass("loading").addClass("jqcloud");
		$.ajax({
			type:"POST",
			dataType:"json",
			url:"/words",
			data:{
				question:graph.data("question"),
				width:graph.width(),
				height:graph.height()
			},
			success:function(data){
				$(".graph.clone").jQCloud(data['words'],{callback:function(){
					// if any words above or below height, adjust display
					
					// add words from graph.clone to graph
					$(".graph.clone span").each(function(){
						$(this).clone().appendTo($(".graph:not[.clone]"));
						// set words in graph so offscreen, then animate to correct position
					});
					$(".graph.clone").remove();
				}});
			}});
	}).bind("clear",function(event){
		$(this).removeClass("loading").removeClass("jqcloud").html("");
	});
});