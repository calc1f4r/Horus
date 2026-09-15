---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21314
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/08/lybra-finance/
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

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

The configurator.getEUSDMaxLocked() Condition Can Be Bypassed During a Flashloan ✓ Fixed

### Overview


A bug was discovered in the LybraV2 project where a user can bypass the restriction on the total amount of EUSD tokens that can be converted to peUSD. This is due to the fact that a flash loan can be taken from the contract, reducing the visible amount of locked tokens. This bug has been resolved by checking the EUSD amount after the flash loan has been taken. Multiple approaches can be taken to prevent this issue from occurring in the future, such as adding reentrancy protection or keeping track of the borrowed amount for a flash loan.

### Original Finding Content

#### Resolution



Fixed in [f6c3afb5e48355c180417b192bd24ba294f77797](https://github.com/LybraFinance/LybraV2/commit/f6c3afb5e48355c180417b192bd24ba294f77797) by checking `eUSD` amount after flash loan.


#### Description


When converting `EUSD` tokens to `peUSD`, there is a check that limits the total amount of `EUSD` that can be converted:


**contracts/lybra/token/PeUSDMainnet.sol:L74-L77**



```
function convertToPeUSD(address user, uint256 eusdAmount) public {
 require(\_msgSender() == user || \_msgSender() == address(this), "MDM");
 require(eusdAmount != 0, "ZA");
 require(EUSD.balanceOf(address(this)) + eusdAmount <= configurator.getEUSDMaxLocked(),"ESL");

```
The issue is that there is a way to bypass this restriction. An attacker can get a flash loan (in `EUSD`) from this contract, essentially reducing the visible amount of locked tokens (`EUSD.balanceOf(address(this))`).


#### Recommendation


Multiple approaches can solve this issue. One would be adding reentrancy protection. Another one could be keeping track of the borrowed amount for a flashloan.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/08/lybra-finance/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

