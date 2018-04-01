import threading
import time
import itertools

class ProducerConsumerTest:
    '''
    '''
    PAYLOAD = 'PAYLOAD'
    def __init__(self, sync_queue, num_payloads, num_producers=1, num_consumers=1,
                 delay_produce=0.001, delay_consume=0.001):
        self._sync_queue    = sync_queue
        self._num_payloads  = num_payloads
        self._num_producers = num_producers
        assert self._num_payloads % self._num_producers == 0, \
               f'Number of payloads ({self._num_payloads}) needs to be \
                 divisible by number of producers ({self._num_producers})'
        self._num_consumers = num_consumers
        self._delay_produce = delay_produce
        self._delay_consume = delay_consume

    def produce(self):
        for _ in range(self._num_payloads // self._num_producers):
            time.sleep(self._delay_produce)
            self._sync_queue.put(self.PAYLOAD)

    def consume(self):
        while True:
            item = self._sync_queue.get()
            if item is None:
                break
            time.sleep(self._delay_consume)

    def run(self):
        # Construct the producer and consumer threads
        producers = [threading.Thread(target=self.produce) for _ in range(self._num_producers)]
        consumers = [threading.Thread(target=self.consume) for _ in range(self._num_consumers)]

        start_time = time.time()
        # Start all the producer and consumer threads
        for t in itertools.chain(consumers, producers):
            t.start()

        # Wait for all the producers to finish
        for t in producers:
            t.join()

        # Send consumer termination payloads
        self._sync_queue.flush(self._num_producers)

        # Wait for all the consumers to finish
        for t in consumers:
            t.join()
        end_time = time.time()

        print(f'Test finished ({self._num_payloads} sent by {self._num_producers} '
              f'producers and received by {self._num_consumers} consumers in '
              f'{end_time - start_time} seconds)')

#class ProducerConsumerTestFifo(ProducerConsumerTest):
#    def produce(self):
#        while True:
#            time.sleep(self._consumption_delay)
#            self._sync_queue.put(self._index_payload)
#            with self._mutex:
#                if self._index_payload == num_payloads:
#                    return
#                self._index_payload += 1
#
#    def consume(self):
#        while True:
#            index_payload = self._sync_queue.get()
#
#    def run(self):
#        consu
