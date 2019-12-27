"""Provides minimal ISO Base Media File Format parsing capability.

Just enough to find media creation date and time.
"""

import struct
import collections
from datetime import datetime
from exifread import ExifHeader

EPOCH_ADJUSTER = 2082844800


class Box:
    def __init__(self, source, size, type, offset, uuid):
        self.source = source
        self.size = size
        self.type = type
        self.offset = offset
        self.uuid = uuid
        self.remaining = size - offset

    def read(self, size):
        read = self.source.read(size)
        self.offset = self.offset + len(read)
        self.remaining = self.remaining - len(read)
        return read

    def __repr__(self):
        return "Box(size={}, type={}, offset={}, uuid={}, remaining={})".\
            format(self.size, self.type, self.offset,
                   self.uuid, self.remaining)


FullBox = collections.namedtuple('FullBox', 'box version flags')
HandlerBox = collections.namedtuple(
    'HandlerBox', 'full_box pre_defined handler_type reserved name')
MetaBox = collections.namedtuple(
    'MetaBox', 'full_box handler_box other_boxes item_infos locations')
ItemInfoEntry = collections.namedtuple(
    'ItemInfoEntry', 'item_id item_type item_name')
ItemOffset = collections.namedtuple(
    'ItemLocation', 'base_offset extent_offset extent_length')
ItemLocation = collections.namedtuple('ItemLocation', 'item_id offsets')
MovieHeaderBox = collections.namedtuple(
    'MovieHeaderBox', 'full_box creation_time modification_time timescale duration creation_date modification_date')


def get64(source):
    return struct.unpack(">Q", source.read(8))[0]


def get32(source):
    return struct.unpack(">I", source.read(4))[0]


def get16(source):
    return struct.unpack(">H", source.read(2))[0]


def getString(source):
    res = bytearray()
    while 1:
        c = source.read(1)[0]
        if c == 0:
            break
        res.append(c)
    return res


def parse_box(source):
    uuid = None
    box_header = source.read(8)
    offset = 8
    if len(box_header) == 0:
        # Reached end of file
        return None
    box_size = struct.unpack(">I", box_header[0:4])[0]
    box_type = box_header[4:8]
    if box_size == 0:
        # Extends to the end of file
        box_size = 0  # FIXME: Calculate size
    elif box_size == 1:
        box_size = get64(source)
        offset = offset + 8
    if box_type == b'uuid':
        uuid = source.read(16)
        offset = offset + 16
    return Box(source=source, size=box_size,
               type=box_type, offset=offset, uuid=uuid)


def parse_full_box(box):
    full_box = box.read(4)
    return FullBox(box=box, version=full_box[0], flags=full_box[1:4])


def parse_handler_box(full_box):
    handler = full_box.box.read(20)
    pre_defined = struct.unpack(">I", handler[0:4])[0]
    if pre_defined != 0:
        # Unexpected predefined value
        return None
    handler_type = handler[4:8]
    reserved = struct.unpack(">III", handler[8:20])
    name = full_box.box.read(full_box.box.remaining)
    return HandlerBox(full_box=full_box, pre_defined=pre_defined,
                      handler_type=handler_type, reserved=reserved, name=name)


def parse_item_info_entry(full_box):
    if full_box.version == 0 or full_box.version == 1:
        full_box.box.read(4)
        item_name = getString(full_box.box)
        content_type = getString(full_box.box)
        content_encoding = getString(full_box.box)
    if full_box.version == 1:
        # Ignoring for now...
        return None
    if full_box.version >= 2:
        if full_box.version == 2:
            item_id = get16(full_box.box)
        elif full_box.version == 3:
            item_id = get32(full_box.box)
        item = full_box.box.read(6)
        item_type = item[2:6]
        item_name = getString(full_box.box)
        if item_type == b'mime':
            content_type = getString(full_box.box)
            if full_box.box.remaining > 0:
                content_encoding = getString(full_box.box)
        elif item_type == b'uri ':
            item_uri_type = getString(full_box.box)
    return ItemInfoEntry(item_id=item_id, item_type=item_type,
                         item_name=item_name)


def read_item_info_entry(source):
    box = parse_box(source)
    if box.type != b'infe':
        # Expected ItemInfoEntry block
        return None
    full_box = parse_full_box(box)
    return parse_item_info_entry(full_box)


def read_handler_box(source):
    box = parse_box(source)
    if box.type != b'hdlr':
        # Expected Handler block
        return None
    full_box = parse_full_box(box)
    if full_box.version != 0:
        # Unexpected version for handler
        return None
    handler_box = parse_handler_box(full_box)
    return handler_box


def parse_item_location_box(full_box):
    locations = {}
    data = full_box.box.read(2)
    offset_size = data[0] & 0x0F
    length_size = (data[0] >> 4) & 0x0F
    base_offset_size = data[1] & 0x0F
    if full_box.version == 1 or full_box.version == 2:
        index_size = (data[1] >> 4) & 0x0F
    else:
        reserved = (data[1] >> 4) & 0x0F
    if full_box.version < 2:
        item_count = get16(full_box.box)
    elif full_box.version == 2:
        item_count = get32(full_box.box)
    for i in range(0, item_count):
        if full_box.version < 2:
            item_id = get16(full_box.box)
        elif full_box.version == 2:
            item_id = get32(full_box.box)
        if full_box.version == 1 or full_box.version == 2:
            full_box.box.read(2)
        data_reference_index = full_box.box.read(2)
        if base_offset_size == 2:
            base_offset = get16(full_box.box)
        elif base_offset_size == 4:
            base_offset =  get32(full_box.box)
        else:
            base_offset = 0
        extent_count = get16(full_box.box)
        offsets = []
        for j in range(0, extent_count):
            if (full_box.version == 1 or full_box.version == 2) and index_size > 0:
                extent_index = full_box.box.read(index_size)
            if offset_size == 2:
                extent_offset = get16(full_box.box)
            elif offset_size == 4:
                extent_offset = get32(full_box.box)
            if length_size == 2:
                extent_length = get16(full_box.box)
            elif length_size == 4:
                extent_length = get32(full_box.box)
            offsets.append(ItemOffset(base_offset=base_offset,
                                      extent_offset=extent_offset,
                                      extent_length=extent_length))
        locations[item_id] = ItemLocation(item_id=item_id, offsets=offsets)
    return locations


def parse_item_info_box(full_box):
    if full_box.version == 0:
        entry_count = get16(full_box.box)
    else:
        entry_count = get32(full_box.box)
    item_infos = {}
    while full_box.box.remaining > 0:
        item = read_item_info_entry(full_box.box)
        item_infos[item.item_id] = item
    return item_infos


def find_meta_box(media_file):
    # search for meta item
    while 1:
        box = parse_box(media_file)
        if box is None:
            # Reached end of file
            return None
        if box.type == b'meta':
            # Found top level meta
            break
        media_file.seek(box.size - box.offset, 1)
    full_box = parse_full_box(box)
    if full_box.version != 0 or full_box.flags != b'\x00\x00\x00':
        # Unexpected version for meta
        return None
    handler_box = read_handler_box(box)
    if handler_box.handler_type != b'pict':
        # Expecting pict handler
        return None
    other_boxes = []
    item_infos = []
    locations = []
    while box.remaining > 0:
        other_box = parse_box(box)
        if other_box.type == b'iinf':
            full_other_box = parse_full_box(other_box)
            item_infos = parse_item_info_box(full_other_box)
        if other_box.type == b'iloc':
            full_other_box = parse_full_box(other_box)
            locations = parse_item_location_box(full_other_box)
        other_box.read(other_box.remaining)
        other_boxes.append(other_box)
    return MetaBox(full_box=full_box, handler_box=handler_box,
                   other_boxes=other_boxes, item_infos=item_infos,
                   locations=locations)


def wrap_exifread(media_file, endian, offset,
                  fake_exif=0,
                  strict=False,
                  debug=False,
                  details=True,
                  stop_tag='UNDEF'):
    """
    Workaround until new exifread version with HEIC support is released
    See https://github.com/ianare/exif-py
    """
    hdr = ExifHeader(media_file, endian, offset, fake_exif,
                     strict, debug, details)
    ifd_list = hdr.list_ifd()
    thumb_ifd = False
    ctr = 0
    for ifd in ifd_list:
        if ctr == 0:
            ifd_name = 'Image'
        elif ctr == 1:
            ifd_name = 'Thumbnail'
            thumb_ifd = ifd
        else:
            ifd_name = 'IFD %d' % ctr
        hdr.dump_ifd(ifd, ifd_name, stop_tag=stop_tag)
        ctr += 1
    # EXIF IFD
    exif_off = hdr.tags.get('Image ExifOffset')
    if exif_off:
        hdr.dump_ifd(exif_off.values[0], 'EXIF', stop_tag=stop_tag)

    # deal with MakerNote contained in EXIF IFD
    # (Some apps use MakerNote tags but do not use a format for which we
    # have a description, do not process these).
    if details and 'EXIF MakerNote' in hdr.tags and 'Image Make' in hdr.tags:
        hdr.decode_maker_note()

    # extract thumbnails
    if details and thumb_ifd:
        hdr.extract_tiff_thumbnail(thumb_ifd)
        hdr.extract_jpeg_thumbnail()

    return hdr.tags


def process_heic(path):
    with open(path, 'rb') as media_file:
        meta_box = find_meta_box(media_file)
        [exif_info] = [i for i in meta_box.item_infos.values() if i.item_type == b'Exif']
        exif_location = meta_box.locations[exif_info.item_id]
        media_file.seek(media_file.seek(
            exif_location.offsets[0].extent_offset, 0))
        header_size = get32(media_file)
        if media_file.read(header_size)[0:4] != b'Exif':
            # Expecting Exif header
            return None
        offset = media_file.tell()
        endian = media_file.read(1)[0]
        tags = wrap_exifread(media_file, endian, offset)
    return tags


def parse_movie_header_box(full_box):
    if full_box.version == 1:
        creation_time = get64(full_box.box)
        modification_time = get64(full_box.box)
        timescale = get64(full_box.box)
        duration = get64(full_box.box)
    elif full_box.version == 0:
        creation_time = get32(full_box.box)
        modification_time = get32(full_box.box)
        timescale = get32(full_box.box)
        duration = get32(full_box.box)
    full_box.box.read(full_box.box.remaining)
    creation_date = str(datetime.fromtimestamp(creation_time - EPOCH_ADJUSTER))
    modification_date = str(datetime.fromtimestamp(modification_time - EPOCH_ADJUSTER))
    return MovieHeaderBox(full_box=full_box, creation_time=creation_time,
                          modification_time=modification_time,
                          creation_date=creation_date, modification_date=modification_date,
                          timescale=timescale, duration=duration)


def read_mvhd(source):
    box = parse_box(source)
    if box.type != b'mvhd':
        # Expecting mvhd handler
        return None
    full_box = parse_full_box(box)
    return parse_movie_header_box(full_box)


def process_mpeg(path):
    with open(path, 'rb') as media_file:
        # search for meta item
        while 1:
            box = parse_box(media_file)
            if box is None:
                # Reached end of file
                return None
            if box.type == b'moov':
                # Found top level meta
                break
            media_file.seek(box.size - box.offset, 1)
        return read_mvhd(box)
