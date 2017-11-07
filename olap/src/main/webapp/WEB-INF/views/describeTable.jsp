<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" isELIgnored="false"%>
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
			<a class="nav-item-cluster" href=".">集群</a>
			<a class="nav-item-data selected" href="showdatabases">数据</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">表详情
			<a onclick="window.history.back()" class="back">返回</a>
		</p>
		<table class="table-theme-d" id="olapTableList">
			<thead>				

			</thead>
			<tbody>
			
			</tbody>
		</table>
	</div>
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script>
$(function(){
		var dt = ${dt};
		for (var i=0; i<dt.rows.length; i++)
		  {
			$("#olapTableList tbody").append("<tr>");
			for (var j=0; j<dt.rows[i].length; j++) {
				$("#olapTableList tbody").append("<td>"+dt.rows[i][j]+ "</td>");
			}
			$("#olapTableList tbody").append("</tr>");
		  }
		$("#olapTableList thead").append("<tr>");
		for (var i=0; i<dt.columns.length; i++)
		  {			
			$("#olapTableList thead").append("<td>"+dt.columns[i]+ "</td>");			
		  }
		$("#olapTableList thead").append("</tr>");
})		
</script>
</body>
</html>