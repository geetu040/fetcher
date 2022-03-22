function reMap(fet_cord, tar_cord) {
	fet.style.setProperty('grid-area', `${fet_cord[1]}/${fet_cord[0]}`)
	tar.style.setProperty('grid-area', `${tar_cord[1]}/${tar_cord[0]}`)
}
function report_action(action) {
	returned = $.ajax({
		type: 'GET',
		data: { action: action },
		url: '/act',
		dataType: 'json',
		async: false,
	})
	fet_cord = JSON.parse(returned.responseText).fet
	tar_cord = JSON.parse(returned.responseText).tar
	reMap(fet_cord, tar_cord)
}
document.addEventListener('keydown', (e)=>{
	report_action(e.key)
});
function handle_ins(mode='change') {
	if (mode == 'change') {
		if (getComputedStyle(ins).getPropertyValue('display') == 'block') {
			ins.style.setProperty('display', 'none')
		} else { ins.style.setProperty('display', 'block') }
	} else { ins.style.setProperty('display', mode) }
}
int_var = 0
function enable_auto(method) {
	clearInterval(int_var)
	stopped = false
	int_var = setInterval(()=>{
		report_action(method)
	}, 200)
}