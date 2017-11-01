<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8"%>
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
		<div class="refresh" onclick="myrefresh()">刷新</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">状态统计</p>
		<table class="table-theme-a">
			<tbody>
				<tr>
					<td>Die</td>
					<td>0</td>
				</tr>
				<tr>
					<td>Living</td>
					<td>23</td>
				</tr>
			</tbody>
		</table>
		<p class="title">节点列表</p>
		<table class="table-theme-b">
			<thead>
				<tr>
					<th>集群</th>
					<th>IP</th>
					<th>状态</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<td>TASK 1508307629.78 AAsvJ</td>
					<td>calcpi (1.0.0)</td>
					<td>FINISHED</td>
				</tr>
				<tr>
					<td>TASK 1508307629.78 AAsvJ</td>
					<td>calcpi (1.0.0)</td>
					<td>FINISHED</td>
				</tr>
			</tbody>
		</table>
	</div>
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script type="text/javascript" src="static/js/olap.js"></script>
</body>
</html>