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
 
    <center>
        <h2>Hello World</h2>
        <h3>
            <a href="hello?name=zhangsan">点击跳转</a>
        </h3>
        <h3>
            <a href="showdatabases">show databases;</a>
        </h3>
        <h3>
            <a href="showtables?database=test">show tables;</a>
        </h3>
    </center>
    <!-- navbar start -->
	<div class="navbar">
		<div class="logo">OLAP&nbsp;&nbsp;管理系统</div>
		<ul class="nav-group">
			<li class="nav-item-cluster selected">集群</li>
			<li class="nav-item-data">数据</li>
		</ul>
		<div class="refresh">刷新</div>
	</div>
	<!-- navbar end -->
	<div class="content">
		<p class="title">数据统计</p>
		<table class="table-statistics">
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
		<table class="table-list">
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
</body>
</html>