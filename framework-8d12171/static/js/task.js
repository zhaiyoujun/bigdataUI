$(function () {

	var PAGE = $('.top-page');

	// 任务状态统计

	function updateStatusStatistic(data) {
		PAGE.find('[data-id=tasks-status-statistic] [data-tag]').each(function (index, ITEM) {
			$(ITEM).text(data[$(ITEM).data('tag')]);
		});
	}

	function refreshStatusStatistic() {
		$.ajax({
			method: 'get',
			url: '/api/task/stat',
			data: {},
			success: function (data) {
				updateStatusStatistic(data);
			}
		});
	}

	refreshStatusStatistic();

	// 任务列表

	function showTasks(TABLE, TABLE_TOOLBAR, fatherId, jump) {
		console.log('showTasks', TABLE, TABLE_TOOLBAR, fatherId, jump);
		var config = {
			method: 'get',
			url: '/api/task',
			toolbar: TABLE_TOOLBAR,
			striped: true,
			cache: false,
			pagination: true,
			sidePagination: 'server',
			paginationHAlign: 'right',
			paginationDetailHAlign: 'left',
			pageNumber: 1,
			pageSize: 50,
			pageList: [50],
			sortable: false,
			showColumns: true,
			showToggle: true,
			showRefresh: !jump,
			cardView: false,
			detailView: false,
			uniqueId: '__TASK_ID__',
			columns: [{
				title: "Task ID",
				field: "__TASK_ID__",
				formatter: function (value, row, index) {
					if (row.__FATHER_ID__)
						value += ' (' + row.__FATHER_ID__ + ')';
					if (jump)
						value = '<span class="text-clickable task-view-family" data-id="' + row.__TASK_ID__ + '">' + value + '</span>';
					return value;
				}
			}, {
				title: "Operation",
				field: "__OPERATION__",
				formatter: function (value, row, index) {
					if (row.__OPERATION_VERSION__)
						return value + ' (' + row.__OPERATION_VERSION__ + ')';
					return value;
				}
			}, {
				title: "Status",
				field: "__STATUS__"
			}, {
				title: "Agent ID",
				field: "__AGENT_ID__"
			}, {
				title: "Exit Code",
				field: "__EXIT_CODE__"
			}, {
				title: "Killed",
				field: "__KILLED__"
			}, {
				title: "Submit Time",
				field: "__SUBMIT_TIME__",
				formatter: COMMON.formatTimestamp
			}, {
				title: "Prepare Time",
				field: "__PREPARE_TIME__",
				formatter: COMMON.formatTimestamp
			}, {
				title: "Finish Time",
				field: "__FINISH_TIME__",
				formatter: COMMON.formatTimestamp
			}, {
				title: "",
				width: 1,
				formatter: function (value, row, index) {
					return '<button class="btn btn-xs btn-info task-more-btn" data-index="' + index + '">MORE</button>';
				}
			}, {
				title: "",
				width: 1,
				formatter: function (value, row, index) {
					return '<button class="btn btn-xs btn-success task-dup-btn" data-index="' + index + '">DUP</button>';
				}
			}, {
				title: "",
				width: 1,
				formatter: function (value, row, index) {
					return '<button class="btn btn-xs btn-danger task-kill-btn" data-id="' + row.__TASK_ID__ + '">KILL</button>';
				}
			}],
			onLoadSuccess: function (r) {
				console.log('onLoadSuccess', r);
				TABLE.find('.task-view-family').on('click', function () {
					var taskId = $(this).data('id');
					COMMON.showDialog({
						tpl: $('#showTaskFamilyDLG'),
						title: 'Family Of Task ' + taskId,
						before: function (DLG) {
							showTasks(DLG.find('table'), null, taskId, false);
						},
						extraLayerConfig: {
							area: "1000px",
							maxmin: true,
							resize: false,
							scrollbar: true
						}
					});
				});

				TABLE.find('.task-kill-btn').on('click', function () {
					var taskId = $(this).data('id');
					COMMON.confirm('Are you sure to kill task ' + taskId + ' ?', 0, 'Warning', function () {
						$.ajax({
							method: 'post',
							url: '/api/task/kill',
							data: {taskId: taskId},
							success: refreshPage
						})
					})
				});

				TABLE.find('.task-dup-btn').on('click', function () {
					var data = r.data.rows[$(this).data('index')];
					COMMON.confirm('Are you sure to dup task ' + data.__TASK_ID__ + ' ?', 1, 'Info', function () {
						var request = {};
						for (var k in data)
							if (!k.startsWith('__') || !k.endsWith('__'))
								request[k] = data[k];
						request.__TYPE__ = 'TASK/SUBMIT';
						request.__AGENT_TAG__ = data['__AGENT_TAG__'];
						request.__OPERATION__ = data['__OPERATION__'];
						request.__OPERATION_VERSION__ = data['__OPERATION_VERSION__'];
						console.log(request);
						$.ajax({
							method: 'post',
							url: '/api',
							data: {request: JSON.stringify(request)},
							success: refreshPage
						})
					})
				});

				TABLE.find('.task-more-btn').on('click', function () {
					var data = r.data.rows[$(this).data('index')];
					layer.open({
						title: 'Full Info',
						content: '<pre>' + COMMON.displayHtml(JSON.stringify(data, null, 4)) + '</pre>',
						area: '800px',
						btn: null,
						shadeClose: true
					});
				});
			},
			queryParams: function (params) {
				if (fatherId) params['fatherId'] = fatherId;
				params['deep'] = (jump ? 1 : 10000);
				return params;
			}
		};

		TABLE.bootstrapTable(config);
		return TABLE;
	}

	var TASK_TABLE = showTasks(PAGE.find('[data-id=tasks-table]'), PAGE.find('[data-id=tasks-table-toolbar]'), null, true);

	// 提交任务的按钮

	PAGE.find('[data-id=tasks-submit]').on('click', function () {
		COMMON.showDialog({
			tpl: $('#submitTaskDLG'),
			title: '提交任务',
			before: function (DLG) {
				$.ajax({
					method: 'get',
					url: '/api/tool',
					async: false,
					success: function (r) {
						var OP_SELELCT = DLG.find('select[name=operation]');
						r.data.forEach(function (tool, index) {
							var name = tool.__TOOL_NAME__;
							if (tool.__TOOL_VERSION__)
								name = tool.__TOOL_NAME__ + '-' + tool.__TOOL_VERSION__;
							OP_SELELCT.append($('<option/>').val(name).text(name));
						});
					}
				});

				$.ajax({
					method: 'get',
					url: '/api/agent',
					async: false,
					success: function (r) {
						var dict = {};
						r.data.forEach(function (agent) {
							for (tag in agent.__AGENT_TAG__) dict[tag] = 1;
						});

						var allTags = [];
						for (var tag in dict) allTags.push(tag);
						allTags.sort();
						console.log(allTags);

						var TAG_SELELCT = DLG.find('select[name=agentTag]');
						allTags.forEach(function (tag) {
							TAG_SELELCT.append($('<option/>').val(tag).text(tag));
						});

						DLG.find('select[name=agentTag]').multipleSelect();
					}
				});
			},
			after: function (DLG, LAYER, Close) {
				DLG.find('[data-id=task-add-param]').on('click', function () {
					var TPL = DLG.find(".param-box.box-tpl");
					var ITEM = TPL.clone().removeClass('box-tpl');
					TPL.before(ITEM);
					ITEM.find('[data-id=task-del-param]').on('click', function () {
						ITEM.remove();
					});
				});

				DLG.find('[data-id=dialog-confirm]').on('click', function () {
					$.ajax({
						method: 'post',
						url: '/api/task/submit',
						data: DLG.find('form').serialize(),
						success: function () {
							Close();
							refreshPage();
						}
					});
				});
				DLG.find('[data-id=dialog-close]').on('click', function () {
					Close();
				});
			}
		});
	});

	// 导航栏

	function refreshPage() {
		refreshStatusStatistic();
		TASK_TABLE.bootstrapTable('refresh');
	}

	$('ul.navbar-nav a[data-id=task]').parent().addClass('active');
	$('ul.navbar-nav a[data-id=refresh]').on('click', function () {
		refreshPage();
	});
	$(".nav-group a[data-id=task]").addClass("selected");
});