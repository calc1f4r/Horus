---
# Core Classification
protocol: Polygon zkEVM Contracts
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21436
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/zkEVM-bridge-Spearbit-27-March.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/zkEVM-bridge-Spearbit-27-March.pdf
github_link: none

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
  - fee_on_transfer

protocol_categories:
  - bridge

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Xiaoming90
  - Gerard Persoon
  - Pashov Krum
  - 0xLeastwood
  - Csanuragjain
---

## Vulnerability Title

Fee on transfer tokens

### Overview


This bug report is about a problem with the PolygonZkEVMBridge.sol contract on line 171. The issue is that when a user bridges a fee on transfer Token A from Mainnet to Rollover R1 for an amount X, the bridge contract will not work properly. X-fees will be received by the bridge contract on Mainnet, but the deposit receipt of the full amount X will be stored in Merkle. When the full amount is bridged back to Mainnet, the contract tries to transfer the amount X, but since it received the amount X-fees, it will use the amount from other users, which can eventually cause a denial of service for other users using the same token. 

To fix this issue, the exact amount which is transferred to the contract should be used. This can be done by adding a check for reentrancy with erc777 tokens and using a sample code to obtain the amount which is transferred to the contract. This issue was solved in PR 87 and 91 and was verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
`PolygonZkEVMBridge.sol#L171`

## Description
The bridge contract will not work properly with a fee on transfer tokens.

1. User A bridges a fee on transfer Token A from Mainnet to Rollover R1 for amount X.
2. In that case, X-fees will be received by the bridge contract on Mainnet, but the deposit receipt of the full amount X will be stored in Merkle.
3. The amount is claimed in R1, and a new TokenPair for Token A is generated, and the full amount X is minted to User A.
4. Now the full amount is bridged back again to Mainnet.
5. When a claim is made on Mainnet, then the contract tries to transfer amount X, but since it received the amount X-fees, it will use the amount from other users, which eventually causes denial of service (DOS) for other users using the same token.

## Recommendation
Use the exact amount that is transferred to the contract, which can be obtained using the sample code below:

```solidity
uint256 balanceBefore = IERC20Upgradeable(token).balanceOf(address(this));
IERC20Upgradeable(token).safeTransferFrom(address(msg.sender), address(this), amount);
uint256 balanceAfter = IERC20Upgradeable(token).balanceOf(address(this));
uint256 transferedAmount = balanceAfter - balanceBefore;

// if you don't want to support fee on transfer token use below:
require(transferedAmount == amount, ...);

// use transferedAmount if you want to support fee on transfer token
```

## Additional Notes
- Polygon-Hermez: Solved in PR 87. To protect against reentrancy with ERC777 tokens, a check for reentrancy MUST be added. Solved in PR 91.
- Spearbit: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Polygon zkEVM Contracts |
| Report Date | N/A |
| Finders | Xiaoming90, Gerard Persoon, Pashov Krum, 0xLeastwood, Csanuragjain |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/zkEVM-bridge-Spearbit-27-March.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/zkEVM-bridge-Spearbit-27-March.pdf

### Keywords for Search

`Fee On Transfer`

