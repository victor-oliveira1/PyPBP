#!/bin/python3
import struct
import zlib

##typedef struct {
##	int offset;
##	int length;
##} INDEX;

##typedef struct {
##	HWND callback;
##	char srcPBP[0xFF];
##  char dstISO[0xFF];
##} ExtractIsoInfo;

MAX_INDEXES = 0x7E00
HEADER_PSAR_OFFSET = 0x24
PSAR_INDEX_OFFSET = 0x4000
PSAR_ISO_OFFSET = 0x100000
ISO_BLOCK_SIZE = 0x930
SEEK_SET = 0

psar_offset = 0
this_offset = 0
count = 0
offset = 0
length = 0
dummy = 6

pbpFileName = 'EBOOT.PBP'
isoFileName = 'IMAGE.IMG'
pbp_stream = open(pbpFileName, 'rb')
iso_stream = open(isoFileName, 'wb')
pbp_stream.seek(HEADER_PSAR_OFFSET)
psar_offset = struct.unpack('i', pbp_stream.read(4))[0]
this_offset = pbp_stream.seek(psar_offset + PSAR_INDEX_OFFSET)

count = 0
count_list = list()
iso_offset = list()
iso_length = list()

while this_offset < (psar_offset + PSAR_ISO_OFFSET):
    offset = struct.unpack('i', pbp_stream.read(4))[0]
    length = struct.unpack('i', pbp_stream.read(4))[0]
    dummy = pbp_stream.read(4 * 6)

    this_offset = pbp_stream.tell()

    if offset is not 0 or length is not 0:
        iso_offset.append(offset)
        iso_length.append(length)
        count += 1
        if count >= MAX_INDEXES:
            exit()

for i in range(0, count):
	this_offset = psar_offset + PSAR_ISO_OFFSET + iso_offset[i]
	pbp_stream.seek(this_offset)
	if iso_length[i] == 16 * ISO_BLOCK_SIZE:
		buffer = pbp_stream.read(iso_length[i])
		iso_stream.write(buffer)
	else:
		buffer = pbp_stream.read(iso_length[i])
		buffer_decoded = zlib.decompress(buffer, -15)
		iso_stream.write(buffer_decoded)
