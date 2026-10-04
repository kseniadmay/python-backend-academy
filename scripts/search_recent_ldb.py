import os, glob

ldb_dir = r"C:\Users\fury6\AppData\Roaming\Opera Software\Opera Air Stable\Default\IndexedDB\https_www.remnote.com_0.indexeddb.leveldb"
files = sorted(glob.glob(os.path.join(ldb_dir, "*.ldb")) + glob.glob(os.path.join(ldb_dir, "*.log")), key=os.path.getmtime, reverse=True)

search_terms = ["Что такое срез", "frozenset – неизменяемая", "frozenset"]

for f in files[:15]:
    try:
        with open(f, "rb") as fp:
            data = fp.read()
            for st in search_terms:
                st_bytes = st.encode("utf-8")
                if st_bytes in data:
                    print(f"Found '{st}' in {os.path.basename(f)} (mtime={os.path.getmtime(f)})")
                    idx = 0
                    count = 0
                    while count < 3:
                        idx = data.find(st_bytes, idx)
                        if idx == -1:
                            break
                        chunk = data[max(0, idx - 150):min(len(data), idx + 250)]
                        try:
                            clean_snippet = chunk.decode("utf-8", errors="replace")
                            print("  Snippet:", clean_snippet)
                        except:
                            print("  Snippet (bytes):", repr(chunk))
                        idx += len(st_bytes)
                        count += 1
    except Exception as e:
        pass
