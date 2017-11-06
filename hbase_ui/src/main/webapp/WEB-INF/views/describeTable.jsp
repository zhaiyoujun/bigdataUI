<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" isELIgnored="false"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>HBASE管理系统</title>
<link rel="stylesheet" type="text/css" href="static/css/hbase.css"/>
</head>
<body>
    <!-- navbar start -->
	<div class="navbar">
		<div class="logo">HBASE&nbsp;&nbsp;管理系统</div>
		<div class="nav-group">
			<a class="nav-item-cluster" href=".">集群</a>
			<a class="nav-item-data selected" href="showdatabases">数据</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<a class="back" onclick="window.history.back()">表统计</a>
		<table class="table-theme-d" id="hbaseTableList">
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
		console.log("dt",dt);
		/* for (var i=0; i<dt.dt.length; i++){
			$("#hbaseTableList").append("<tr>"+
				"<td>"+dt.dt.+ "</td>"+
				"<td>"+dt.dt.+ "</td>"+
				"<td>"+dt.dt.+ "</td>"+
			"</tr>");
			} */
})		
</script>
</body>
</html>