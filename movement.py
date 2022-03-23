from keras.models import model_from_json

models = {
	'euler': 0,
	'abs': 0,
	'manual': 0,
}
for model_name in models:
	model_url = f'modelling/models/{model_name}_model/{model_name}_model.json'
	weights_url = f'modelling/models/{model_name}_model/{model_name}_weights.h5'
	with open(model_url) as f:
		model = model_from_json(f.read())
	model.load_weights(weights_url)
	models[model_name] = model

class Movement():
	def move_with_keys(self, dir, data, allowHit=True):

		next_cord = data['fet']
		if dir == 'u':
			next_cord[1] -= 1
		elif dir == 'l':
			next_cord[0] -= 1
		elif dir == 'd':
			next_cord[1] += 1
		elif dir == 'r':
			next_cord[0] += 1

		# editing the data
		if (next_cord in self.map or allowHit) and (next_cord[0]!=0 and next_cord[1]!=0 and next_cord[0]!=self.cols+1 and next_cord[1]!=self.rows+1):
			data['fet'] = next_cord
			data['prev_dir'] = ['u', 'l', 'd', 'r'].index(dir)

		# if fetcher hits a wall
		if (next_cord not in self.map and allowHit):
			data['hits'] += 1

		return data

	def move_with_alog(self, method, data):
		possible_dirs = [
			int([data['fet'][0], data['fet'][1]-1] in self.map),
			int([data['fet'][0]-1, data['fet'][1]] in self.map),
			int([data['fet'][0], data['fet'][1]+1] in self.map),
			int([data['fet'][0]+1, data['fet'][1]] in self.map),
		]
		if data['prev_dir'] != 4:
			possible_dirs[(data['prev_dir']+2) % 4] = 0
		if method == 'euler':   # shortest hypotenuis
			distances = [
				(data['fet'][0] - data['tar'][0])**2 + (data['fet'][1]-1 - data['tar'][1])**2,
				(data['fet'][0]-1 - data['tar'][0])**2 + (data['fet'][1] - data['tar'][1])**2,
				(data['fet'][0] - data['tar'][0])**2 + (data['fet'][1]+1 - data['tar'][1])**2,
				(data['fet'][0]+1 - data['tar'][0])**2 + (data['fet'][1] - data['tar'][1])**2,
			]
		elif method == 'abs':   # shortest base + perp
			distances = [
				abs(data['fet'][0] - data['tar'][0]) + abs(data['fet'][1]-1 - data['tar'][1]),
				abs(data['fet'][0]-1 - data['tar'][0]) + abs(data['fet'][1] - data['tar'][1]),
				abs(data['fet'][0] - data['tar'][0]) + abs(data['fet'][1]+1 - data['tar'][1]),
				abs(data['fet'][0]+1 - data['tar'][0]) + abs(data['fet'][1] - data['tar'][1]),
			]
			
		best_dir = None
		shortest_d = 99999999
		for i in range(4):
			if possible_dirs[i] and distances[i]<shortest_d:
				shortest_d = distances[i]
				best_dir = i
		
		return self.move_with_keys(dir=['u', 'l', 'd', 'r'][best_dir], data=data)

	def move_with_model(self, method, data):
		X = [
			data['fet'][0] / 27,
			data['fet'][1] / 31,
			data['tar'][0] / 27,
			data['tar'][1] / 31,
			int([data['fet'][0], data['fet'][1]-1] in self.map),
			int([data['fet'][0]-1, data['fet'][1]] in self.map),
			int([data['fet'][0], data['fet'][1]+1] in self.map),
			int([data['fet'][0]+1, data['fet'][1]] in self.map),
		]
		if data['prev_dir'] != 4:   # removing backward direction from available directions
			X[ 4 + (data['prev_dir']+2)%4 ] = 0
		
		pred = models[method].predict([X])
		pred = list(pred[0]).index(max(pred[0]))  # fetching one with highest probability
		dir = ['u', 'l', 'd', 'r'][pred]

		return self.move_with_keys(dir=dir, data=data)