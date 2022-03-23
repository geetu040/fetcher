prev_dir = 4
steps = 0
function report_action(action) {
	returned = $.ajax({
		type: 'GET',
		data: {
			'action': action,
			'data': JSON.stringify({
				fet: [parseInt(getComputedStyle(fet).getPropertyValue('grid-column-start')), parseInt(getComputedStyle(fet).getPropertyValue('grid-row-start'))],
				tar: [parseInt(getComputedStyle(tar).getPropertyValue('grid-column-start')), parseInt(getComputedStyle(tar).getPropertyValue('grid-row-start'))],
				prev_dir: prev_dir,
				steps: steps,
			})
		},
		url: '/act',
		dataType: 'json',
		async: false,
		success: function(response) {
			fet.style.setProperty('grid-area', `${response.fet[1]}/${response.fet[0]}`)
			tar.style.setProperty('grid-area', `${response.tar[1]}/${response.tar[0]}`)
			prev_dir = response.prev_dir
			steps = response.steps
		}
	})
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