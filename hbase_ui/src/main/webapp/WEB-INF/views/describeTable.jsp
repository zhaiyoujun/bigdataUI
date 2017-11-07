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
		<p class="title">表详情
		<a onclick="window.history.back()" class="back">返回</a>
		</p>
		<table class="table-theme-c hbaseTable" id="hbaseTableList">
			<thead>				
				<tr>
					<th>列簇</th>
					<th>属性</th>
				</tr>
			</thead>
			<tbody>
			</tbody>
		</table>
	</div>
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script>
$(function(){
	
		var dt = ${dt};
		for (var i=0; i<dt.name.length; i++){
			var CF = $("<td></td>");
			CF.html(dt.name[i]);
			var CF_DETAIL = $("<td><dl></dl></td>");
			for(var j=0; j<dt.rows[i].length; j++){
				CF_DETAIL.find('dl').append(
						"<dd>"+dt.rows[i][j][0]+"</dd>"+
						"<dd>"+dt.rows[i][j][1]+"</dd>");	
			}
			var ROW = $("<tr></tr>");
			ROW.append(CF);
			ROW.append(CF_DETAIL);
			$("#hbaseTableList tbody").append(ROW);
		}
})		
</script>
</body>
</html>