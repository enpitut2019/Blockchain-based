pragma solidity ^0.5.1;

contract Idmng{

    
    mapping (address => uint256) devAddrTorank; //デバイスのアドレスとランクの紐付け
    mapping (address => string) devAddrTodevname;//デバイスとのアドレスとデバイス名のランクづけ
    

    // IDrank=0...安全 
    // IDrank=1...危険

    function regDevice(address _devAddr,address _devName) public{　// ID管理局がデバイスのアドレスとランク,アドレスとデバイス名を紐づけて登録する
         devAddrTorank[_devAddr]=0; //登録時点ではデバイスは安全(デバイスランクは0)
         devAddrTodevname[_devAddr]=_devName;  //デバイスのアドレスと名前を紐づける
    }

    function getDeviceRank(address _devAddr) public returns(uint256){//親IoTがアドレスをブロックチェーンに投げて,rankを確認する
         return devAddrTorank[_devAddr];
    }
    
}