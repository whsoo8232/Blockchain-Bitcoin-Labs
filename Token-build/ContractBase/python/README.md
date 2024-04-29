1. 작업 directory(UpgradableContract)가 있어야한다.
   UpgradableContract/
     |
     +-- contracts/
     |
     +-- package.json
     |
     +-- scripts/
     |
     +-- testConfig/
     |     |
     |     +-- ERC20TokenName.sol
     |     |
     |     +-- ERC721TokenName.sol
     |     |
     |     +-- deploy1.js.samp
     |     |
     |     +-- deploy2.js.samp(사용않함)
     |     |
     |     +-- hardhat.config.js.samp
     |
     +-- utils/
           |
           +-- verify.js

2. 작업순서
   1) contract 정보 입력
      > 공통
        - network : baobab, klaytn, mumbai, polygon 등 network 이름 설정
          . testConfig directory의 hardhat.config.js.samp에 해당 이름이 있는지 확인. 없으면 추가
        - infuraKey : infura api key를 설정
          . 없는 경우 등록 필수
        - etherscanKey : etherscan의 api key 설정
          . 없는 경우, etherscan 사이트에서 등록하가나 공백 설정
        - ownerPK : owner privage key
      > Token 정보 입력
        - ERC20의 경우
          . tokenTyps        : ERC20
          . targetTokenName  : Token Name
          . targetSymbolName : Token Symbol Name
          . targetAmount     : Total total amount
        - ERC721의 경우
          . tokenTyps        : ERC721
          . targetTokenName  : Token Name
          . targetSymbolName : Token Symbol Name
          . targetAmount     : None
   2) deployContract 함수 호출
      > retCode, retMessage = deployContract(network, infuraKey, etherscanKey, ownerPK, tokenType, targetTokenName, targetSymbolName, targetAmount)
   3) deployContract 함수에서 하는 일
      > subprocess.Popen으로 ./deployContract.sh clean을 호출하여 이전 정보 삭제
      > tokenType에 따라 ERC20Token 또는 ERC721Token 소스를 contracts 디렉토리에 생성
      > infuraKey, etherscanKey, ownerPK를 home directory에 .env에 저장
      > testConfig/hardhat.config.js.samp 를 읽어서 localhost를 network에 설정된 값으로 수정한 후 directory home에 hardhat.config.js로 저장
      > testConfig/deployv1.js.samp를 읽어서 tokenName을 targetTokenName에 설정된 값으로 수정한 수 scripts/deploy1.js로 저장
      > subprocess.Popen으로 ./deployContract.sh deploy1을 호출하여 contract 배포 후 결과 deployed 된 contract address 를 contractAddress 변수에 저장
      > artifacts/contracts/{tokenName}.sol/{tokenName}.json 파일을 jsonData 변수로 load
      > jsonData['abi']를 abi 변수값으로, jsonData['bytecode']를 byteCodeData 변수값으로 저장
      > backup directory를 생성("../Upgradeable/backup/" + datetime.now().strftime("%Y_%m_%d"))
      > targetTokenName + '.abi" 파일을 backup directoru에 저장
      > contracts/{targetTokenName}.sol 을 "../Upgradeable/backup/" + datetime.now().strftime("%Y_%m_%d") + "/" + targetTokenName + ".sol" 로 저장
      > contractAddress 변수값을 "../Upgradeable/backup/" + datetime.now().strftime("%Y_%m_%d") + "/" + targetTokenName + ".addr"에 저장
