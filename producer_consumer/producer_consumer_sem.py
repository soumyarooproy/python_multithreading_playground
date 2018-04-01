import collections
import time
import threading
import random
import itertools

def producer(prod_id):
    global payload
    while not quit:
        # Proceed to write to the buffer if the buffer is not full; block
        # otherwise
        not_full.acquire()

        # Critical Section
        with mutex:
            buff.append(payload)
            #print('Prod{} wrote'.format(prod_id), payload)
            payload += 1
            time.sleep(random.random()/1000)

        # Notify that the buffer is not empty anymore
        not_empty.release()

def consumer(cons_id):
    global prev_recv_payload
    while not quit:
        # Proceed to read from the buffer if the buffer is not empty; block
        # otherwise
        not_empty.acquire()

        # Critical Section
        with mutex:
            payload = buff.popleft()
            assert payload == prev_recv_payload + 1, 'prev_recv_payload = {}, payload = {}'.format(prev_recv_payload, payload)
            #print('Cons{}'.format(cons_id), payload, len(buff))
            prev_recv_payload = payload
            time.sleep(random.random()/1000)

        # Notify that the buffer is not full anymore
        not_full.release()

N = 20
buff = collections.deque()
not_full = threading.BoundedSemaphore(value=N)
not_empty = threading.BoundedSemaphore(value=N)
for i in range(N):
    not_empty.acquire()
mutex = threading.Lock()

NUM_PRODUCERS = 10
NUM_CONSUMERS = 10

payload = 0
prev_recv_payload = -1

consumers = [threading.Thread(target=consumer, args=(i,)) for i in range(NUM_CONSUMERS)]
producers = [threading.Thread(target=producer, args=(i,)) for i in range(NUM_PRODUCERS)]

quit = False
for t in itertools.chain(consumers, producers):
    t.start()

time.sleep(10)
quit = True

for t in itertools.chain(consumers, producers):
    t.join()

print('Test passed, last payload sent =', payload - 1, 'last payload received =', prev_recv_payload)

