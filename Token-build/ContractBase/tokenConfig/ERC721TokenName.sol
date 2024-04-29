// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts-upgradeable/token/ERC721/ERC721Upgradeable.sol"; 
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721URIStorageUpgradeable.sol"; 
import "@openzeppelin/contracts-upgradeable/token/ERC721/extensions/ERC721BurnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/PausableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol"; 
import "@openzeppelin/contracts-upgradeable/utils/CountersUpgradeable.sol";

contract ERC721TokenName is Initializable, ERC721Upgradeable, ERC721URIStorageUpgradeable, OwnableUpgradeable, PausableUpgradeable, ERC721BurnableUpgradeable { 
    using CountersUpgradeable for CountersUpgradeable.Counter;
    CountersUpgradeable.Counter private supplyCounter;

    mapping(address => bool) public isMinter;
    mapping(address => bool) public isPauser;

    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }

    function initialize() public initializer { 
        __ERC721_init("ERC721TokenName", "SymbolName"); 
        __ERC721URIStorage_init(); 
        __Pausable_init();
        __ERC721Burnable_init();
        __Ownable_init(); 
    } 

    /**
     * @dev Sets the status of minter.
     */
    function setMinter(address _address, bool _status) public onlyOwner() {
        isMinter[_address] = _status;
    }

    /**
     * @dev Throws if called by any account that is not minter.
     */
    modifier onlyMinter() {
        require(isMinter[_msgSender()], "!Minter");
        _;
    }

    /**
     * @dev Sets the status of pauser.
     */
    function setPauser(address _address, bool _status) public onlyOwner() {
        isPauser[_address] = _status;
    }

    /**
     * @dev Throws if called by any account that is not pauser.
     */
    modifier onlyPauser() {
        require(isPauser[_msgSender()], "!Pauser");
        _;
    }

    function pause() public onlyPauser { 
        _pause();
    }

    function unpause() public onlyPauser { 
        _unpause();
    }

    function totalSupply() public view returns (uint256) {
        return supplyCounter.current();
    }

    function mint(address to, uint256 tokenId, string memory tokenUri) public onlyMinter { 
        _mint(to, tokenId);
	_setTokenURI(tokenId, tokenUri);
        supplyCounter.increment();
    } 
    
    function multimint (address[] memory dests,uint256[] memory tokenIds, string[] memory tokenURIs) public onlyMinter returns (uint256) {
        uint256 i = 0;
        while (i < dests.length) {
            mint(dests[i], tokenIds[i], tokenURIs[i]);
            i += 1;
        }
        return(i);
    }


    function _burn(uint256 tokenId) internal override(ERC721Upgradeable, ERC721URIStorageUpgradeable) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId) public view override(ERC721Upgradeable, ERC721URIStorageUpgradeable) returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721Upgradeable, ERC721URIStorageUpgradeable) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}
