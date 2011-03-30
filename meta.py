
class Person(object):
	def name(self):
		raise NotImplementedError

class TwitterPerson(Person):
	def twitterHandle(self):
		return self.twitterhandle
	
class FacebookPerson(Person):
	def phone(self):
		return '111-111-1111'
	
class GTalkPerson(Person):
	def phone(self):
		return '222-222-2222'
	
class MetaMerge(object):
	def __init__(self, cls, instances):
		self.cls = cls
		self.instances = instances
		
	def get(self, prop, args):
		l = []
		for i in self.instances:
			if hasattr(i, prop):
				l.append((getattr(i, prop)(*args), i))
		return l
	
	def __getattr__(self, prop):
		return lambda *args: self.get(prop, args)

t = TwitterPerson()
f = FacebookPerson()
g = GTalkPerson()

m = MetaMerge(Person, [t,f,g])
print m.phone()
