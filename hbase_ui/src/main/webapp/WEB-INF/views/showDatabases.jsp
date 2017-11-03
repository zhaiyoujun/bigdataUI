<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" isELIgnored="false"%>
<%@taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>OLAP管理系统</title>
<link rel="stylesheet" type="text/css" href="static/css/hbase.css"/>
</head>
<body>
    <!-- navbar start -->
	<div class="navbar">
		<div class="logo">OLAP&nbsp;&nbsp;管理系统</div>
		<div class="nav-group">
			<a class="nav-item-cluster" href=".">集群</a>
			<a class="nav-item-data selected" href="showdatabases">数据</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">数据统计</p>
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
<script type="text/javascript" src="static/js/olap.js"></script>
<script>
$(function(){
		var rs = ${rs};
		for (var i=0; i<rs.rows.length; i++)
		  {
			$("#olapDataList").append("<tr>"+
				"<td>"+i+"</td>"+
				"<td>"+rs.rows[i]+ "</td>"+
				"<td><a href='showtables?database="+rs.rows[i]+"'>查看</a></td>"+
			"</tr>");
		  }
})		
</script>
</body>
</html>