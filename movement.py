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
	def move_with_keys(self, dir, allowHit=True):

		next_cord = self.fet.copy()
		if dir == 'u':
			next_cord[1] -= 1
		elif dir == 'l':
			next_cord[0] -= 1
		elif dir == 'd':
			next_cord[1] += 1
		elif dir == 'r':
			next_cord[0] += 1

		if (next_cord in self.map or allowHit) and (next_cord[0]!=0 and next_cord[1]!=0 and next_cord[0]!=self.cols+1 and next_cord[1]!=self.rows+1):
			dataline = f'\n{self.fet[0]},{self.fet[1]},{self.tar[0]},{self.tar[1]},{self.best_dir},'

			self.fet = next_cord[:]
			self.best_dir = ['u', 'l', 'd', 'r'].index(dir)

			dataline += f'{self.best_dir}'
			self.data += dataline

	def move_with_alog(self, method='euler'):
		possible_dirs = [
			int([self.fet[0], self.fet[1]-1] in self.map),
			int([self.fet[0]-1, self.fet[1]] in self.map),
			int([self.fet[0], self.fet[1]+1] in self.map),
			int([self.fet[0]+1, self.fet[1]] in self.map),
		]
		if self.best_dir != 4:
			possible_dirs[(self.best_dir+2) % 4] = 0
		if method == 'euler':
			distances = [
				(self.fet[0] - self.tar[0])**2 + (self.fet[1]-1 - self.tar[1])**2,
				(self.fet[0]-1 - self.tar[0])**2 + (self.fet[1] - self.tar[1])**2,
				(self.fet[0] - self.tar[0])**2 + (self.fet[1]+1 - self.tar[1])**2,
				(self.fet[0]+1 - self.tar[0])**2 + (self.fet[1] - self.tar[1])**2,
			]
		elif method == 'abs':
			distances = [
				abs(self.fet[0] - self.tar[0]) + abs(self.fet[1]-1 - self.tar[1]),
				abs(self.fet[0]-1 - self.tar[0]) + abs(self.fet[1] - self.tar[1]),
				abs(self.fet[0] - self.tar[0]) + abs(self.fet[1]+1 - self.tar[1]),
				abs(self.fet[0]+1 - self.tar[0]) + abs(self.fet[1] - self.tar[1]),
			]
			
		best_dir = None
		shortest_d = 99999999
		for i in range(4):
			if possible_dirs[i] and distances[i]<shortest_d:
				shortest_d = distances[i]
				best_dir = i
		
		self.move_with_keys(dir=['u', 'l', 'd', 'r'][best_dir])

	def move_with_model(self, method):
		X = [
			self.fet[0] / 27,
			self.fet[1] / 31,
			self.tar[0] / 27,
			self.tar[1] / 31,
			int([self.fet[0], self.fet[1]-1] in self.map),
			int([self.fet[0]-1, self.fet[1]] in self.map),
			int([self.fet[0], self.fet[1]+1] in self.map),
			int([self.fet[0]+1, self.fet[1]] in self.map),
		]
		if self.best_dir != 4:
			X[ 4 + (self.best_dir+2)%4 ] = 0
		
		pred = models[method].predict([X])
		pred = list(pred[0]).index(max(pred[0]))
		dir = ['u', 'l', 'd', 'r'][pred]
		self.move_with_keys(dir, allowHit=True)