$(function () {

	var PAGE = $('.top-page');

	// Agent状态统计

	function updateStatusStatistic(data) {
		PAGE.find('[data-id=agents-status-statistic] [data-tag]').each(function (index, ITEM) {
			$(ITEM).text(data[$(ITEM).data('tag')]);
		});
	}

	function refreshStatusStatistic() {
		$.ajax({
			method: 'get',
			url: '/api/agent/stat',
			data: {},
			success: function (data) {
				updateStatusStatistic(data);
			}
		});
	}

	refreshStatusStatistic();

	// Agent 列表

	var agentTableConfig = {
		method: 'get',
		url: '/api/agent',
		toolbar: PAGE.find('[data-id=agents-table-toolbar]'),
		striped: true,
		cache: false,
		pagination: false,
		sortable: false,
		showColumns: true,
		showToggle: true,
		showRefresh: false,
		cardView: false,
		detailView: false,
		uniqueId: '__AGENT_ID__',
		columns: [{
			title: "Agent ID",
			field: "__AGENT_ID__"
		}, {
			title: "IP",
			field: "__AGENT_IP__"
		}, {
			title: "Status",
			field: "__STATUS__"
		}, {
			title: "Tag",
			field: "__AGENT_TAG__",
			formatter: function (value, row, index) {
				console.log(value, row, index);
				var tags = [];
				for (var tk in value) {
					if (value[tk])
						tags.push('<span class="tag"><span class="tag-name">' + tk + '</span><span class="tag-value">' + value[tk] + '</span></span>');
					else
						tags.push('<span class="tag"><span class="tag-name">' + tk + '</span></span>')
				}
				return tags.join('');
			}
		}, {
			title: "Active Time",
			field: "__TIME__",
			formatter: COMMON.formatTimestamp
		}]
	};

	var AGENT_TABLE = PAGE.find('[data-id=agents-table]');
	AGENT_TABLE.bootstrapTable(agentTableConfig);

	// 导航栏

	function refreshPage() {
		refreshStatusStatistic();
		AGENT_TABLE.bootstrapTable('refresh');
	}

	$('ul.navbar-nav a[data-id=agent]').parent().addClass('active');
	$('ul.navbar-nav a[data-id=refresh]').on('click', function () {
		refreshPage();
	});

	$(".nav-group a[data-id=agent]").addClass("selected");
});