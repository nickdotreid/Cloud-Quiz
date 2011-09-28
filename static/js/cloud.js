$(document).ready(function(){
	setInterval('$(".graph").trigger("get")',60000)
	
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
				if(data['img']){
					$(".graph").trigger({type:'blit',img:data['img']});
				}else{
					$(".graph").trigger({type:"update",words:data['words']});
				}
			}});
	}).bind("blit",function(event){
		graph = $(this);
		graph.html("");
		graph.append("<img src='"+event['img']+"' />");
	}).bind("update",function(event){
		graph = $(this);
		words = event.words;
		$(".tag",graph).addClass("old");
		existing = $(".tag.old",graph);
		for(index in words){
			word = words[index]
			properties = {
				'top':word['top']+'px',
				'left':word['left']+'px',
				'width':word['width']+'px',
				'height':word['height']+'px',
				'font-size':word['size']+'px',
				'opacity':1,
			}
			found = false;
			for(var i=0;i<existing.length;i++){
				if(existing.data("tag") == word['tag'] && found){
					found = true;
					word = $(existing[i]);
					word.removeClass("old").animate(properties,{duration:'500'});
				}
			}
			if(!found){
				graph.append('<a class="tag" data-tag="'+word['tag']+'" href="#">'+word['tag']+'</a>');
				$("a:last",graph).css(properties).fadeIn(500);
			}
		}
		$(".tag.old",graph).animate({'opacity':0,'left':graph.width()},{
			'duration':500,
			'complete':function(){
				$(this).remove();
			}
		})
	});

	
});