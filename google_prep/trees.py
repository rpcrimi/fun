import numpy

class tree(object):
	def __init__(self, root, max_level):
		self.root = root
		self.max_level = max_level

	def depth_first(self, root):
		if root.leaves == []:
			print root.value
			return
		else:
			print root.value
			for leaf in root.leaves:
				self.depth_first(leaf)


	def breadth_first(self, root):
		for level range(self.max_level):
			print 

class node(object):
	def __init__(self, value, level, leaves):
		self.value = value
		self.level = level
		self.leaves = leaves

def main():
	lf = node("F", 2, [])
	le = node("E", 2, [])
	ld = node("D", 2, [])
	lc = node("C", 1, [le, lf])
	lb = node("B", 1, [ld])
	la = node("A", 0, [lb, lc])
	t = tree(la, 2)
	#t.depth_first(la)
	t.breadth_first(la)


if __name__ == "__main__":
	main()