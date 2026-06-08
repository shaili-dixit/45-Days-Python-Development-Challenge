"""
Binary Image Metadata Reader for JPEG and PNG Without External Libraries
Reads binary headers from JPEG/PNG to extract width, height, color depth, format.
"""

import os
import struct
import glob
from datetime import datetime


def read_png_metadata(filepath):
    """Parse PNG binary header: signature + IHDR chunk."""
    info = {'format': 'PNG', 'file': os.path.basename(filepath)}
    with open(filepath, 'rb') as f:
        sig = f.read(8)
        PNG_SIG = b'\x89PNG\r\n\x1a\n'
        if sig != PNG_SIG:
            raise ValueError("Not a valid PNG file")

        # IHDR chunk: 4 length + 4 type + 13 data
        length = struct.unpack('>I', f.read(4))[0]
        chunk_type = f.read(4)
        if chunk_type != b'IHDR':
            raise ValueError("Missing IHDR chunk")

        width  = struct.unpack('>I', f.read(4))[0]
        height = struct.unpack('>I', f.read(4))[0]
        bit_depth     = struct.unpack('B', f.read(1))[0]
        color_type    = struct.unpack('B', f.read(1))[0]
        compression   = struct.unpack('B', f.read(1))[0]
        filter_method = struct.unpack('B', f.read(1))[0]
        interlace     = struct.unpack('B', f.read(1))[0]

        color_types = {0: 'Grayscale', 2: 'RGB', 3: 'Indexed', 4: 'Grayscale+Alpha', 6: 'RGBA'}
        info.update({
            'width': width, 'height': height,
            'bit_depth': bit_depth,
            'color_type': color_types.get(color_type, f'Unknown({color_type})'),
            'compression': compression,
            'interlace': 'Adam7' if interlace else 'None',
        })
    return info


def read_jpeg_metadata(filepath):
    """Parse JPEG binary markers to extract dimensions and color info."""
    info = {'format': 'JPEG', 'file': os.path.basename(filepath)}
    with open(filepath, 'rb') as f:
        header = f.read(2)
        if header != b'\xff\xd8':
            raise ValueError("Not a valid JPEG file")

        while True:
            marker = f.read(2)
            if len(marker) < 2:
                break
            if marker[0] != 0xFF:
                break
            marker_type = marker[1]
            if marker_type == 0xD9:  # EOI
                break
            if marker_type in (0xC0, 0xC1, 0xC2):  # SOF markers
                f.read(2)  # length
                precision  = struct.unpack('B', f.read(1))[0]
                height     = struct.unpack('>H', f.read(2))[0]
                width      = struct.unpack('>H', f.read(2))[0]
                components = struct.unpack('B', f.read(1))[0]
                sof_types  = {0xC0: 'Baseline DCT', 0xC1: 'Extended Sequential', 0xC2: 'Progressive'}
                color_map  = {1: 'Grayscale', 3: 'YCbCr (RGB)', 4: 'CMYK'}
                info.update({
                    'width': width, 'height': height,
                    'bit_depth': precision,
                    'components': components,
                    'color_type': color_map.get(components, f'{components} components'),
                    'encoding': sof_types.get(marker_type, 'Unknown'),
                })
                break
            else:
                seg_len = struct.unpack('>H', f.read(2))[0]
                f.read(seg_len - 2)
    return info


def file_stats(filepath):
    stat = os.stat(filepath)
    return {
        'size_bytes': stat.st_size,
        'size_human': format_size(stat.st_size),
        'modified':   datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
    }


def format_size(b):
    for unit in ('B', 'KB', 'MB', 'GB'):
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"


def read_image_metadata(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    stats = file_stats(filepath)
    try:
        if ext == '.png':
            meta = read_png_metadata(filepath)
        elif ext in ('.jpg', '.jpeg'):
            meta = read_jpeg_metadata(filepath)
        else:
            return {'file': os.path.basename(filepath), 'error': f'Unsupported extension: {ext}'}
        return {**meta, **stats}
    except Exception as e:
        return {'file': os.path.basename(filepath), 'error': str(e), **stats}


def print_metadata(meta):
    print(f"\n  {'─'*55}")
    print(f"  File    : {meta.get('file','?')}")
    if 'error' in meta:
        print(f"  ⚠  Error: {meta['error']}")
    else:
        print(f"  Format  : {meta.get('format','?')}")
        print(f"  Size    : {meta.get('width','?')} × {meta.get('height','?')} px")
        print(f"  Bit Depth: {meta.get('bit_depth','?')} bpp")
        print(f"  Color   : {meta.get('color_type','?')}")
        for k in ('encoding', 'interlace', 'compression', 'components'):
            if k in meta:
                print(f"  {k.capitalize():<10}: {meta[k]}")
    print(f"  Filesize: {meta.get('size_human','?')}  ({meta.get('size_bytes','?')} bytes)")
    print(f"  Modified: {meta.get('modified','?')}")
    print(f"  {'─'*55}")


def create_minimal_png(path, width=64, height=64):
    """Create a minimal valid PNG (1x1 white pixel) for demo."""
    import zlib
    def chunk(name, data):
        c = name + data
        crc = struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack('>I', len(data)) + c + crc

    sig  = b'\x89PNG\r\n\x1a\n'
    ihdr = chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
    raw  = b'\x00\xff\xff\xff'
    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')

    with open(path, 'wb') as f:
        f.write(sig + ihdr + idat + iend)


def create_minimal_jpeg(path):
    """Write a minimal 1x1 white JPEG."""
    # Minimal JPEG bytes (1x1 white pixel)
    data = bytes([
        0xFF,0xD8,0xFF,0xE0,0x00,0x10,0x4A,0x46,0x49,0x46,0x00,0x01,0x01,0x00,
        0x00,0x01,0x00,0x01,0x00,0x00,0xFF,0xDB,0x00,0x43,0x00,0x08,0x06,0x06,
        0x07,0x06,0x05,0x08,0x07,0x07,0x07,0x09,0x09,0x08,0x0A,0x0C,0x14,0x0D,
        0x0C,0x0B,0x0B,0x0C,0x19,0x12,0x13,0x0F,0x14,0x1D,0x1A,0x1F,0x1E,0x1D,
        0x1A,0x1C,0x1C,0x20,0x24,0x2E,0x27,0x20,0x22,0x2C,0x23,0x1C,0x1C,0x28,
        0x37,0x29,0x2C,0x30,0x31,0x34,0x34,0x34,0x1F,0x27,0x39,0x3D,0x38,0x32,
        0x3C,0x2E,0x33,0x34,0x32,0xFF,0xC0,0x00,0x0B,0x08,0x00,0x01,0x00,0x01,
        0x01,0x01,0x11,0x00,0xFF,0xC4,0x00,0x1F,0x00,0x00,0x01,0x05,0x01,0x01,
        0x01,0x01,0x01,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x02,
        0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A,0x0B,0xFF,0xC4,0x00,0xB5,0x10,
        0x00,0x02,0x01,0x03,0x03,0x02,0x04,0x03,0x05,0x05,0x04,0x04,0x00,0x00,
        0x01,0x7D,0x01,0x02,0x03,0x00,0x04,0x11,0x05,0x12,0x21,0x31,0x41,0x06,
        0x13,0x51,0x61,0x07,0x22,0x71,0x14,0x32,0x81,0x91,0xA1,0x08,0x23,0x42,
        0xB1,0xC1,0x15,0x52,0xD1,0xF0,0x24,0x33,0x62,0x72,0x82,0xFF,0xDA,0x00,
        0x08,0x01,0x01,0x00,0x00,0x3F,0x00,0xFB,0xD5,0xFF,0xD9,
    ])
    with open(path, 'wb') as f:
        f.write(data)


def batch_process(folder):
    patterns = [os.path.join(folder, ext) for ext in ('*.png', '*.jpg', '*.jpeg')]
    files = []
    for p in patterns:
        files.extend(glob.glob(p))
    if not files:
        print(f"  No image files found in '{folder}'.")
        return
    print(f"\n  Batch processing {len(files)} image(s) in '{folder}':")
    for fp in files:
        meta = read_image_metadata(fp)
        print_metadata(meta)


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Binary Image Metadata Reader v1.0     ║")
    print("╚══════════════════════════════════════════╝")

    demo_dir = "demo_images"
    os.makedirs(demo_dir, exist_ok=True)

    png_path  = os.path.join(demo_dir, "sample.png")
    jpeg_path = os.path.join(demo_dir, "sample.jpg")

    create_minimal_png(png_path)
    create_minimal_jpeg(jpeg_path)

    print("\n  Reading individual files:")
    for path in [png_path, jpeg_path]:
        meta = read_image_metadata(path)
        print_metadata(meta)

    batch_process(demo_dir)

    user_path = input("\n  Enter path to an image file or folder (or Enter to skip): ").strip()
    if user_path:
        if os.path.isdir(user_path):
            batch_process(user_path)
        elif os.path.isfile(user_path):
            print_metadata(read_image_metadata(user_path))
        else:
            print("  Path not found.")

    import shutil; shutil.rmtree(demo_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
