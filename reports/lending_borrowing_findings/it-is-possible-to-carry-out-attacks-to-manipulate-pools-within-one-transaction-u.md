---
# Core Classification
protocol: Cover Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28662
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Cover%20Protocol/Cover%20Protocol%20Peripheral/README.md#1-it-is-possible-to-carry-out-attacks-to-manipulate-pools-within-one-transaction-using-a-flash-loan
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

It is possible to carry out attacks to manipulate pools within one transaction using a flash loan

### Overview


This bug report is about a vulnerability in contracts CoverRouter.sol and Rollover.sol. These contracts allow users to exchange tokens and add and remove liquidity. An attacker can exploit this vulnerability by taking a flash loan and performing multiple liquidity manipulations within a single transaction. This can lead to a loss of funds for other users. 

To protect against token manipulation with flash loans, it is recommended to add the following code to the contracts: 

```solidity
mapping(address => uint256) private _lastSwapBlock;

function some() external {
   _preventSameTxOrigin();
   ....
   some logic
   ...
 }

function _preventSameTxOrigin() private {
   require(block.number > _lastSwapBlock[tx.origin], "SAME_TX_ORIGIN");
   _lastSwapBlock[tx.origin] = block.number;
 }
```

This code will prevent an attacker from performing multiple liquidity manipulations within a single transaction. This will help protect other users from potential losses of funds.

### Original Finding Content

##### Description
In contracts https://github.com/CoverProtocol/cover-peripheral/tree/d5b37e34d47abec3252cdabd46e55e34a72421d4/contracts/CoverRouter.sol and https://github.com/CoverProtocol/cover-peripheral/tree/d5b37e34d47abec3252cdabd46e55e34a72421d4/contracts/Rollover.sol, any user can exchange tokens with a contract. Any user can add and remove liquidity. An attacker can take a flash loan and perform multiple liquidity manipulations within a single transaction. These manipulations can lead to a loss of funds for other users.

##### Recommendation
It is recommended to add protection against token manipulation with flash loans.
Here's some sample code:

```solidity
mapping(address => uint256) private _lastSwapBlock;

function some() external {
   _preventSameTxOrigin();
   ....
   some logic
   ...
 }

function _preventSameTxOrigin() private {
   require(block.number > _lastSwapBlock[tx.origin], "SAME_TX_ORIGIN");
   _lastSwapBlock[tx.origin] = block.number;
 }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Cover Protocol |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Cover%20Protocol/Cover%20Protocol%20Peripheral/README.md#1-it-is-possible-to-carry-out-attacks-to-manipulate-pools-within-one-transaction-using-a-flash-loan
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

