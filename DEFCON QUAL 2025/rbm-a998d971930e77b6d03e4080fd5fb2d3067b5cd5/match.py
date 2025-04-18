import glob 
matched_files = []
# payload = NEd4Qzk1SUZBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUZJNTlDeEc0

for filename in glob.glob("output*.txt"):
    with open(filename, "rb") as f:
        content = f.read()
        if b"target: 6161616161616161" in content:
            matched_files.append(filename)

print("Matched files:")
for name in matched_files:
    print(name)
