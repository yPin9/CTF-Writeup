# Rainbow Mountain
* user 可以輸入兩次，第一次選擇 function 
* binary 提供 2000 個 function 供 user invoke
* user 可以輸入兩次，第一次選擇 function 
* 第二次輸入是調用這個 function 的參數
* 然後這個調用的方式它寫的很醜= =，逆了一陣子才知道他就是單純調用，它裡面塞了一些沒用的 function(function 的功能就是返回帶進去的參數)
* 每個 function 的功能其實就是比對 stack 中的某兩個 8bytes 的值是否一樣
* 然後某些 function 有 overflow 0~4 bytes，這是人工 fuzz 出來的
* 所以我就弄了一個 script，對每個 function 塞 1500 個 `A` (這邊很幸運，因為 1500 個 A 是迴文，他其實有個判斷檢查 input 是不是迴文)
* 發現其中 1576 可以 overflow 8 個 bytes
* 然後進去看他的判斷條件是要蓋成`4GxC95IF` 這個
* 就拿去 base64 encode 然後給
* 比較特別的是他在比對之前會進行一個迴文的判斷，所以最後的 payload 會長這樣 : `NEd4Qzk1SUZBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUZJNTlDeEc0`