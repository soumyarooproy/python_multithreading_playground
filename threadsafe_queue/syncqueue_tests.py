from syncqueue import SyncQueueCond
from syncqueue_test import ProducerConsumerTest

test1 = ProducerConsumerTest(SyncQueueCond(20), 1000)
test1.run()

test2 = ProducerConsumerTest(SyncQueueCond(20), 100000, 100, 100)
test2.perf()

