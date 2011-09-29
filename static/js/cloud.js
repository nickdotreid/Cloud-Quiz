$(document).ready(function(){
	$(".graph:not[.jqcloud]").bind("get",function(event){
		graph = $(this);
		graph.trigger("clear");
		clone = graph.clone().html("").removeClass("graph").addClass("cloud").appendTo(graph).css("left",(0-graph.width()+"px"));
		graph.addClass("loading");
		$.ajax({
			type:"POST",
			dataType:"json",
			url:"/words",
			data:{
				'question':graph.data("question")
			},success:function(data){
				$(".graph .cloud:last").jQCloud(data['words'],{callback:function(){
					// if any words above move them lower
					$(".graph .cloud span").each(function(){
						top_offset = $(this).position().top;
						if(top_offset < 0){
							top_offset = top_offset*-1;
							$("span",$(this).parent()).each(function(){ $(this).css('top',(top_offset+$(this).position().top)+"px");});
						}
					});
					$(".graph .cloud").animate({'left':'0px'},{'duration':700});
					$(".graph").removeClass("loading");
				}});
			}});
	}).bind("clear",function(event){
		$(".cloud.jqcloud").remove();
		$(this).removeClass("loading");
	});
});