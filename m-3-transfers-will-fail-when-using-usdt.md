---
# Core Classification
protocol: LEND
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58400
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/908
source_link: none
github_link: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/529

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
finders_count: 19
finders:
  - 0xpetern
  - 0xDemon
  - wickie
  - 1337web3
  - kom
---

## Vulnerability Title

M-3: Transfers will fail when using USDT

### Overview


The bug report discusses an issue with some tokens, specifically USDT, not complying with the ERC20 standard. This means that when certain functions are called using these tokens, they will fail and cause a denial of service (DoS) for the protocol. The report suggests using the OZ `SafeERC20` library's `safeTransfer` as a solution to mitigate this issue. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/529 

## Found by 
0xDemon, 0xpetern, 1337web3, A\_Failures\_True\_Power, Drynooo, Hueber, adeolu, dimah7, h2134, ifeco445, khaye26, kom, mgf15, molaratai, oade\_hacks, one618xyz, skipper, theweb3mechanic, wickie

### Summary

Some tokens like USDT doesn't comply with the ERC20 standard and doesn't return `bool` on ERC20 methods. This will make the calls with this token to revert, making it impossible to use them.

### Root Cause

Tokens like USDT on Mainnet doesn't comply with the ERC20 specs, thus will fail when regular transfers are tried to be made with them, resulting in DoS of core functions of the protocol. For example the `CoreRouter::borrow`:

https://github.com/sherlock-audit/2025-05-lend-audit-contest/blob/3c97677544cf993c9f7be18d423bd3b5e5a62dd9/Lend-V2/src/LayerZero/CoreRouter.sol#L170

```javascript
function borrow(uint256 _amount, address _token) external {
        require(_amount != 0, "Zero borrow amount");

        address _lToken = lendStorage.underlyingTolToken(_token);

        ...

        // Borrow tokens
        require(LErc20Interface(_lToken).borrow(_amount) == 0, "Borrow failed");

        // Transfer borrowed tokens to the user
@>      IERC20(_token).transfer(msg.sender, _amount);
```

Using USDT here will not comply with the interaface and revert, this is of concern because the borrow function is basically one of the entry-points to the protocol.

### Internal Pre-conditions

None

### External Pre-conditions

None

### Attack Path

None

### Impact

DoS on borrows

### PoC

_No response_

### Mitigation

Use OZ `SafeERC20` library's `safeTransfer`

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | LEND |
| Report Date | N/A |
| Finders | 0xpetern, 0xDemon, wickie, 1337web3, kom, Drynooo, theweb3mechanic, skipper, ifeco445, mgf15, Hueber, h2134, A\_Failures\_True\_Power, molaratai, khaye26, dimah7, adeolu, one618xyz, oade\_hacks |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-05-lend-audit-contest-judging/issues/529
- **Contest**: https://app.sherlock.xyz/audits/contests/908

### Keywords for Search

`vulnerability`

