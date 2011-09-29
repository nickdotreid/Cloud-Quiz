$(document).ready(function(){
	$(".graph").bind("get",function(event){
		graph = $(this);
		if($(".cloud",graph).length > 0){
			graph.trigger("clear");
			return false;
		}
		graph.trigger("load");
	}).bind("load",function(){
		graph = $(this);
		if($(".cloud",graph).length > 0){
			return false;
		}
		clone = graph.clone().html("").height(graph.height()).removeClass("graph").addClass("cloud").appendTo(graph).css("left",(0-graph.width()+"px"));
		graph.addClass("loading");
		$.ajax({
			type:"POST",
			dataType:"json",
			url:"/words",
			data:{
				'question':graph.data("question")
			},success:function(data){
				$(".graph .cloud").jQCloud(data['words'],{callback:function(){
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
		$(".cloud.jqcloud",$(this)).addClass("old").animate(
			{'left':$(this).width()+"px"},
			{'animate':300,
			'complete':function(){
				setTimeout('$(".graph").trigger("load")');
				$(this).remove();
			}});
		$(this).removeClass("loading");
	});
});