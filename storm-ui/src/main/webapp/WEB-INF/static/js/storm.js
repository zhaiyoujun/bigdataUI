$(function(){
	var STORM_UI_HOST = $('body').data('storm-ui');
	$.ajax({
		type:"GET",
		url:STORM_UI_HOST + "/api/v1/cluster/summary",
		dataType:"jsonp",
		jsonp:"callback",
		timeout:"1000",
		success:function(data){
			console.log("1",STORM_UI_HOST);
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
			console.log("2",STORM_UI_HOST);
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
			console.log("3",STORM_UI_HOST);
			for (var i=0; i<data.topologies.length; i++){
				
				var string = data;
				$("#stormTopologyList tbody").append("<tr>"+
					"<td>"+string.topologies[i].name+ "</td>"+
					"<td>"+string.topologies[i].status+ "</td>"+
					"<td>"+string.topologies[i].uptime+ "</td>"+
					"<td>"+string.topologies[i].workersTotal+ "</td>"+
					"<td>"+string.topologies[i].executorsTotal+ "</td>"+
					"<td>"+string.topologies[i].tasksTotal+ "</td>"+
					"<td><a href='topologydetails?id="+string.topologies[i].id+"&sys="+string.topologies[i].status+"' onclock='saveValue'>查看</a></td>"+
				"</tr>");
				
				
				}
		},
		error:function(jqXHR){
			alert("发生错误："+jqXHR.status);
		}
	})	
	

})