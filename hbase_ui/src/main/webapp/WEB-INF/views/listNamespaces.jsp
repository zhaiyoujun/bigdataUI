<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" isELIgnored="false"%>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>HBASE管理系统</title>
<link rel="stylesheet" type="text/css" href="static/css/hbase.css"/>
<link rel="shortcut icon" href="static/img/favicon.ico" />
</head>
<body>
    <!-- navbar start -->
	<div class="navbar">
		<div class="logo">HBASE&nbsp;&nbsp;管理系统</div>
		<div class="nav-group">
			<a class="nav-item-cluster" href=".">存储集群管理</a>
			<a class="nav-item-data selected" href="listnamespaces">数据库管理</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">数据库查看</p>
		<table class="table-theme-c" id="olapDataList">
			<thead>
				<tr>
					<th>序号</th>
					<th>库名称</th>
					<th>操作</th>
				</tr>
			</thead>
			<tbody>
			
			</tbody>
		</table>
	</div>
	
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script>
$(function(){
		var ns = ${ns};
		for (var i=0; i<ns.namespaces.length; i++)
		  {
			$("#olapDataList tbody").append("<tr>"+
				"<td>"+i+"</td>"+
				"<td>"+ns.namespaces[i]+ "</td>"+
				"<td><a href='listtablesbynamespace?namespace="+ns.namespaces[i]+"'>查看</a></td>"+
			"</tr>");
		  }
})		
</script>
</body>
</html>