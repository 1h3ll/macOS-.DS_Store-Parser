# 🗂️ macOS `.DS_Store` Parser  
**Human-Readable `.DS_Store` Inspector for Linux / Windows / macOS**

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)  
![Python](https://img.shields.io/badge/Python-3.7%2B-yellow.svg)  
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-green.svg)  

This tool parses macOS `.DS_Store` files and prints Finder metadata in a **clean, readable format**.  
Useful for **DFIR**, **research**, **OSINT**, **reverse-engineering**, or simply understanding what macOS leaves behind.

A small utility to print Apple `DS_Store` entries in a human-friendly form.

The script attempts to:

* Show 4-character resource keys (e.g. `lg1S`, `moDD`) when possible
* Decode common Apple timestamp encodings (CFAbsoluteTime, POSIX, HFS) and present ISO8601 datetimes in UTC
* Pretty-print binary blobs as hex when not recognized
* Show human-friendly sizes (KB/MB) for certain cached-size keys
* Handle both `bytes` and `str` filenames and keys gracefully

---

## Requirements

* Python 3.8+
* `ds_store` Python package (a library for parsing DS_Store files)

Install with pip:

```bash
pip install ds-store
```

(If your distribution has a package named differently, install the appropriate package.)

---

## Usage

```bash
python pretty_dsstore.py <path/to/DS_Store>
```

Example:

```bash
python pretty_dsstore.py ./DS_Store
```

Output looks like:

```
Icon        icVO  [00 00 00 00 ...]
.Spotlight  moDD  2023-07-09T12:34:56Z
myfile.txt  lg1S  2345 (2.29 KB)
```

---

## Notes & Behavior

* The script tries multiple encodings for timestamp-like 4- or 8-byte values:

  * 8-byte big-endian double interpreted as CFAbsoluteTime (seconds since 2001-01-01)
  * 8-byte big-endian unsigned integer interpreted as POSIX seconds since 1970
  * 4-byte big-endian unsigned integer interpreted as POSIX seconds
  * 4-byte big-endian unsigned integer interpreted as HFS (1904) epoch

* `plausible()` filters timestamps to a reasonable range (1990–2100) to avoid printing garbage values.

* Key detection: The script attempts to read several attribute names (`code`, `key`, `fourcc`, `tag`, `typ`) commonly present on DS_Store record objects returned by the `ds_store` library. If none are present it falls back to a regex on the `repr()` of the record.

---

## Potential Improvements

* Add unit tests for the `try_decode_dates()` and `get_fourcc()` helpers using canned byte sequences.
* Add CLI flags for more verbose output or JSON/CSV export for downstream processing.
* Allow reading from stdin or adding recursion for scanning directories for `DS_Store` files.
* Improve detection heuristics for other DS_Store value types (e.g., Finder flags, icon positions).

---

## License

Choose and add a license (MIT is a common, permissive choice).

---

If you want, I can also:

* generate a `requirements.txt`
* create unit tests for the decoding functions
* convert this into a small package with entry point
* add JSON output mode for machine consumption

Pick one and I'll do it next.
