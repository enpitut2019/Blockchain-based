pragma solidity ^0.5.8;
// 各ベンダーが利用するアップデートログ を保持するコントラクト 
contract Update_log {
    // モデル名と開発者のマッピング
    mapping(string=>address) public vender;
    // モデル名でファームウェアを管理(リストの最新が最新のファームウェア)
    mapping(string=>int256[]) public version;
    
    // モデル名・バージョンで検証用ハッシュ値取得 実装未定
   // mapping(string=>mapping(int256=>string[])) public firmware;
    
    address public owner;

    constructor() public{
        owner = msg.sender;
    }
    
    event Up_newver(address indexed from, string indexed model, int256 indexed ver);
    
    // ハッシュ関数(文字列 -> ハッシュ値)
    function getHash(string memory _var) public pure returns (bytes32){
        byte b = 0x00;
        uint8 i = 0;
        return keccak256(abi.encodePacked(b, i, _var));
    }
    
    // モデル名(_model)を元に最新のファームウェア(_program)情報を保存
    function up_newver(string memory _model,int256 _ver)public{
        if(vender[_model] == address(0)){
            vender[_model] = msg.sender;
        }else if(vender[_model] != msg.sender){
            revert("不正な更新情報です");
        }
        
        version[_model].push(_ver);
        emit Up_newver(msg.sender, _model, _ver);
        //firmware[_model][_ver].push(getHash(_program));
    }
    
    // 最新のファームウェア情報を取得
    function getInfo(string memory _model) public view returns (int256){
        if(vender[_model] == address(0)){
            revert("該当するモデルはありません");
        }
        return version[_model][version[_model].length - 1];
    }
}

contract Idmng{

    
    mapping (address => uint256) devAddrTorank; //デバイスのアドレスとランクの紐付け
    mapping (address => string) devAddrToname;//デバイスとのアドレスとデバイス名のランクづけ
    

    // IDrank=0...安全 
    // IDrank=1...危険

    function regDevice(address _devAddr,string memory _devName) public{// ID管理局がデバイスのアドレスとランク,アドレスとデバイス名を紐づけて登録する
         devAddrTorank[_devAddr]=0; //登録時点ではデバイスは安全(デバイスランクは0)
         devAddrToname[_devAddr]=_devName; //デバイスのアドレスと名前を紐づける
    }

    function getDeviceRank(address _devAddr) public view returns(uint256){//親IoTがアドレスをブロックチェーンに投げて,rankを確認する
         return devAddrTorank[_devAddr];
    }
    function getDeviceName(address _devAddr)public view returns(string memory){//確認用
        return devAddrToname[_devAddr];
    }
    
    
}

contract IDchecker{
    Update_log public ulog;
    Idmng public idm;

    constructor(Update_log _ulog, Idmng _idm) public{
        ulog = _ulog;
        idm = _idm;
    }
    
    function checkID(int256 _ver, address _addr) public view returns(uint256){
        // アドレスのモデル名取得
        string memory name = idm.getDeviceName(_addr);
        // アドレスのバージョンを取得
        int256 ver = ulog.getInfo(name);
        if(ver == _ver){
            return 0;
        }else{
            return 1;
        }
    }
    
}