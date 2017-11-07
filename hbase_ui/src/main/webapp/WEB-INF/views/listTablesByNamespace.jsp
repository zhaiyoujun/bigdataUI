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
			<a class="nav-item-data selected" href="listnamespaces">数据</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">表列表
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
		var tn = ${tn};
		for (var i=0; i<tn.tablesByNamespace.length; i++)
		  {
			$("#olapTableList").append("<tr>"+
				"<td>"+i+"</td>"+
				"<td>"+tn.tablesByNamespace[i]+ "</td>"+
				"<td><a href='describetable?table="+tn.tablesByNamespace[i]+"'>查看</a></td>"+
						"</tr>");
		  }
})		
</script>
</body>
</html>