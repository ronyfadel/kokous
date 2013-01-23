var users;
var participantsAdded = new Array();

$(document).ready(function(){
	
	// Setting up the time pickers
	$("#inputStart").ptTimeSelect();
	$("#inputEnd").ptTimeSelect();
	
	// Setting up the date pickers
	$( "#datepicker" ).datepicker( "option", "dateFormat", "yy-mm-dd" );
	$( "#datepicker" ).datepicker();
	var participantsAdded = [ ];	
	
	$("#inputParticipant").keyup(function() {
		var input = $(this).val();
		var url ="/api/user.json?query="+input;
		$.getJSON(url, function(data) { users=data; });
		
		if($("#inputParticipant").val()==0)
			 $("#users").html(" ");
		else
		{
			var list = '';
			for (var i in users)
			{
				var user = users[i];
				list+="<div data=" + JSON.stringify(name) + "><b>" + user.username + '</b> (' + user.first_name + ' ' + user.last_name + ') ' + " <a href='#' class='action' username="+ user.username +">Add</a></div>"; 
				$("#users").html(list);
			}
		}
	});

	$("#users .action").live("click", function()
	{
		var cpt = 0;
			var s = $(this).attr("username");
			participantsAdded.push(s);
				if(participantsAdded.length>1)
				{
					for(i=0;i<participantsAdded.length;i++ )
					{
							for(j=i+1;j<participantsAdded.length; j++)
								if(participantsAdded[i]==participantsAdded[j])
								{
									alert("user already invited");
									cpt++;
									participantsAdded.pop();
								}
					}
				}
				$("#invitedparticipants").val(participantsAdded);
				if(cpt==0){
				$(this).html("x") ;
				$("#members").prepend($(this).parent('div'));
			}
	});

	$("#members .action").live("click", function() {
		var s = $(this).attr("username");
		var index;
		for(i=0;i<participantsAdded.length;i++)
		{
			if(participantsAdded[i]==s)
			{
				index=i;
			}
		}
		participantsAdded.splice(index,1);
		$("#invitedparticipants").val(participantsAdded);
	    $(this).html("Add") ;
	    $("#users").prepend($(this).parent('div'));
	});
	
	// Setup the map
	initializeMap();

});
