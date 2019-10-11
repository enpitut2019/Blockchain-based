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