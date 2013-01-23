$(document).ready(function(){
	var toggled = false;
	$("#toggle").click(function(){
		if(toggled == false){
			toggled = true;
			$(".panel").slideDown("slow");
		}
		else{
			toggled = false;
			$(".panel").slideUp("slow");
		}	
	});
});