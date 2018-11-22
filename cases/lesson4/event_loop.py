from threading import Thread
import time

from Queue import Queue

q = Queue()


class event_loop(Thread):
	def __init__(self):
		super(event_loop, self).__init__()

	def run(self):
		count = 0
		for i in range(6):
			global q
			q.put(count)
			time.sleep(1)
			count += 1
		q.put('exit')

def main():
	e = event_loop()
	e.start()
	while True:
		if not q.empty():
			value = q.get()
			if value == 'exit':
				break
			else:
				print value

main()

