function $(selector, context) {
	return (context || document).querySelector(selector);
}

function $$(selector, context) {
	return [].slice.call((context || document).querySelectorAll(selector));
}
$$(".button-box").forEach(function (el) {
	if ($$("button", el).length === 1) {
		$("button", el).style.cssText = "display:block;margin:0 auto;";
	}
})
$("#container").style.display = "block";
$$("#button-box-1 button").forEach(function (btn, index) {
	btn.onclick = function () {
		var type = ["info", "success", "warn", "error"];
		Dialog[type[index]](type[index] + " 对话框", "内容区域");
	}
})
$$("#button-box-2 button").forEach(function (btn, index) {
	btn.onclick = function () {
		Dialog("Hello World");

	}
})
