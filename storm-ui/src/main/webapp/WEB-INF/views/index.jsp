<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8" isELIgnored="false"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>STORM管理系统</title>
<link rel="stylesheet" type="text/css" href="static/css/storm.css"/>
</head>
<body>
    <!-- navbar start -->
	<div class="navbar">
		<div class="logo">STORM&nbsp;&nbsp;管理系统</div>
		<div class="nav-group">
			<a class="nav-item-cluster selected" href=".">集群</a>
			<a class="nav-item-topology" href="topology">拓扑</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">插槽统计</p>
		<table class="table-theme-a">
			<tbody>
				<tr>
					<td>插槽总数</td>
					<td id = "stateTotal"></td>
				</tr>
				<tr>
					<td>已使用插槽</td>
					<td id = "stateLiving"></td>
				</tr>
			</tbody>
		</table>
		<p class="title">节点列表</p>
		<table class="table-theme-b" id="stormClusterList">
			<thead>
				<tr>
					<th>节点名称</th>
					<th>ID</th>
					<th>运行时间</th>
					<th>插槽总数</th>
					<th>已使用插槽</th>
				</tr>
			</thead>
			<tbody>

			</tbody>
		</table>
	</div>
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script>
$(document).ready(function(){

	var url = "http://192.168.2.58:8089/api/v1/cluster/summary";
	$.ajax({
		type:"GET",
		url:url,
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
	
	var url = "http://192.168.2.58:8089/api/v1/supervisor/summary";
	$.ajax({
		type:"GET",
		url:url,
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
	
	 
})
</script>
</body>
</html>