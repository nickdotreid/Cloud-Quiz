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
						clone = $(this)
						graph = $(this).clone();
						graph.appendTo($(".graph:not[.clone]"))
						graph.css({
							'left':'0px',
							'opacity':0
						}).animate({
							'left':clone.css("left"),
							'opacity':1
						},{
							'duration':700
						})
					});
					$(".graph.clone").remove();
					$(".graph").removeClass("loading");
				}});
			}});
	}).bind("clear",function(event){
		$(this).height($(this).data("original_height"));
		$(this).removeClass("loading").removeClass("jqcloud");
		$("span").remove();
	});
});