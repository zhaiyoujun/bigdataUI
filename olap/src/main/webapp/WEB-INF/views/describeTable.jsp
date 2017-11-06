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
		<a class="back" href="showdatabases">数据统计</a>
		<table class="table-theme-d" id="olapTableList">
			<thead>
				<tr>
					<th>COLUMN_NAME</th>
					<th>COLUMN_TYPE</th>
					<th>IS_NULLABLE</th>
					<th>COLUMN_KEY</th>
					<th>COLUMN_DEFAULT</th>
					<th>EXTRA</th>
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
		var dt = ${dt};
		for (var i=0; i<dt.rows.length; i++)
		  {
			$("#olapTableList").append("<tr>");
			for (var j=0; j<dt.rows[i].length; j++) {
				$("#olapTableList").append("<td>"+dt.rows[i][j]+ "</td>");
			}
			$("#olapTableList").append("</tr>");
		  }
})		
</script>
</body>
</html>