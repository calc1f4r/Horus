---
# Core Classification
protocol: Debt DAO
chain: everychain
category: uncategorized
vulnerability_type: call_vs_transfer

# Attack Vector Details
attack_type: call_vs_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6250
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-debt-dao-contest
source_link: https://code4rena.com/reports/2022-11-debtdao
github_link: https://github.com/code-423n4/2022-11-debtdao-findings/issues/369

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3.0003583740810145
rarity_score: 1.001075122243043

# Context Tags
tags:
  - call_vs_transfer

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - payments
  - rwa_lending

# Audit Details
report_date: unknown
finders_count: 33
finders:
  - codexploder
  - Nyx
  - cryptonue
  - Bnke0x0
  - peanuts
---

## Vulnerability Title

[M-10] address.call{value:x}() should be used instead of payable.transfer()

### Overview


This bug report is about an issue with the Line-of-Credit contract on the Ethereum blockchain. The contract uses Solidity's `transfer()` function to withdraw and refund ETH. This function can cause issues when the withdrawer is a smart contract, as it may not be able to withdraw ETH deposits. This is because the withdrawer smart contract may not have a payable fallback function, or it may have one that uses more than 2300 gas units. The risks of reentrancy stemming from the use of this function can be mitigated by following the "Check-Effects-Interactions" pattern and using OpenZeppelin Contract’s ReentrancyGuard contract. It is recommended to use low-level `call.value(amount)` with the corresponding result check or using the OpenZeppelin `Address.sendValue` instead.

### Original Finding Content

## Lines of code

https://github.com/debtdao/Line-of-Credit/blob/e8aa08b44f6132a5ed901f8daa231700c5afeb3a/contracts/utils/LineLib.sol#L48


## Vulnerability details

## Impact

When withdrawing and refund  ETH, the  contract uses Solidity’s `transfer()` function. 

Using Solidity's `transfer()` function has some notable shortcomings when the withdrawer is a smart contract, which can render ETH deposits impossible to withdraw. Specifically, the withdrawal will inevitably fail when:
* The withdrawer smart contract does not implement a payable fallback function.
* The withdrawer smart contract implements a payable fallback function which uses more than 2300 gas units.
* The withdrawer smart contract implements a payable fallback function which needs less than 2300 gas units but is called through a proxy that raises the call’s gas usage above 2300.

Risks of reentrancy stemming from the use of this function can be mitigated by tightly following the "Check-Effects-Interactions" pattern and using OpenZeppelin Contract’s ReentrancyGuard contract. 

## Proof of Concept

```solidity
// Line-of-Credit/contracts/utils/LineLib.sol
48:    payable(receiver).transfer(amount);
```


#### References:

The issues with `transfer()` are outlined [here](https://consensys.net/diligence/blog/2019/09/stop-using-soliditys-transfer-now/
)

For further reference on why using Solidity’s `transfer()` is no longer recommended, refer to these [articles](https://blog.openzeppelin.com/reentrancy-after-istanbul/).



## Tools Used
Manual analysis.

## Recommended Mitigation Steps

Using low-level `call.value(amount)` with the corresponding result check or using the OpenZeppelin `Address.sendValue` is advised, [reference](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Address.sol#L60).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3.0003583740810145/5 |
| Rarity Score | 1.001075122243043/5 |
| Audit Firm | Code4rena |
| Protocol | Debt DAO |
| Report Date | N/A |
| Finders | codexploder, Nyx, cryptonue, Bnke0x0, peanuts, Ch_301, pashov, minhquanym, joestakey, KingNFT, Amithuddar, adriro, Tomo, d3e4, IllIllI, Deivitto, cccz, RaymondFam, corerouter, 0xdeadbeef0x, cloudjunky, SmartSek, 8olidity, __141345__, datapunk, martin, RedOneN, carlitox477, merlin, rvierdiiev, Satyam_Sharma, bananasboys |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-debtdao
- **GitHub**: https://github.com/code-423n4/2022-11-debtdao-findings/issues/369
- **Contest**: https://code4rena.com/contests/2022-11-debt-dao-contest

### Keywords for Search

`call vs transfer`

