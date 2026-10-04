---
# Core Classification
protocol: Trader Joe
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5712
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-trader-joe-v2-contest
source_link: https://code4rena.com/reports/2022-10-traderjoe
github_link: https://github.com/code-423n4/2022-10-traderjoe-findings/issues/108

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 14
finders:
  - The_GUILD
  - 0x52
  - MiloTruck
  - phaze
  - bctester
---

## Vulnerability Title

[M-02] beforeTokenTransfer called with wrong parameters in LBToken._burn

### Overview


This bug report is about a vulnerability in the code of the 'LBToken' contract. This vulnerability is caused by an incorrect call of the '_beforeTokenTransfer' hook with 'from = address(0)' and 'to = _account'. While this does not cause any high severity issue in the current setup, this wrong call is dangerous for future extensions or protocols built on top of the protocol or forked from it.

For example, if the protocol is extended with some logic that needs to track mints and burns, the code would break, leading to possible loss of funds or a bricked system.

The recommended mitigation step for this vulnerability is to call the hook correctly with '_account' as the first parameter and 'address(0)' as the second parameter.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-traderjoe/blob/37258d595d596c195507234f795fa34e319b0a68/src/LBToken.sol#L237


## Vulnerability details

## Impact
In `LBToken._burn`, the `_beforeTokenTransfer` hook is called with `from = address(0)` and `to = _account`:
```solidity
_beforeTokenTransfer(address(0), _account, _id, _amount);
```
Through a lucky coincidence, it turns out that this in the current setup does not cause a high severity issue. `_burn` is always called with `_account = address(this)`, which means that `LBPair._beforeTokenTransfer` is a NOP. However, this wrong call is very dangerous for future extensions or protocol that built on top of the protocol / fork it.

## Proof Of Concept
Let's say the protocol is extended with some logic that needs to track mints / burns. The canonical way to do this would be:
```solidity
function _beforeTokenTransfer(
        address _from,
        address _to,
        uint256 _id,
        uint256 _amount
    ) internal override(LBToken) {
	if (_from == address(0)) {
		// Mint Logic
	} else if (_to == address(0)) {
		// Burn Logic
	}
}
```
Such an extension would break, which could lead to loss of funds or a bricked system.

## Recommended Mitigation Steps
Call the hook correctly:
```solidity
_beforeTokenTransfer(_account, address(0), _id, _amount);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Trader Joe |
| Report Date | N/A |
| Finders | The_GUILD, 0x52, MiloTruck, phaze, bctester, ladboy233, Aymen0909, Lambda, KingNFT, zzzitron, indijanc, imare, chaduke, RustyRabbit |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-traderjoe
- **GitHub**: https://github.com/code-423n4/2022-10-traderjoe-findings/issues/108
- **Contest**: https://code4rena.com/contests/2022-10-trader-joe-v2-contest

### Keywords for Search

`Business Logic`

