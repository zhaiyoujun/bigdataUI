$(function () {

	var PAGE = $('.top-page');

	// tool列表

	var toolTableConfig = {
		method: 'get',
		url: '/api/tool',
		toolbar: PAGE.find('[data-id=tools-table-toolbar]'),
		striped: true,
		cache: false,
		pagination: false,
		sortable: false,
		showColumns: true,
		showToggle: true,
		showRefresh: false,
		cardView: false,
		detailView: false,
		uniqueId: '__TOOL_NAME__',
		columns: [{
			title: "工具名称",
			field: "__TOOL_NAME__"
		}, {
			title: "版本",
			field: "__TOOL_VERSION__"
		}, {
			title: "存储路径",
			field: "__TOOL_PATH__"
		}, {
			title: "",
			width: 1,
			class:"padding68",
			formatter: function (value, row, index) {
				return '<button class="btn-delete" data-index="' + index + '">删除</button> ';
			}
		}],
		onLoadSuccess: function (r) {
			TOOL_TABLE.find('.tool-del-btn').on('click', function () {
				var tool = r.data[$(this).data('index')];
				var toolName = tool.__TOOL_NAME__;
				if (tool.__TOOL_VERSION__) toolName += ' (' + tool.__TOOL_VERSION__ + ')';
				COMMON.confirm('确认要删除工具 ' + toolName + ' ?', 0, '警告', function () {
					$.ajax({
						method: 'post',
						url: '/api/tool/del',
						data: {operation: tool.__TOOL_NAME__, version: tool.__TOOL_VERSION__},
						success: function () {
							TOOL_TABLE.bootstrapTable('refresh');
						}
					})
				});
			});
		}
	};

	var TOOL_TABLE = PAGE.find('[data-id=tools-table]');
	TOOL_TABLE.bootstrapTable(toolTableConfig);

	// 添加工具的按钮

	PAGE.find('[data-id=tools-add]').on('click', function () {
		COMMON.showDialog({
			tpl: $('#addToolDLG'),
			title: '添加工具',
			after: function (DLG, LAYER, Close) {
				DLG.find('form').formValidation({
					message: '输入格式不正确',
					fields: {
						operation: {
							validators: {
								notEmpty: {}
							}
						},
						version: {
							validators: {
								notEmpty: {}
							}
						},
						tar: {
							validators: {
								notEmpty: {}
							}
						}
					}
				}).on('success.form.fv', function (e) {
					var formData = new FormData(DLG.find('form')[0]);
					$.ajax({
						method: 'post',
						url: '/api/tool',
						data: formData,
						contentType: false,
						processData: false,
						success: function () {
							Close();
							TOOL_TABLE.bootstrapTable('refresh');
						}
					});
					return false;
				});
				DLG.find('[data-id=dialog-close]').on('click', function () {
					Close();
				});
			}
		});
	});

	// 导航栏

	$('ul.navbar-nav a[data-id=tool]').parent().addClass('active');
	$('ul.navbar-nav a[data-id=refresh]').on('click', function () {
		TOOL_TABLE.bootstrapTable('refresh');
	});
	
	$(".nav-group a[data-id=tool]").addClass("selected");
});