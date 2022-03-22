from flask import Flask, render_template, request, send_from_directory, url_for
import json, os
from grid import Grid

rows = 31
cols = 28
with open('static/mapping.json', 'r') as f:
	map = json.load(f)


grid = Grid(rows, cols, map, record_file_url='current_dataset.csv')

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
		'fet': grid.fet,
		'tar': grid.tar,
	}
	return render_template("index.html", params=params)

@app.route("/act", methods=["GET", "POST"])
def act():
	action = request.args.get('action')
	grid.handle_action(action)
	return json.dumps({'fet': grid.fet, 'tar': grid.tar})

if __name__ == '__main__':
	app.run(debug=True)
