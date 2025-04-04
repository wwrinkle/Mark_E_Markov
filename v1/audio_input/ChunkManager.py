import numpy
from datetime import datetime
from core.const import BUFFER_SIZE, NUMPY_DATA_TYPE
from queue import Queue


class ChunkManager(object):

    def __init__(self):
        self.chunks = Queue(maxsize=BUFFER_SIZE)

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ChunkManager, cls).__new__(cls)
        return cls.instance

    def append_chunk(self, chunk):
        # print("appending chunk")
        chunk_array = numpy.frombuffer(chunk, dtype=NUMPY_DATA_TYPE)
        self.chunks.put([datetime.now(), chunk_array])
