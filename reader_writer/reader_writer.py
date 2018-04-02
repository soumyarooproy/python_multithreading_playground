import time
import threading
import itertools
import statistics

class ReaderWriterVer1():
    '''Reader Writer Problem - Version I

    Correctness Constraints:
    1. Readers can access shared data when there are no writers
    2. Writers can access shared data when there are no readers or writers
    3. Only one thread modifies the state variables at a time
    '''

    def __init__(self, delay_read=0.001, delay_write=0.002):
        self._shared_data = 0
        self._delay_read  = delay_read
        self._delay_write = delay_write

        # State variables
        self._readers_active  = 0
        self._readers_waiting = 0
        self._writers_active  = 0
        self._writers_waiting = 0

        self._mutex     = threading.Lock()
        self._can_read  = threading.Condition(self._mutex)
        self._can_write = threading.Condition(self._mutex)

    def _checkin_to_read(self):
        while self._writers_active > 0:
            self._readers_waiting += 1
            self._can_read.wait()
            self._readers_waiting -= 1
        self._readers_active += 1

    def _checkout_after_read(self):
        self._readers_active -= 1
        if self._readers_active == 0 and self._writers_waiting > 0:
            self._can_write.notify()

    def _checkin_to_write(self):
        while self._writers_active + self._readers_active > 0:
            self._writers_waiting += 1
            self._can_write.wait()
            self._writers_waiting -= 1
        self._writers_active += 1

    def _checkout_after_write(self):
        self._writers_active -= 1
        if self._readers_waiting > 0:
            self._can_read.notify_all()
        elif self._writers_waiting > 0:
            self._can_write.notify()

    def read(self):
        # Check-in         - wait until no writers
        with self._mutex:
            self._checkin_to_read()

        # Read the shared data - non-critical section among readers
        data = self._shared_data
        time.sleep(self._delay_read)

        # Check-out        - wake up a waiting writer
        with self._mutex:
            self._checkout_after_read()

    def write(self):
        # Check-in         - wait until no writers or readers
        with self._mutex:
            self._checkin_to_write()

        # Critical Section - modify the shared data
        self._shared_data += 1
        time.sleep(self._delay_write)

        # Check-out        - wake up a waiting writer or reader
        with self._mutex:
            self._checkout_after_write()

    def run(self, *, num_transactions, ratio_read_to_write=10.0, num_readers=1, num_writers=1):

        def reader(id_reader, num_reads):
            for i in range(num_reads):
                start_time = time.time()
                self.read()
                reader_wait_times[id_reader][i] = time.time() - start_time

        def writer(id_writer, num_writes):
            for i in range(num_writes):
                start_time = time.time()
                self.write()
                writer_wait_times[id_writer][i] = time.time() - start_time

        # Compute the number of reads and writes to simulate
        est_num_writes = int(1 / (ratio_read_to_write + 1) * num_transactions)
        est_num_reads  = num_transactions - est_num_writes
        num_reads_per_reader  = est_num_reads // num_readers
        num_writes_per_writer = max(1, est_num_writes // num_writers)

        # Set up to collect stats (waiting times for the transactions)
        reader_wait_times = [[0.0] * num_reads_per_reader  for _ in range(num_readers)]
        writer_wait_times = [[0.0] * num_writes_per_writer for _ in range(num_writers)]

        # Initialize shared data (a counter)
        self._shared_data = 0

        # Run the reader and writer threads
        readers = [threading.Thread(target=reader, args=(i, num_reads_per_reader))  for i in range(num_readers)]
        writers = [threading.Thread(target=writer, args=(i, num_writes_per_writer)) for i in range(num_writers)]
        start_time = time.time()
        for t in itertools.chain(readers, writers):
            t.start()
        for t in itertools.chain(readers, writers):
            t.join()
        end_time = time.time()

        # Sanity check:
        #     Since each write increments the shared data (a counter) by 1,
        #     the final value of the shared data should be the same as the
        #     number of writes
        assert self._shared_data == num_writers * num_writes_per_writer, \
               f'shared_data ({self._shared_data}) != num_writes ' \
               f'({num_writers * num_writes_per_writer})'

        # Compute waiting times for all the transactions
        mean_wait_read = statistics.mean(itertools.chain.from_iterable(reader_wait_times))
        mean_wait_write = statistics.mean(itertools.chain.from_iterable(writer_wait_times))
        max_wait_read = max(itertools.chain.from_iterable(reader_wait_times))
        max_wait_write = max(itertools.chain.from_iterable(writer_wait_times))

        # Print report
        print(f'Test finished in {end_time - start_time:.{3}} s: ' \
              f'{num_readers * num_reads_per_reader} reads ' \
              f'and {num_writers * num_writes_per_writer} writes ' \
              f'by {num_readers} readers and {num_writers} writers; ' \
              f'read wait time: {1000 * mean_wait_read:.{5}} ms (avg), ' \
              f'{1000 * max_wait_read:.{5}} ms (max), ' \
              f'write wait time: {1000 * mean_wait_write:.{5}} ms (avg), ' \
              f'{1000 * max_wait_write:.{5}} ms (max)' \
              )

class ReaderWriterVer2(ReaderWriterVer1):
    '''Reader Writer Problem - Version II

    Variant of ReaderWriter where writers are given priority over readers
    '''
    def _checkin_to_read(self):
        while self._writers_active + self._writers_waiting > 0:
            self._readers_waiting += 1
            self._can_read.wait()
            self._readers_waiting -= 1
        self._readers_active += 1

    def _checkout_after_read(self):
        self._readers_active -= 1
        if self._readers_active == 0 and self._writers_waiting > 0:
            self._can_write.notify()

    def _checkin_to_write(self):
        while self._writers_active + self._readers_active > 0:
            self._writers_waiting += 1
            self._can_write.wait()
            self._writers_waiting -= 1
        self._writers_active += 1

    def _checkout_after_write(self):
        self._writers_active -= 1
        if self._writers_waiting > 0:
            self._can_write.notify()
        elif self._readers_waiting > 0:
            self._can_read.notify_all()

class ReaderWriterVer3(ReaderWriterVer1):
    '''Reader Writer Problem - Version III

    Variant of ReaderWriter where fairness is maintained for both readers
    and writers
    '''
    def _checkin_to_read(self):
        raise NotImplementedError()

    def _checkout_after_read(self):
        raise NotImplementedError()

    def _checkin_to_write(self):
        raise NotImplementedError()

    def _checkout_after_write(self):
        raise NotImplementedError()

