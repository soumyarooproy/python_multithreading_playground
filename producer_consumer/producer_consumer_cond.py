import collections
import time
import threading
import random
import itertools
import time

def producer(prod_id):
    global payload
    while payload <= MIN_PAYLOADS:
        # Simulate item production
        #time.sleep(random.random()/100)
        time.sleep(0.005)

        # Proceed to write to the buffer if the buffer is not full; block
        # otherwise
        with not_full:
            not_full.wait_for(lambda : len(buff) < N)

            # Enqueue item
            buff.append(payload)
            #print('Prod{}'.format(prod_id), payload, len(buff))
            payload += 1

        # Notify that the buffer is not empty anymore
        with not_empty:
            not_empty.notify()

    #print('Prod{}'.format(prod_id), 'finished.')

def consumer(cons_id):
    global prev_recv_payload
    while True:
        # Proceed to read from the buffer if the buffer is not empty; block
        # otherwise
        with not_empty:
            not_empty.wait_for(lambda : buff)

            # Dequeue item
            payload = buff.popleft()
            if not payload:
                #print('Cons{}'.format(cons_id), 'finished.')
                return
            assert payload == prev_recv_payload + 1, (
                   'prev_recv_payload = {}, payload = {}'.format(prev_recv_payload, payload))
            prev_recv_payload = payload
            if payload % 1000 == 0:
                print('Cons{}'.format(cons_id), payload, len(buff))
            #print('Cons{}'.format(cons_id), payload, len(buff))

        # Notify that the buffer is not full anymore
        with not_full:
            not_full.notify()

        # Simulate item consumption
        #time.sleep(random.random()/100)
        time.sleep(0.005)

N = 200
random.seed(0)
buff = collections.deque()
#lock = threading.Lock()
lock = None
not_full = threading.Condition(lock)
not_empty = threading.Condition(lock)

MIN_PAYLOADS  = 50000
NUM_PRODUCERS = 100
NUM_CONSUMERS = 100

payload = 1
prev_recv_payload = 0

consumers = [threading.Thread(target=consumer, args=(i, )) for i in range(NUM_CONSUMERS)]
producers = [threading.Thread(target=producer, args=(i, )) for i in range(NUM_PRODUCERS)]

start_time = time.time()
for t in itertools.chain(consumers, producers):
    t.start()

for t in producers:
    t.join()
print('Producers finished')

for _ in consumers:
    buff.append(None)
print('Send consumer terminating payloads')
with not_empty:
    not_empty.notify_all()

for t in consumers:
    t.join()
print('Consumers finished')

print('Test passed, last payload sent =', payload - 1, 'last payload received =', prev_recv_payload)
print("--- %s seconds ---" % (time.time() - start_time))

