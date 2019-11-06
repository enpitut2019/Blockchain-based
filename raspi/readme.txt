ラズパイが有線でネットに繋がっていることが必要
(macと有線接続し、インターネット共有でも可能)

参照ページ
https://qiita.com/wannabe/items/a66c4549e4a11491f9d5
このページに載っていないエラーでhostapd起動できない場合
(sudo apt install rfkill)
rfkill unblock wifi
ifconfig wlan0 down
ifconfig wlna0 up

※　毎回同じエラーとかが起きて上記が必要な場合以下する
/etc/rc.localの、# By default this script does nothing.という行の下に追加
/usr/sbin/rfkill unblock wifi

その他
wifiの自動接続は切っておく
ここに載っていないファイルは参照ページのやつそのまま
(ここのファイルもほぼ参照ページと同じ)