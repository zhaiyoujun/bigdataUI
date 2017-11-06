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
			<a class="nav-item-cluster" href=".">集群</a>
			<a class="nav-item-topology selected" href="topology">拓扑</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">拓扑列表</p>
		<table class="table-theme-b" id="stormTopologyList">
			<thead>
				<tr>
					<th>拓扑名称</th>
					<th>ID</th>
					<th>状态</th>
					<th>运行时间</th>
					<th>进程数量</th>
					<th>线程数量</th>
					<th>任务数量</th>
				</tr>
			</thead>
			<tbody>

			</tbody>
		</table>
	</div>
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script>
$(document).ready(function(){
	var url = "http://192.168.2.58:8089/api/v1/topology/summary";
	$.ajax({
		type:"GET",
		url:url,
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