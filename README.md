# 🗂️ macOS `.DS_Store` Parser  
**Human-Readable `.DS_Store` Inspector for Linux / Windows / macOS**

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)  
![Python](https://img.shields.io/badge/Python-3.7%2B-yellow.svg)  
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-green.svg)  

This tool parses macOS `.DS_Store` files and prints Finder metadata in a **clean, readable format**.  
Useful for **DFIR**, **research**, **OSINT**, **reverse-engineering**, or simply understanding what macOS leaves behind.

---

## ✨ Features

| Feature | Description |
|--------|------------|
✅ Parse `.DS_Store` without a Mac |  
✅ Shows **true Finder keys** (`lg1S`, `ph1S`, `moDD`, `modD`) |  
✅ **Human-readable sizes** (KB/MB/GB) |  
✅ Detects several **Apple timestamp formats** |  
✅ Falls back to **hex blobs** when decoding isn't safe |  
✅ Works offline |  
✅ Linux / macOS / Windows compatible |

---

## 📦 Install

### Install Python Dependency
```bash
pip install ds-store
