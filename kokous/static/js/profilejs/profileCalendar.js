$(document).ready(function(){
	$('#calendar').fullCalendar({
		firstDay: 1,
		timeFormat: '(h:mm TT)',
		height: 325,
		weekMode: 'liquid',
		theme: true,
		header: {
			left: 'prev,next today',
			center: 'title',
			// right: 'month,basicWeek,basicDay'
			right: 'month,basicWeek,agendaDay'
		},
		events: function(start, end, callback) {
			var s = $("#userID").attr("userId");
		        $.ajax({
		            url: '/api/meeting.json?id='+s,
		            dataType: 'json',
		            data: {
		                // our hypothetical feed requires UNIX timestamps
		                start: Math.round(start.getTime() / 1000),
		                end: Math.round(end.getTime() / 1000)
		            },
		            success: function(data) {

						var meetings, start, end, newDateStart, newDateEnd,hourStart ,hourEnd,effDateStart,effDateEnd,ds,ms,ys,de,me,ye
						meetings=data;
		                var events = [];
	                    for (var i in meetings)
						{
							var meeting = meetings[i];
							start = meeting.fields.meeting_date;
							end = meeting.fields.meeting_date;
							newDateStart = $.fullCalendar.parseDate(start)
							newDateEnd = $.fullCalendar.parseDate(end)
							effDateStart =  $.fullCalendar.parseDate($.fullCalendar.formatDate( newDateStart, 'd-MMM-yyyy'));
							hourStart = meeting.fields.start_time;
							hoursstart=hourStart.split(":");
							ds = newDateEnd.getDate();
							ms = newDateEnd.getMonth();
							ys = newDateEnd.getFullYear();
							effDateEnd = $.fullCalendar.parseDate($.fullCalendar.formatDate( newDateEnd, 'd-MMM-yyyy'));
							de = effDateEnd.getDate();
							me = effDateEnd.getMonth();
							ye = effDateEnd.getFullYear();
							hourEnd = meeting.fields.end_time;
							hoursend=hourEnd.split(":")
							// alert(hourStart);
							events.push({title:meeting.fields.title,
										start: new Date(ys,ms,ds,parseInt(hoursstart[0]),parseInt(hoursstart[1])),
										end: new Date(ye,me,de,parseInt(hoursend[0]),parseInt(hoursend[1])),
										allDay: false,
										url: '/meeting/'+meeting.pk});

						}
		                
		                callback(events);
		            }
		        });
		    }

	});	
});