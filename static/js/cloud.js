$(document).ready(function(){
	setInterval('$(".graph").trigger("get")',30000)
	
	$(".graph").bind("get",function(event){
		graph = $(this);
		$.ajax({
			type:"POST",
			dataType:"json",
			url:"/tagmap",
			data:{
				question:graph.data("question"),
				width:graph.width(),
				height:graph.height(),
			},
			success:function(data){
				$(".graph").trigger({type:"update",words:data['words']});
			}});
	}).bind("update",function(event){
		graph = $(this);
		words = event.words;
		$(".tag",graph).addClass("old");
		for(index in words){
			word = words[index]
			properties = {
				'top':word['top']+'px',
				'left':word['left']+'px',
				'width':word['width']+'px',
				'height':word['height']+'px',
				'font-size':word['size']+'px',
			}
			if($(".tag:[data-tag="+word['tag']+"]").length>0){
				word = $(".tag:[data-tag='"+word['tag']+"']");
				word.removeClass("old").animate(properties,{duration:'500'});
			}else{
				graph.append('<a class="tag" data-tag="'+word['tag']+'" href="#">'+word['tag']+'</a>');
				$("a:last",graph).css(properties)
			}
			$(".tag.old").animate({'opacity':0},{
				'duration':500,
				'complete':function(){
					$(this).remove();
				}
			})
		}
	});

	
});