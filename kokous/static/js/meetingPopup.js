// 0 -> disabled, 1 -> enabled
var popupStatus = 0;
// loading popup
function loadPopup(){
	// loads popup only if it is disabled
	if(popupStatus==0){
		$("#backgroundPopup").css({
			"opacity": "0.7"
		});
		$("#backgroundPopup").fadeIn("slow");
		$("#popupMeetingInfo").fadeIn("slow");
		popupStatus = 1;
	}
}

// disabling popup
function disablePopup(){
	// disables popup only if it is enabled
	if(popupStatus==1){
		$("#backgroundPopup").fadeOut("slow");
		$("#popupMeetingInfo").fadeOut("slow");
		popupStatus = 0;
	}
}

// centering popup
function centerPopup(){
	// request data for centering
	var windowWidth = document.documentElement.clientWidth;
	var windowHeight = document.documentElement.clientHeight;
	
	var popupHeight = $("#popupMeetingInfo").height();
	var popupWidth = $("#popupMeetingInfo").width();
	// centering
	$("#popupMeetingInfo").css({
		"position": "absolute",
		// "position": "fixed",
		"top": windowHeight/2-popupHeight/2,
		"left": windowWidth/2-popupWidth/2,
		"height" : "auto",
		"background" : "#EDEDED"
	});
}

$(document).ready(function(){	

	// $("#button").click(function(){
	// 	// centering with css
	// 	centerPopup();
	// 	// load popup
	// 	loadPopup();
	// });
	
	$(".viewMeeting").click(function(){
		var s = $(this).attr("meetingID");
		// making url with meeting id
		var url = "/meeting/" + s + " #tableSection";
		// loading the html
		$("#page").load(url);
		centerPopup();loadPopup();
		return false;
	});
				
	// closing popup
	// //Click the x event!
	// $("#popupMeetingInfoClose").click(function(){
	// 	disablePopup();
	// });
	//Click out event!
	$("#backgroundPopup").click(function(){
		disablePopup();
	});
	popupMeetingInfo

});