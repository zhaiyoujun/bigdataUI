$(function(){
	var STORM_UI_HOST = "${getStorm_Host_Ip}";

	$.ajax({
		type:"GET",
		url:STORM_UI_HOST + "/api/v1/cluster/summary",
		dataType:"jsonp",
		jsonp:"callback",
		timeout:"1000",
		success:function(data){
			if(data){
				$("#stateTotal").html(data.slotsTotal);
				$("#stateLiving").html(data.slotsUsed);
			}else{
				$("#stateTotal").html("出现错误："+data.slotsUsed);
				$("#stateLiving").html("出现错误："+data.slotsFree);
			}
		},
		error:function(jqXHR){
			alert("发生错误："+jqXHR.status);
		}
	})
	
	$.ajax({
		type:"GET",
		url:STORM_UI_HOST + "/api/v1/supervisor/summary",
		dataType:"jsonp",
		jsonp:"callback",
		timeout:"1000",
		success:function(data){
			
			for (var i=0; i<data.supervisors.length; i++){
				var string = data;
				$("#stormClusterList tbody").append("<tr>"+
					"<td>"+string.supervisors[i].host+ "</td>"+
					"<td>"+string.supervisors[i].id+ "</td>"+
					"<td>"+string.supervisors[i].uptime+ "</td>"+
					"<td>"+string.supervisors[i].slotsTotal+ "</td>"+
					"<td>"+string.supervisors[i].slotsUsed+ "</td>"+
				"</tr>");
				}
		},
		error:function(jqXHR){
			alert("发生错误："+jqXHR.status);
		}
	})	
	
	 
	$.ajax({
		type:"GET",
		url:STORM_UI_HOST + "/api/v1/topology/summary",
		dataType:"jsonp",
		jsonp:"callback",
		timeout:"1000",
		success:function(data){
			
			for (var i=0; i<data.topologies.length; i++){
				var string = data;
				$("#stormTopologyList tbody").append("<tr>"+
					"<td>"+string.topologies[i].name+ "</td>"+
					"<td>"+string.topologies[i].id+ "</td>"+
					"<td>"+string.topologies[i].status+ "</td>"+
					"<td>"+string.topologies[i].uptime+ "</td>"+
					"<td>"+string.topologies[i].workersTotal+ "</td>"+
					"<td>"+string.topologies[i].executorsTotal+ "</td>"+
					"<td>"+string.topologies[i].tasksTotal+ "</td>"+
					"<td><a href=''>查看</a></td>"+
				"</tr>");
				}
		},
		error:function(jqXHR){
			alert("发生错误："+jqXHR.status);
		}
	})	
})