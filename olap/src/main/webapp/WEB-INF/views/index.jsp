<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8" isELIgnored="false"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>OLAP管理系统</title>
<link rel="stylesheet" type="text/css" href="static/css/olap.css"/>
</head>
<body>
    <!-- navbar start -->
	<div class="navbar">
		<div class="logo">OLAP&nbsp;&nbsp;管理系统</div>
		<div class="nav-group">
			<a class="nav-item-cluster selected" href=".">集群</a>
			<a class="nav-item-data" href="showdatabases">数据</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">状态统计</p>
		<table class="table-theme-a">
			<tbody>
				<tr>
					<td>Die</td>
					<td>${dieCount}</td>
				</tr>
				<tr>
					<td>Living</td>
					<td>${livingCount}</td>
				</tr>
			</tbody>
		</table>
		<p class="title">节点列表</p>
		<table class="table-theme-b" id="olapClusterList">
			<thead>
				<tr>
					<th>集群</th>
					<th>IP</th>
					<th>状态</th>
				</tr>
			</thead>
			<tbody>

			</tbody>
		</table>
	</div>
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script>
$(function(){
		string cs = [[qwe,qwew],[0,0],[3,3]];
		for (var i=0; i<cs.length; i++){
			$("#olapClusterList").append("<tr>"+
				"<td>"+i+"</td>"+
				"<td>"+cs[i][0]+ "</td>"+
				"<td>"+cs[i][1]+ "</td>"+
			"</tr>");
			alert("sad",cs.length);
			console.log("sad",cs.length);
			}
		
})		
</script>
</body>
</html>