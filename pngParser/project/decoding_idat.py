import zlib

def PaethPredictor(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        Pr = a
    elif pb <= pc:
        Pr = b
    else:
        Pr = c
    return Pr


def Recon_a(Recon, r, c, stride, bytesPerPixel):
    return Recon[r * stride + c - bytesPerPixel] if c >= bytesPerPixel else 0


def Recon_b(Recon, r, c, stride, bytesPerPixel):
    return Recon[(r - 1) * stride + c] if r > 0 else 0


def Recon_c(Recon, r, c, stride, bytesPerPixel):
    return Recon[(r - 1) * stride + c - bytesPerPixel] if r > 0 and c >= bytesPerPixel else 0


def decode_idat_chunk(data, width, height, bytesPerPixel):
    data = "".join(data)
    data = bytes.fromhex(data)
    data = zlib.decompress(data)

    stride = width * bytesPerPixel
    Recon = []

    i = 0
    for r in range(height):  # for each scanline
        filter_type = data[i]  # first byte of scanline is filter type
        i += 1
        for c in range(stride):  # for each byte in scanline
            Filt_x = data[i]
            i += 1
            if filter_type == 0:  # None
                Recon_x = Filt_x
            elif filter_type == 1:  # Sub
                Recon_x = Filt_x + Recon_a(Recon, r, c, stride, bytesPerPixel)
            elif filter_type == 2:  # Up
                Recon_x = Filt_x + Recon_b(Recon, r, c, stride, bytesPerPixel)
            elif filter_type == 3:  # Average
                Recon_x = Filt_x + (Recon_a(Recon, r, c, stride, bytesPerPixel)
                                    + Recon_b(Recon, r, c, stride, bytesPerPixel)) // 2
            elif filter_type == 4:  # Paeth
                Recon_x = Filt_x + PaethPredictor(Recon_a(Recon, r, c, stride, bytesPerPixel),
                                                  Recon_b(Recon, r, c, stride, bytesPerPixel),
                                                  Recon_c(Recon, r, c, stride, bytesPerPixel))
            else:
                raise Exception('unknown filter type: ' + str(filter_type))
            Recon.append(Recon_x & 0xff)  # truncation to byte

    return Recon