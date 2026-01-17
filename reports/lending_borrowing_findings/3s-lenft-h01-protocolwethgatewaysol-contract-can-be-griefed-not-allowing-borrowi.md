---
# Core Classification
protocol: Lenft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19076
audit_firm: ThreeSigma
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ThreeSigma/2023-06-06-leNFT.md
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
  - ThreeSigma
---

## Vulnerability Title

3S-LENFT-H01 protocol/WETHGateway.sol: contract can be griefed not allowing borrowing

### Overview


A bug has been reported in the WETHGateway contract, which is used to simplify operations with ETH by converting it to WETH. If someone sends 1 wei to the contract, it will always revert on line 117 of the contract, making the borrow operation useless. This issue is not critical, but it does have a high severity as it affects user experience. To fix the issue, it is recommended to remove the line responsible for the revert, as the market.borrow() call will either revert or transfer the amount to the contract, and any calls to unwrap the WETH and send it back to the user will also revert, thus protecting user funds. It is also possible to remove the balance of the WETHGateway contract, though this would not be a definitive solution as any user could send another wei to the contract, blocking it again.

### Original Finding Content

#### Description
The borrow operation of the WETHGateway contract can be rendered useless if someone sends 1 wei to the contract (causing it to always revert on [line 117](https://github.com/leNFT/contracts/blob/master/contracts/protocol/WETHGateway.sol#L117)): `assert(_weth.balanceOf(address(this)) == amount);`

This issue in not critical since the WETHGateway contract is just a router which simplifies operations with eth (by converting it to weth), however, the severity is still high since it is used by the front end, so this exploit could significantly harm user experience.

#### Recommendation
Remove this line since the `market.borrow()` call will either revert or transfer the amount to the contract. Even if it doesn't, the calls to unwrap the weth and send it back to the user will also revert, so the user funds are always protected.


Note: Is is always possible to remove the balance of the WETHGateway contract, since anyone can use `depositTradingPool()` to get approval for all NFTs and weth from the contract. This would not present a definitive solution though, as any user could send another wei to the contract, blocking it again.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ThreeSigma |
| Protocol | Lenft |
| Report Date | N/A |
| Finders | ThreeSigma |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ThreeSigma/2023-06-06-leNFT.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

