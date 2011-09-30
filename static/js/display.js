$(document).ready(function(){
	if($("#content .explination").length>0){
		$("#content .explination").each(function(){
			$(this).hide();
			$("#head .list").append('<li class="hidden"><a href="#'+this.id+'">'+this.id+'</a></li>');
		});
	}
	
	$(window).resize(function(){
		content_height = $(window).height() - make_css_int($(".wrapper").css("padding-top"))-make_css_int($(".wrapper").css("padding-bottom"))-make_css_int($("#head").css("margin-top"))-make_css_int($("#head").css("margin-bottom"))-$("#head").height()-$("#foot").height()-make_css_int($("#foot").css("padding-bottom"))-make_css_int($("#foot").css("padding-top"));
		$("#content").height(content_height);
		$("#content .graph").width($("#content").width()).height(content_height).css({
			'position':'absolute',
			'left':'0px',
			'top':'0px'
		});
	}).resize();
	
	$("#content").bind("next",function(){
		if($("#head .list li.selected")[0]==$("#head .list li:last")[0]){
			$("#head .list li:first a").click();
			return true;
		}
		$("a",$("#head .list li.selected").next()).click();
	});
	
});
setInterval('$("#content").trigger("next")',5000);


function make_css_int(str){
	if(!str){
		return 0;
	}
	return parseInt(str.replace('px',''));
}