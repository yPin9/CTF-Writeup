from pwn import *
import base64
import concurrent.futures

raw_payload = b'a' * 1500
payload = base64.b64encode(raw_payload)

def interact_with_binary(i):
    try:
        p = process("./rbm")
        p.sendlineafter(b"function index:", str(i).encode())
        p.sendlineafter(b"base64'd input:", payload)

        output = p.recvall(timeout=2)
        p.close()

        with open(f"output_{i}.txt", "wb") as f:
            f.write(output)
    except Exception as e:
        print(f"[!] Error on index {i}: {e}")

# 建立 ThreadPool
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(interact_with_binary, i) for i in range(1999)]

    # 等待全部完成
    concurrent.futures.wait(futures)
