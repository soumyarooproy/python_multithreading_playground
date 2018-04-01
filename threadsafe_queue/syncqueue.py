''' Reimplementation of a multi-producer, multi-consumer queue '''

import threading
from collections import deque

__all__ = ['SyncQueueCond', 'SyncQueueSem']

class SyncQueueBase:
    def __init__(self, maxsize=0):
        self._max_size = maxsize
        self._queue = deque()

    def put(self, item):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

class SyncQueueSem(SyncQueueBase):
    pass

class SyncQueueCond(SyncQueueBase):
    ''' Thread-safe FIFO queue implemented using conditions

    '''
    def __init__(self, maxsize=1):
        super().__init__(maxsize)
        self._p_mutex = threading.Lock()
        self._g_mutex = threading.Lock()
        self._not_full = threading.Condition(self._p_mutex)
        self._not_empty = threading.Condition(self._g_mutex)

    def flush(self, num_consumers):
        for _ in range(num_consumers):
            self.put(None)
        with self._not_empty:
            self._not_empty.notify_all()

    def put(self, item):
        ''' Put an item into the queue.

        '''
        # Proceed to enqueue item if the buffer is not full; block otherwise
        with self._not_full:
            self._not_full.wait_for(lambda : len(self._queue) < self._max_size)
            # Enqueue item
            self._queue.append(item)
        # Notify that the buffer is not empty anymore
        with self._not_empty:
            self._not_empty.notify()

    def get(self):
        ''' Get an item from the queue.

        '''
        # Proceed to dequeue item if the buffer is not empty; block otherwise
        with self._not_empty:
            self._not_empty.wait_for(lambda : len(self._queue))
            # Dequeue item
            item = self._queue.popleft()
        # Notify that the buffer is not full anymore
        with self._not_full:
            self._not_full.notify()
        return item
