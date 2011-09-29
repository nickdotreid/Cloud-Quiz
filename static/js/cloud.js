$(document).ready(function(){
	$(".graph").bind("get",function(event){
		graph = $(this);
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
				$(".graph").jQCloud(data['words'],{callback:function(){
					// something to animage here?
				}});
			}});
	});

	
});