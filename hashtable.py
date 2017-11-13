class HashTable(object):
	def __init__(self, size):
		self.size = size
		self.load_factor = 0
		self._table = [[-1, -1] for _ in range(size)]
		self._hashfunction = lambda x : x
		
	def insert(self, key:int, value:int):
		hashadr = self._hashfunction(key)
		self._table[hashadr][0] = key
		self._table[hashadr][1] = value
		
	def delete(self, key):
		hashadr = self._hashfunction(key)
		self._table[hashadr][0] = -1
		self._table[hashadr][1] = -1
		
	def search(self, key):
		hashadr = self._hashfunction(key)
		return self._table[hashadr][1]
		
	def prettyprint(self):
		for i in range(self.size):
			obj = self._table[i]
			print("{:^2}: ({:^3}, {:^3})".format(i, obj[0], obj[1]))

ht = HashTable(10)
ht.insert(1, 10)
ht.insert(3, 5)
print(ht.search(3))
ht.delete(3)
print(ht.search(3))
ht.prettyprint()
