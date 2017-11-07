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
		<p class="title">详情查看
			<a onclick="window.history.back()" class="back">返回</a>
		</p>
		<table class="table-theme-c" id="stormTopologyDetails">
			<thead>
				<tr>
					<th>时间</th>
					<th>发送数</th>
					<th>提交数</th>
					<th>确认数</th>
					<th>失败数</th>
				</tr>
			</thead>
			<tbody>

			</tbody>
		</table>
	</div>
<script type="text/javascript" src="static/js/jquery-3.2.1.min.js"></script>
<script type="text/javascript" src="static/js/storm.js"></script>
<script type="text/javascript" src="static/js/storm-topology-details.js"></script>
</body>
</html>