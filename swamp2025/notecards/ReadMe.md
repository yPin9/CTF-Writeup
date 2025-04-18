# Notecard

賽後覆盤，其實也算簡單的 heap 題，只是我不知道該怎麼覆寫

他的邏輯是這樣去要4塊 chunk，chunk1~chunk4，然後把 chunk 的地址放在一個陣列裡(chunk5)，然後這個陣列有 OOB

Memory layout 長下面這樣

|           |      0x8       |      0x8       |
| --------- |:--------------:|:--------------:|
| chunk1--> |     header     |   chunk size   |
| chunk1--> |      data      |      data      |
| chunk2--> |     header     |   chunk size   |
| chunk2--> |      data      |      data      |
| chunk3--> |     header     |   chunk size   |
| chunk3--> |      data      |      data      |
| chunk4--> |     header     |   chunk size   |
| chunk4--> |      data      |      data      |
| chunk5--> |     header     |   chunk size   |
| chunk5--> | chunk1 address | chunk2 address |
| chunk5--> | chunk3 address | chunk4 address |


chunk5 就是存在 oob 的陣列，我們把前面的 chunk 改成 GOT 表，就操作 GOT hijack 常規操作，然後再 call 就 get shell 了