$(document).ready(function(){
	$(".question:even").addClass("odd");
	$(".question").append("<br class='cb' />")
	
	$("form").append('<input type="hidden" value="true" name="ajax" />').submit(function(event){
		event.preventDefault();
		form = $(this);
		if(!form.validate({rules:{text: {required: true,maxlength: 500}}}).form()){
			return false;
		}
		$.ajax({
			url:form.attr("action"),
			type:form.attr("method"),
			data:form.serialize(),
			success:function(data){
				form.trigger("show_thankyou");
				form.parent(".question:first").after(data);
				form.parent(".question:first").remove();
			}
		});
	})
	$("form input,form textarea").each(function(){
		input = $(this);
		if($("label[for="+input.attr('id')+"].limit").length>0){
			input.data("limit",Number($("label[for="+input.attr('id')+"].limit .number:first").text()))
			
			input.keyup(function(){
				input = $(this)
				characters_left = input.data("limit") - input.val().length
				$("label[for="+input.attr('id')+"].limit").html('<span class="number">'+characters_left+'</span> characters left');
				if(characters_left<1){
					$("label[for="+input.attr('id')+"].limit .number").addClass("error");
				}
			}).keyup()
			
		}
	})
	
	$("#head .list a").click(function(){
		$(".graph").trigger("clear");
		$(".questions li").removeClass("selected");
		$(".questions .question").hide();
		$(this).parent().addClass('selected').trigger("get");
	});
	$("#head .list li").bind("get",function(event){
		$(".graph").data("question",$(this).data("question")).trigger("get");
	}).delegate("a","click",function(event){
		event.preventDefault();
		$($(this).attr("href")).show();
	})
	$(".questions .question").hide();
	setTimeout('$("#head .questions a:first").click()',200);

})