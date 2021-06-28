#!/bin/python3
#victor.oliveira@gmx.com
import struct
import zlib
import sys

class PBPExtract:
    def __init__(self):
        self.pbp_name = name
        self.img_name = name.casefold().replace('pbp', 'img')
        self.pbp_file = open(self.pbp_name, 'rb')
        self.img_file = open(self.img_name, 'wb')

        #Getting the psar offset
        self.pbp_file.seek(36)
        self.psar_offset = struct.unpack('i', self.pbp_file.read(4))[0]

    def _isMultiDisk(self):
        self.pbp_file.seek(self.psar_offset)
        tmp = self.pbp_file.read(10)
        if b'PSTITLEIMG' in tmp:
            return True
        elif b'PSISOIMG' in tmp:
            return False
        else:
            raise ValueError('The PBP file is damaged')

    def _getImageIndexes(self, multidisk=False):
        if multidisk:
            pbp_file.seek(self.psar_offset + 512)
            self.iso_psar_offset = struct.unpack('iiii', pbp_file.read(16))
            for psar_offset in iso_psar_offset:
                self.pbp_file.seek(self.psar_offset + 16384)
                indexes = dict()
                for i in range(0, 32256):
                    offset, size = struct.unpack('ii', self.pbp_file.read(8))
                    self.pbp_file.read(24)
                    if offset or size:
                        indexes.update({offset : size})
                return indexes
            
        self.pbp_file.seek(self.psar_offset + 16384)
        indexes = dict()
        for i in range(0, 32256):
            offset, size = struct.unpack('ii', self.pbp_file.read(8))
            self.pbp_file.read(24)
            if offset or size:
                indexes.update({offset : size})
        return indexes

    def _writeBlocks(self, psar_offset, indexes):
        for index in indexes.items():
            offset = index[0]
            size = index[1]
            self.pbp_file.seek(psar_offset + 1048576 + offset)
            buffer = self.pbp_file.read(size)
            if size is not 37632:
                buffer = zlib.decompress(buffer, -15)
            self.img_file.write(buffer)

            
a = PBPExtract(sys.argv[1])
indexes = a._getImageIndexes()
a._writeBlocks(a.psar_offset, indexes)
