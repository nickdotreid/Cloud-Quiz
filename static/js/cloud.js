$(document).ready(function(){
	$(".graph").data("original_height",$(".graph").height()).bind("get",function(event){
		graph = $(this);
		graph.trigger("clear");
		clone = graph.clone().addClass("clone").appendTo(graph).css("left",(0-graph.width()+"px"));
		graph.addClass("loading").addClass("jqcloud");
		$.ajax({
			type:"POST",
			dataType:"json",
			url:"/words",
			data:{
				'question':graph.data("question")
			},success:function(data){
				$(".graph.clone").jQCloud(data['words'],{callback:function(){
					// if any words above move them lower
					$(".graph.clone span").each(function(){
						top_offset = $(this).position().top;
						if(top_offset < 0){
							top_offset = top_offset*-1;
							$(".graph.clone span").each(function(){ $(this).css('top',(top_offset+$(this).position().top)+"px")});
						}
					});
					// adjust bottom lower so words are not cut off
					max_bottom = 0;
					spans = $(".graph.clone span")
					for(var i=0;i<spans.length;i++){
						bottom = $(spans[i]).height()+$(spans[i]).position().top;
						if(bottom > max_bottom){
							max_bottom = bottom;
						}
					}
					$(".graph:not[.clone]").height(max_bottom);
					// add words from graph.clone to graph
					$(".graph.clone span").each(function(){
						$(this).clone().appendTo($(".graph:not[.clone]"));
						// set words in graph so offscreen, then animate to correct position
					});
					$(".graph.clone").remove();
				}});
			}});
	}).bind("clear",function(event){
		$(this).height($(this).data("original_height"));
		$(this).removeClass("loading").removeClass("jqcloud").html("");
	});
});