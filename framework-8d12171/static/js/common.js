Date.prototype.format = function (fmt) { //author: meizz
	var o = {
		"M+": this.getMonth() + 1, //月份
		"d+": this.getDate(), //日
		"h+": this.getHours(), //小时
		"m+": this.getMinutes(), //分
		"s+": this.getSeconds(), //秒
		"q+": Math.floor((this.getMonth() + 3) / 3), //季度
		"S": this.getMilliseconds() //毫秒
	};
	if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
	for (var k in o)
		if (new RegExp("(" + k + ")").test(fmt))
			fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
	return fmt;
};

var COMMON = {};

(function (exports) {
	exports.formatTimestamp = function (ts) {
		if (!ts) return '-';
		return new Date(ts * 1000).format('yyyy-MM-dd hh:mm:ss');
	};

	exports.displayHtml = function (str) {
		return str.replace(/&/g, '&amp;')
			.replace(/</g, '&lt;')
			.replace(/>/g, '&gt;')
			.replace(/"/g, '&quot;');
	};

	exports.confirm = function (content, icon, title, confirmCallback, cancelCallback) {
		layer.confirm(content, {icon: icon, title: title}, function (index) {
			confirmCallback();
			layer.close(index);
		}, function (index) {
			if (cancelCallback && typeof(cancelCallback) == "function") {
				cancelCallback();
			}
			layer.close(index);
		});
	};

	/**
	 * option 属性
	 *  tpl                 对话框模板
	 *  title               对话框标题
	 *  before              对话框展示前的插入函数
	 *  after               对话框展示后的插入函数
	 *  extraLayerConfig    额外的layer参数
	 */
	exports.showDialog = function (option) {
		var DLG = option.tpl.clone().insertBefore(option.tpl).removeAttr('id');

		if (option.before !== undefined && option.before !== null)
			option.before(DLG);

		var layerConfig = {
			type: 1,
			title: option.title,
			area: "800px",
			shadeClose: true,
			content: DLG,
			end: function () {
				setTimeout(function () {
					DLG.remove();
				}, 1000); // 还需要一点动画时间让 layer 删除附属于 DLG 的一些东西
			}
		};
		if (option.extraLayerConfig !== undefined && option.extraLayerConfig !== null)
			for (var k in option.extraLayerConfig)
				layerConfig[k] = option.extraLayerConfig[k];

		console.log("will open layer", layerConfig);

		var LAYER = layer.open(layerConfig);

		var Close = function () {
			layer.close(LAYER);
		};

		DLG.find('.dialog-close').on('click', function () {
			Close();
		});

		if (option.after !== undefined && option.after !== null)
			option.after(DLG, LAYER, Close);
	}
})(COMMON);