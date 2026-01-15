---
# Core Classification
protocol: Boost Account AA Wallet
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41037
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/426
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-boost-aa-wallet-judging/issues/106

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 16
finders:
  - oxelmiguel
  - ge6a
  - tinnohofficial
  - 4b
  - 0xloophole
---

## Vulnerability Title

M-1: Both block.prevrandao and block.timestamp are not reliably source of randonness

### Overview


The report discusses an issue found in the ERC20Incentive.sol code, where the use of block.prevrandao and block.timestamp as a source of randomness is not reliable. This can allow miners to manipulate the results of a raffle and potentially choose a specific winner. The report recommends changing the method of generating randomness, such as using Chainlink VRF, to prevent this vulnerability.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-boost-aa-wallet-judging/issues/106 

## Found by 
0x539.eth, 0xSecuri, 0xloophole, 4b, Atharv, Japy69, Okazaki, Pheonix, ctf\_sec, denzi\_, ge6a, haxagon, oxelmiguel, pwning\_dev, sakshamguruji, tinnohofficial
## Summary

Both block.prevrandao and block.timestamp are not reliably source of randonness

## Vulnerability Detail

In the ERC20Incentive.sol, 

```solidity
    function drawRaffle() external override onlyOwner {
        if (strategy != Strategy.RAFFLE) revert BoostError.Unauthorized();

        LibPRNG.PRNG memory _prng = LibPRNG.PRNG({state: block.prevrandao + block.timestamp});

        address winnerAddress = entries[_prng.next() % entries.length];

        asset.safeTransfer(winnerAddress, reward);
        emit Claimed(winnerAddress, abi.encodePacked(asset, winnerAddress, reward));
    }
```

the code use block.prevrandao and block.timestamp as source of randoness to determine who is lucky to win the raffle.

However, both op code are not good source of randonness.

https://eips.ethereum.org/EIPS/eip-4399

>  Security Considerations
> The PREVRANDAO (0x44) opcode in PoS Ethereum (based on the beacon chain RANDAO implementation) is a source of randomness with different properties to the randomness supplied by BLOCKHASH (0x40) or DIFFICULTY (0x44) opcodes in the PoW network.

 > Biasability
> The beacon chain RANDAO implementation gives every block proposer 1 bit of influence power per slot. Proposer may deliberately refuse to propose a block on the opportunity cost of proposer and transaction fees to prevent beacon chain randomness (a RANDAO mix) from being updated in a particular slot.

## Impact

Miner can manipulate the block.prevrandao and block.timestamp to let specific address win the raffle

## Code Snippet

https://github.com/sherlock-audit/2024-06-boost-aa-wallet/blob/78930f2ed6570f30e356b5529bd4bcbe5194eb8b/boost-protocol/packages/evm/contracts/incentives/ERC20Incentive.sol#L137

## Tool used

Manual Review

## Recommendation

change randon generate method (can use chainlink VRF, etc...)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Boost Account AA Wallet |
| Report Date | N/A |
| Finders | oxelmiguel, ge6a, tinnohofficial, 4b, 0xloophole, denzi\_, Pheonix, pwning\_dev, Okazaki, haxagon, sakshamguruji, 0x539.eth, Atharv, Japy69, 0xSecuri, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-boost-aa-wallet-judging/issues/106
- **Contest**: https://app.sherlock.xyz/audits/contests/426

### Keywords for Search

`vulnerability`

