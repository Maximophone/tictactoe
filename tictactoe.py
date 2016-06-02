class TicTacToe(object):
	
	_VALUES = ('x','o')
	_turn_lookup = {k:v for k,v in zip(_VALUES[-1:]+_VALUES[:-1],_VALUES)}

	def __init__(self,size=3,board=None):
		self.size = size
		self.is_over = False
		self.winner = None
		self.next_player = self._VALUES[0] # x starts
		if not board:
			self.board = ['']*size*size
		else:
			assert len(board)==size*size, "Invalid board size"
			self._sanity_check_board(board)
			self.board = board
			self.next_player = self._VALUES[len([v for v in board if v==self._VALUES[0]])-len([v for v in board if v==self._VALUES[1]])]
			self._check_over()

	@staticmethod
	def _sanity_check_board(board):
		assert len([v for v in board if v==TicTacToe._VALUES[0]]) >= len([v for v in board if v==TicTacToe._VALUES[1]]), "Invalid board"
		assert len([v for v in board if v==TicTacToe._VALUES[0]]) <= len([v for v in board if v==TicTacToe._VALUES[1]]) + 1, "Invalid board"

	def copy(self):
		return TicTacToe(size=self.size,board=self.board[:])

	def get_available_moves(self):
		return [(i,j) for i in range(self.size) for j in range(self.size) if self[i,j]=='']

	def _getij(self,i,j):
		if isinstance(i,slice) and isinstance(j,slice):
			return [
					[
					self._getij(_i,_j) 
					for _j in range(j.start or 0, j.stop or self.size, j.step or 1)
					] 
					for _i in range(i.start or 0, i.stop or self.size, i.step or 1)
					]
		elif isinstance(i,slice):
			return [self._getij(_i,j) for _i in range(i.start or 0, i.stop or self.size, i.step or 1)]
		elif isinstance(j,slice):
			return [self._getij(i,_j) for _j in range(j.start or 0, j.stop or self.size, j.step or 1)]
		else:
			assert i<self.size
			assert j<self.size
			return self.board[i*self.size+j]

	def _setij(self,i,j,value=''):
		assert i<self.size
		assert j<self.size
		self.board[i*self.size+j] = value

	def __getitem__(self,ij):
		assert len(ij)==2
		return self._getij(*ij)

	def __setitem__(self,ij,value):
		assert value==self.next_player, "Wrong player"
		assert not self.is_over, "Over"
		assert self._getij(*ij)==''
		assert value in self._VALUES
		self._setij(*ij,value=value)
		self._update()

	def _update(self):
		self._check_over()
		self.next_player = self._turn_lookup[self.next_player]

	def _check_over(self):
		# Is board filled?
		if '' not in self.board:
			self.is_over = True
		# Checking rows
		lines = []
		for i in range(self.size):
			lines.append(self[i,:])
		for j in range(self.size):
			lines.append(self[:,j])
		lines.append([self[i,i] for i in range(self.size)])
		lines.append([self[self.size-1-i,i] for i in range(self.size)])
		for line in lines:
			for player in self._VALUES:
				if all([x==player for x in line]):
					self.winner = player
					self.is_over = True

	def __str__(self):
		lookup = {'x':'x','o':'o','':' '}
		table = [[lookup[self._getij(i,j)] for j in range(self.size)] for i in range(self.size)]
		string = "  "+' '.join([str(x%10) for x in range(self.size)])+'\n'
		string += "%s|"+"|\n%s|".join(['|'.join(x) for x in table])+'|'
		string = string%tuple([x%10 for x in range(self.size)])
		return string