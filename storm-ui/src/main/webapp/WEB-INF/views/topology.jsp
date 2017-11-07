<%@ page language="java" contentType="text/html; charset=UTF-8"
pageEncoding="UTF-8" isELIgnored="false"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>STORM管理系统</title>
<link rel="stylesheet" type="text/css" href="static/css/storm.css"/>
<link rel="shortcut icon" href="static/img/favicon.ico" />
</head>
<body data-storm-ui="${ip}">
    <!-- navbar start -->
	<div class="navbar">
		<div class="logo">STORM&nbsp;&nbsp;管理系统</div>
		<div class="nav-group">
			<a class="nav-item-cluster" href=".">流处理集群管理</a>
			<a class="nav-item-topology selected" href="topology">流式拓扑管理</a>
		</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">拓扑列表</p>
		<table class="table-theme-c" id="stormTopologyList">
			<thead>
				<tr>
					<th>拓扑名称</th>
					<th>状态</th>
					<th>运行时间</th>
					<th>进程数量</th>
					<th>线程数量</th>
					<th>任务数量</th>
					<th>操作</th>
				</tr>
			</thead>
			<tbody>

			</tbody>
		</table>
	</div>
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script type="text/javascript" src="static/js/storm.js"></script>
</body>
</html>