from ds_store import DSStore
import sys, struct, datetime, string, re

UTC = datetime.timezone.utc
MAC_EPOCH_OFFSET = 978307200  # seconds between 1970-01-01 and 2001-01-01 (CFAbsoluteTime offset)

def is_printable_ascii(b: bytes) -> bool:
    return all(32 <= x < 127 for x in b)

def key_to_str(k):
    # Show 4-char codes like "lg1S", "moDD"; fall back to hex if weird
    if isinstance(k, str):
        return k
    if isinstance(k, (bytes, bytearray)):
        b = bytes(k)
        if len(b) == 4 and is_printable_ascii(b):
            return b.decode('ascii', 'ignore')
        return "[" + " ".join(f"{x:02x}" for x in b) + "]"
    return str(k)

def name_to_str(n):
    if isinstance(n, (bytes, bytearray)):
        for enc in ("utf-8", "latin-1"):
            try:
                return n.decode(enc, "ignore")
            except Exception:
                pass
        return "".join(chr(x) if 32 <= x < 127 else "?" for x in n)
    return str(n)

def human_size(n: int) -> str:
    units = ("bytes", "KB", "MB", "GB", "TB")
    f = float(n); i = 0
    while f >= 1024 and i < len(units)-1:
        f /= 1024.0; i += 1
    return f"{int(f)} {units[i]}" if units[i] == "bytes" else f"{f:.2f} {units[i]}"

def plausible(dt: datetime.datetime) -> bool:
    return datetime.datetime(1990,1,1,tzinfo=UTC) <= dt <= datetime.datetime(2100,1,1,tzinfo=UTC)

def try_decode_dates(raw: bytes):
    """Try several common encodings used in Apple metadata. Return ISO string or None."""
    if not isinstance(raw, (bytes, bytearray)):
        return None
    b = bytes(raw)

    # 1) CFAbsoluteTime (seconds since 2001-01-01), BE double
    if len(b) == 8:
        try:
            d = struct.unpack(">d", b)[0]
            # Ignore near-zero (often just cache placeholders)
            if d is not None and abs(d) > 3600:
                ts = d + MAC_EPOCH_OFFSET
                dt = datetime.datetime.fromtimestamp(ts, UTC)
                if plausible(dt):
                    return dt.isoformat() + "Z"
        except Exception:
            pass
        # 2) POSIX seconds since 1970, BE uint64
        try:
            s = struct.unpack(">Q", b)[0]
            dt = datetime.datetime.fromtimestamp(s, UTC)
            if plausible(dt):
                return dt.isoformat() + "Z"
        except Exception:
            pass

    # 3) POSIX/HFS+ 32-bit candidates
    if len(b) == 4:
        # a) POSIX 1970 epoch
        try:
            s = struct.unpack(">I", b)[0]
            dt = datetime.datetime.fromtimestamp(s, UTC)
            if plausible(dt):
                return dt.isoformat() + "Z"
        except Exception:
            pass
        # b) HFS Classic 1904 epoch (offset from 1970 to 1904 = 2082844800)
        try:
            s = struct.unpack(">I", b)[0] - 2082844800
            dt = datetime.datetime.fromtimestamp(s, UTC)
            if plausible(dt):
                return dt.isoformat() + "Z"
        except Exception:
            pass

    return None

def hex_bytes(b: bytes) -> str:
    return " ".join(f"{x:02x}" for x in b)

def get_fourcc(rec):
    """Return the real 4-char DS_Store key if available (e.g., lg1S/moDD), else best effort."""
    for attr in ("code", "key", "fourcc", "tag", "typ"):  # try common names across library variants
        if hasattr(rec, attr):
            return getattr(rec, attr)
    # Fallback: try to parse from repr like "<DSStoreEntry 'name' lg1S=...>"
    m = re.search(r"\s([A-Za-z0-9]{4})\s", repr(rec))
    return m.group(1) if m else getattr(rec, "type", b"")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pretty_dsstore.py <DS_Store path>")
        sys.exit(1)

    path = sys.argv[1]

    with DSStore.open(path) as ds:
        for rec in ds:
            name = name_to_str(getattr(rec, "filename", ""))
            raw_key = get_fourcc(rec)
            key = key_to_str(raw_key)
            val = rec.value

            left = f"{name:12} {key:4} "

            # Cached sizes
            if key in ("lg1S", "ph1S") and isinstance(val, int):
                print(left + f"{val} ({human_size(val)})")
                continue

            # Byte blobs (date-ish or opaque)
            if isinstance(val, (bytes, bytearray)):
                decoded = try_decode_dates(val)
                if decoded:
                    print(left + decoded)
                else:
                    print(left + "[" + hex_bytes(val) + "]")
                continue

            # Other values (strings/ints/etc.)
            print(left + str(val))

if __name__ == "__main__":
    main()
