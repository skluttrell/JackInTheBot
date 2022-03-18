import random, urllib3

URL = 'https://www.random.org/integers/?num=1&min=%i&max=%i&col=1&base=10&format=plain&rnd=new'
HTTP = urllib3.PoolManager()

def get_quota():
	"""Checks to see if random.org is available"""

	request = HTTP.request('GET', 'https://www.random.org/quota/?format=plain')
	if request.data is not None:
		if request.status == 200: return int(request.data.decode('utf-8'))
	return -1

def get_int(min: int=1, max: int=6) -> int:
	request = HTTP.request('GET', URL % (min, max))
	if request.status != 200:
		return random.randint(min, max)
	data = int(request.data.decode('utf-8'))
	return data

if __name__ == '__main__':
	roll = 'd%s: %i'
	for s in [6,8,10,12,20,100]:
		print(roll % (s, get_int(1, s)))