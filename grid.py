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
		self.fet = None
		self.tar = None
		self.data = ''

		self.rePos(fet=True, tar=True)

	def rePos(self, fet=False, tar=False):
		self.steps = 0
		self.best_dir = 4
		cord_fet = random.choice(self.map)
		cord_tar = random.choice(self.map)
		if fet:
			if cord_fet != self.fet:
				self.fet = cord_fet
			else:
				self.rePos(fet=fet, tar=tar)
		if tar:
			if cord_tar != self.tar:
				self.tar = cord_tar
			else:
				self.rePos(fet=fet, tar=tar)

	def handle_action(self, action):
		if action == 'change fetcher':
			self.rePos(fet=True)
		elif action == 'change target':
			self.rePos(tar=True)
		elif action == 'change both':
			self.rePos(tar=True, fet=True)
		elif 'Arrow' in action:
			self.move(method='key', dir=action[5:6].lower())
		elif action == ' ':
			self.move(method='euler alog')
		elif action == '0':
			self.move(method='abs alog')
		elif action == '1':
			self.move(method='euler model')
		elif action == '2':
			self.move(method='abs model')
		elif action == '3':
			self.move(method='manual model')
		elif action == 'Enter':
			self.save()
		elif action == 'Backspace':
			self.data = ''
			self.best_dir = 4


	def move(self, method, dir=None):
		self.steps += 1
		if self.steps > 100:
			self.rePos(tar=True)
			self.missed += 1
		if method == 'key':
			self.move_with_keys(dir=dir)
		elif method == 'euler alog':
			self.move_with_alog(method='euler')
		elif method == 'abs alog':
			self.move_with_alog(method='abs')
		elif method == 'euler model':
			self.move_with_model(method='euler')
		elif method == 'abs model':
			self.move_with_model(method='abs')
		elif method == 'manual model':
			self.move_with_model(method='manual')
		
		if self.fet == self.tar:
			self.score += 1
			self.rePos(tar=True)

	def save(self):
		if self.data != '':
			with open(self.record_file_url, 'a') as f:
				f.write(self.data)
			self.data = ''