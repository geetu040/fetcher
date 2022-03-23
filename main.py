from flask import Flask, render_template, request, send_from_directory
import json, os
from grid import Grid

rows = 31
cols = 28
with open('static/mapping.json', 'r') as f:
	map = json.load(f)

grid = Grid(rows, cols, map)

app = Flask(__name__, template_folder='static')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
	params = {
		'rows': rows,
		'cols': cols,
		'map': map,
	}
	return render_template("index.html", params=params)

@app.route("/act", methods=["GET", "POST"])
def act():
	"""
	here data and response are tuples consisting of 4 items
	- fet_pos
	- tar_pos
	- prev_dir
	- steps
	"""
	action = request.args.get('action')
	data = json.loads(request.args.get('data'))
	response = grid.handle_action(action, data)
	return json.dumps(response)

if __name__ == '__main__':
	app.run(debug=True)