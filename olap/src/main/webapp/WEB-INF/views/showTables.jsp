<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" isELIgnored="false"%>
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
			<a class="nav-item-cluster" href=".">数据库集群管理</a>
			<a class="nav-item-data selected" href="showdatabases">数据库管理</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">表查看
			<a onclick="window.history.back()" class="back">返回</a>
		</p>
		<table class="table-theme-c" id="olapTableList">
			<thead>
				<tr>
					<th>序号</th>
					<th>表名称</th>
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
		var rs = ${rs};
		var db = ${db};
		for (var i=0; i<rs.rows.length; i++)
		  {
			$("#olapTableList tbody").append("<tr>");
			$("#olapTableList tbody").append("<td>"+i+"</td>");
			$("#olapTableList tbody").append("<td>"+rs.rows[i]+ "</td>");
			$("#olapTableList tbody").append("<td><a href='describetable?database="+db.name+"&table="+rs.rows[i]+"'>查看</a></td>");	
			$("#olapTableList tbody").append("</tr>");
		  }		
})		
</script>
</body>
</html>