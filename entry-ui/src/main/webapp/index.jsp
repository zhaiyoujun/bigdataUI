<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<title>iecas-bigdata</title>
<link rel="stylesheet" type="text/css" href="static/css/entry.css"/>
<link rel="shortcut icon" href="static/img/favicon.ico" />
</head>
<body>
	<!-- title start -->
	<div class="title">数据管理与计算一体机</div>
	<!-- title end -->
	
	<div class="sub-title">产品分支</div>
	
	<ul class="list">
	<!-- 注释： 禁用某系统，在 li标签的class属性中加入disabled类名即可禁用-->
		<li class="item-olap">
			<div class="item-content">
				<p class="name">文件管理系统（OLAP）</p>
				<p class="descr" id="descrOLAP"></p>
				<a href="/olap_ui/">点击查看</a>
			</div>
		</li>
		<li class="item-storm">
			<div class="item-content">
				<p class="name">节点计算系统（STORM）</p>
				<p class="descr" id="descrSTORM"></p>
				<a href="/storm-ui/">点击查看</a>
			</div>
		</li>
		<li class="item-llts">
			<div class="item-content">
				<p class="name">节点计算系统（LLTS）</p>
				<p class="descr" id="descrLLTS"></p>
				<a href="http://localhost:5000/task">点击查看</a>
			</div>
		</li>
		<li class="item-hbase">
			<div class="item-content">
				<p class="name">数据管理（HBASE）</p>
				<p class="descr" id="descrHBASE"></p>
				<a href="/hbase_ui/">点击查看</a>
			</div>
		</li>
		<li class="item-dfs">
			<div class="item-content">
				<p class="name">数据管理（DFS）</p>
				<p class="descr" id="descrDFS"></p>
				<a href="http://192.168.192.130:8120/overview">点击查看</a>
			</div>
		</li>
	</ul>

<script type="text/javascript" src="static/js/entry.js"></script>
</body>
</html>