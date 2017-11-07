<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8" isELIgnored="false"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>OLAP管理系统</title>
<link rel="stylesheet" type="text/css" href="static/css/olap.css"/>
<link rel="shortcut icon" href="static/img/favicon.ico" />
</head>
<body>
    <!-- navbar start -->
	<div class="navbar">
		<div class="logo">OLAP&nbsp;&nbsp;管理系统</div>
		<div class="nav-group">
			<a class="nav-item-cluster selected nav-btn" href=".">数据库集群管理</a>
			<a class="nav-item-data nav-btn" href="showdatabases">数据库管理</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">数据库节点统计</p>
		<table class="table-theme-b">
			<thead>
				<tr>
					<th>状态</th>
					<th>数量</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>掉线</td>
					<td>${dieCount}</td>
				</tr>
				<tr>
					<td>在线</td>
					<td>${livingCount}</td>
				</tr>
			</tbody>
		</table>
		<p class="title">数据库节点查看</p>
		<table class="table-theme-b" id="olapClusterList">
			<thead>
				<tr>
					<th>节点名称</th>
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
		var cs = ${cs};
		var text = {Die:"掉线",Living:"在线"}
		
		
		for (var i=0; i<cs.rows.length; i++){
			$("#olapClusterList").append("<tr>"+
				"<td>"+cs.rows[i][0]+ "</td>"+
				"<td>"+cs.rows[i][1]+ "</td>"+
				"<td>"+text[cs.rows[i][2]]+ "</td>"+
			"</tr>");
			}
		
})		
</script>
</body>
</html>