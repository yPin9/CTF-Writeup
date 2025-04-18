from pwn import *
import subprocess

index = []
gdb_results = []

for i in range(200):  
    p = process("./rbm")
    p.sendlineafter(b"function index:", str(i).encode())

    print(f"Testing index: {i}")

    p.recvuntil(b"picked ")
    picked_raw = p.recvline().strip()  # e.g., b'7ffd1757aa40'

    try:
        picked_addr = int(picked_raw, 16)
        picked_hex = hex(picked_addr)
    except ValueError:
        print(f"[!] Could not parse picked value: {picked_raw}")
        picked_hex = "invalid"
        p.close()
        continue

    index.append(picked_hex)
    print(f"[+] Got picked address: {picked_hex}")

    # 利用 GDB 執行 `x/gx <picked_hex>`，並把輸出讀出來
    gdb_cmds = f"""
    set pagination off
    attach {p.pid}
    x/gx {picked_hex}
    detach
    quit
    """

    # 用 subprocess 呼叫 GDB，執行上面的指令
    result = subprocess.run(['gdb', '-q'], input=gdb_cmds.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    gdb_output = result.stdout.decode()

    for line in gdb_output.splitlines():
        # 濾掉 gef prompt 等干擾資訊
        if picked_hex in line and ':' in line:
            try:
                value = line.split(':')[1].strip().split()[0]
                gdb_results.append(value)
                print(f"[GDB] {picked_hex} → {value}")
            except Exception as e:
                print(f"[!] Failed to parse line: {line} ({e})")
                gdb_results.append("N/A")
            break
    else:
        gdb_results.append("N/A")
        print("[GDB] No matching output found")


    p.close()

print("\nAll picked values:")
print(index)

print("\nAll x/gx results:")
print(gdb_results)
