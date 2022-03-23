// INITIALIZING VARIABLES
prev_dir = 4
steps = 0
score = 0
hits = 0
missed = 0
int_var = 0
report_action('change both')

function report_action(action) {
	/*   
	--> available actions
	- change fetcher
	- change target
	- change both
	- ArrowUp | ArrowDown | ArrowLeft | ArrowRight
	- 0 | . | 1 | 2 | 3
	*/
	returned = $.ajax({
		type: 'GET',
		data: {
			'action': action,
			'data': JSON.stringify({
				fet: [
					parseInt(getComputedStyle(fet).getPropertyValue('grid-column-start')),
					parseInt(getComputedStyle(fet).getPropertyValue('grid-row-start'))
				],
				tar: [
					parseInt(getComputedStyle(tar).getPropertyValue('grid-column-start')),
					parseInt(getComputedStyle(tar).getPropertyValue('grid-row-start'))
				],
				prev_dir: prev_dir,
				steps: steps,
				score: score,
				hits: hits,
				missed: missed,
			})
		},
		url: '/act',
		dataType: 'json',
		async: false,
		success: function(response) {
			// updating data
			fet.style.setProperty('grid-area', `${response.fet[1]}/${response.fet[0]}`)
			tar.style.setProperty('grid-area', `${response.tar[1]}/${response.tar[0]}`)
			prev_dir = response.prev_dir
			steps = response.steps
			score = response.score
			hits = response.hits
			missed = response.missed
		}
	})
}
// ADDING CONTROLS WITH ARROW KEYS
document.addEventListener('keydown', (e)=>{ report_action(e.key) });

// HANDLING INSTRUCTION BOX
function handle_ins(mode='change') {
	if (mode == 'change') {
		if (getComputedStyle(ins).getPropertyValue('display') == 'block') {
			ins.style.setProperty('display', 'none')
		} else { ins.style.setProperty('display', 'block') }
	} else { ins.style.setProperty('display', mode) }
}

// HANDLING MODEL BUTTONS
function enable_auto(method) {
	clearInterval(int_var)
	stopped = false
	int_var = setInterval(()=>{
		report_action(method)
	}, 200)
}