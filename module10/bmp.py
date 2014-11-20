def write_greyscale(filename, pixels):
    # each pixel is a value from 0 to 255
    height = len(pixels)
    width = len(pixels[0])

    with open(filename, 'wb') as bmp:
        # BMP header
        bmp.write(b'BM')

        size_bookmark = bmp.tell()     # the next four bytes hold the 32-bit integer filesize
        bmp.write(b'\x00\x00\x00\x00') # as a little-endian integer, put placeholders for now

        bmp.write(b'\x00\x00') # unused 16-bit integer
        bmp.write(b'\x00\x00') # unused 16-bit integer

        pixel_offset_bookmark = bmp.tell() # again 4 bytes
        bmp.write(b'\x00\x00\x00\x00')

        # Image header
        # First, write a length of the image header as a 32-bit integer
        bmp.write(b'\x28\x00\x00\x00') # remember - little-endian
        bmp.write(_int32_to_bytes(width))
        bmp.write(_int32_to_bytes(height))

        # this is fixed for greyscale
        bmp.write(b'\x01\x00') # number of image planes
        bmp.write(b'\x08\x00') # 8 bits per pixel for greyscale
        bmp.write(b'\x00\x00\x00\x00') # no compression
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')
        bmp.write(b'\x00\x00\x00\x00')

        # that was 40 bytes total, as promised!

        # color pallette - a linear grayscale
        for c in range(256):
            bmp.write(bytes((c, c, c, c, 0)))

        # pixel data
        pixel_data_bookmark = bmp.tell()
        for row in reversed(pixels): # BMP files are bottom to top
            row_data = bytes(row)
            bmp.write(row_data)
            padding = b'\x00' * (4 - (len(row) % 4))
            bmp.write(padding)

        # end of file
        eof_bookmark = bmp.tell()

        # fulfill promises
        bmp.seek(size_bookmark)
        bmp.write(_int32_to_bytes(eof_bookmark))

        bmp.seek(pixel_offset_bookmark)
        bmp.write(_int32_to_bytes(pixel_data_bookmark))


def _int32_to_bytes(i):
    return bytes((i & 0xff,
                  i >> 8 & 0xff,
                  i >> 16 & 0xff,
                  i >> 24 & 0xff))
