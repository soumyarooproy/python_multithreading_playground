from reader_writer import ReaderWriterVer1, ReaderWriterVer2, ReaderWriterVer3

test1 = ReaderWriterVer1()
test2 = ReaderWriterVer2()

test1.run(num_transactions=100000,
          ratio_read_to_write=2000.0,
          num_readers=200,
          num_writers=100)

test2.run(num_transactions=100000,
          ratio_read_to_write=2000.0,
          num_readers=200,
          num_writers=100)

test1.run(num_transactions=100000,
          ratio_read_to_write=200.0,
          num_readers=200,
          num_writers=100)

test2.run(num_transactions=100000,
          ratio_read_to_write=200.0,
          num_readers=200,
          num_writers=100)

test1.run(num_transactions=100000,
          ratio_read_to_write=20.0,
          num_readers=200,
          num_writers=100)

test2.run(num_transactions=100000,
          ratio_read_to_write=20.0,
          num_readers=200,
          num_writers=100)

test1.run(num_transactions=100000,
          ratio_read_to_write=2.0,
          num_readers=200,
          num_writers=100)

test2.run(num_transactions=100000,
          ratio_read_to_write=2.0,
          num_readers=200,
          num_writers=100)

