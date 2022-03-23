import random
from movement import Movement

class Grid(Movement):
	def __init__(self, rows, cols, map, record_file_url):
		self.rows = rows
		self.cols = cols
		self.map = map
		self.record_file_url = record_file_url
		self.hits = 0
		self.score = 0
		self.steps = 0
		self.missed = 0
		self.best_dir = 4
		self.data = ''

	def rePos(self, fet=False, tar=False, data=None):
		new_fet = data['fet']
		new_tar = data['tar']

		if fet and tar:
			new_fet = random.choice(self.map)
			new_tar = random.choice(self.map)
			while new_fet == data['fet'] or new_tar == data['tar'] or new_fet == new_tar:
				new_fet = random.choice(self.map)
				new_tar = random.choice(self.map)
		elif fet:
			new_fet = random.choice(self.map)
			while new_fet == data['fet'] or new_fet == data['tar']:
				new_fet = random.choice(self.map)
		elif tar:
			new_tar = random.choice(self.map)
			while new_tar == data['fet'] or new_tar == data['tar']:
				new_tar = random.choice(self.map)

		data['fet'] = new_fet
		data['tar'] = new_tar
		data['prev_dir'] = 4
		data['steps'] = 0
		return data

	def handle_action(self, action, data):
		if action == 'change fetcher':
			new_data =  self.rePos(fet=True, data=data)
		elif action == 'change target':
			new_data = self.rePos(tar=True, data=data)
		elif 'Arrow' in action:
			new_data = self.move(method='key', dir=action[5:6].lower(), data=data)
		elif action == ' ':
			new_data = self.move(method='euler alog', data=data)
		elif action == '0':
			new_data = self.move(method='abs alog', data=data)
		elif action == '1':
			new_data = self.move(method='euler model', data=data)
		elif action == '2':
			new_data = self.move(method='abs model', data=data)
		elif action == '3':
			new_data = self.move(method='manual model', data=data)
		# elif action == 'Enter':
		# 	self.save()
		# elif action == 'Backspace':
		# 	self.data = ''
		# 	self.best_dir = 4
		return new_data


	def move(self, method, dir=None, data=None):
		if data['steps'] > 100:
			self.missed += 1
			data = self.rePos(tar=True, data=data)

		if method == 'key':
			new_data = self.move_with_keys(dir=dir, data=data)
		elif 'alog' in method:
			new_data = self.move_with_alog(method=method[:-5], data=data)
		elif 'model' in method:
			new_data = self.move_with_model(method=method[:-6], data=data)
		
		if data['fet'] == data['tar']:
			self.score += 1
			new_data = self.rePos(tar=True, data=new_data)
		new_data['steps'] += 1

		return new_data

	def save(self):
		if self.data != '':
			with open(self.record_file_url, 'a') as f:
				f.write(self.data)
			self.data = ''