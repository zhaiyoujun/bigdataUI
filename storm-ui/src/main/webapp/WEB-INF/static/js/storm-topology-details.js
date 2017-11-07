$(function(){
	var STORM_UI_HOST = $('body').data('storm-ui');
	GetQueryString();	
	function GetQueryString(name)
	{
	     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
	     var r = window.location.search.substr(1).match(reg);
	     if(r!=null)return  unescape(r[2]); return null;
	}
	 var topologyId = GetQueryString("id");
	 var topologySys = GetQueryString("sys");
	 console.log("4",STORM_UI_HOST);
		
		$.ajax({
			type:"GET",
			url:STORM_UI_HOST + "/api/v1/topology/"+topologyId+"?sys="+topologySys,
			dataType:"jsonp",
			jsonp:"callback",
			timeout:"1000",
			success:function(data){
				console.log(data.topologyStats);
				for (var i=0; i<data.topologyStats.length; i++){
					$("#stormTopologyDetails").append("<tr>"+
						"<td>"+data.topologyStats[i].windowPretty+ "</td>"+
						"<td>"+data.topologyStats[i].window+ "</td>"+
						"<td>"+data.topologyStats[i].emitted+ "</td>"+
						"<td>"+data.topologyStats[i].transferred+ "</td>"+
						"<td>"+data.topologyStats[i].completeLatency+ "</td>"+
					"</tr>");
					}
				
			},
			error:function(jqXHR){
				alert("发生错误："+jqXHR.status);
			}
		})	
})