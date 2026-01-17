---
# Core Classification
protocol: Telcoin Platform Audit Update
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30573
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/196
source_link: none
github_link: https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update-judging/issues/4

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
  - front-running
  - blacklisted

protocol_categories:
  - bridge

# Audit Details
report_date: unknown
finders_count: 13
finders:
  - ZdravkoHr.
  - ZanyBonzy
  - blutorque
  - neocrao
  - bughuntoor
---

## Vulnerability Title

M-1: Blacklisted accounts can still transact.

### Overview


Issue M-1 reports a vulnerability in the Telcoin platform where blacklisted accounts are still able to transact normally. This means that even though an account has been blacklisted, it can still use the platform's Stablecoin funds. This vulnerability was found by multiple individuals and is considered a medium impact as it affects a manually administered security feature. The vulnerability was identified through a manual review and it is recommended that the protocol team update the code to prevent blacklisted addresses from being able to send and receive tokens. The team has since fixed the issue and the Lead Senior Watson has signed off on the fix. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update-judging/issues/4 

## Found by 
0xkmg, Krace, Tendency, ZanyBonzy, ZdravkoHr., blutorque, bughuntoor, cawfree, merlin, neocrao, sa9933, smbv-1923, turvec
## Summary

Accounts that have been blacklisted by the [`BLACKLISTER_ROLE`](https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update/blob/21920190e0772afa18e7f856a036fea3ef5b9635/telcoin-contracts/contracts/util/abstract/Blacklist.sol#L32) continue to transact normally.

## Vulnerability Detail

Currently, the only real effect of blacklisting an account is the seizure of [`Stablecoin`](https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update/blob/main/telcoin-contracts/contracts/stablecoin/Stablecoin.sol) funds:

```solidity
/**
 * @notice Overrides Blacklist function to transfer balance of a blacklisted user to the caller.
 * @dev This function is called internally when an account is blacklisted.
 * @param user The blacklisted user whose balance will be transferred.
 */
function _onceBlacklisted(address user) internal override {
  _transfer(user, _msgSender(), balanceOf(user));
}
```

However, following a call to [`addBlackList(address)`](https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update/blob/21920190e0772afa18e7f856a036fea3ef5b9635/telcoin-contracts/contracts/util/abstract/Blacklist.sol#L72C14-L72C26), the blacklisted account may continue to transact using [`Stablecoin`](https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update/blob/main/telcoin-contracts/contracts/stablecoin/Stablecoin.sol).

Combined with previous audit reports, which attest to the blacklist function's [susceptibility to frontrunning](https://github.com/sherlock-audit/2023-02-telcoin-judging/issues/43), the current implementation of the blacklist operation can effectively be considered a no-op.

## Impact

Medium, as this the failure of a manually administered security feature.

## Code Snippet

### [📄 Stablecoin.sol](https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update/blob/main/telcoin-contracts/contracts/stablecoin/Stablecoin.sol)

## Tool used

Manual Review

## Recommendation

ERC20s that enforce blacklists normally prevent a sanctioned address from being able to transact:

### [📄 Stablecoin.sol](https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update/blob/main/telcoin-contracts/contracts/stablecoin/Stablecoin.sol)

```diff
+ error Blacklisted(address account);

+function _update(address from, address to, uint256 value) internal virtual override {
+
+  if (blacklisted(from)) revert Blacklisted(from); 
+  if (blacklisted(to)) revert Blacklisted(to);
+
+  super._update(from, to, value);
+}
```



## Discussion

**sherlock-admin4**

1 comment(s) were left on this issue during the judging contest.

**takarez** commented:
>  valid; high(1)



**sherlock-admin4**

The protocol team fixed this issue in PR/commit https://github.com/telcoin/telcoin-contracts/pull/3.

**spacegliderrrr**

Fix looks good, blacklisted addresses can no longer send and receive tokens.

**sherlock-admin4**

The Lead Senior Watson signed off on the fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin Platform Audit Update |
| Report Date | N/A |
| Finders | ZdravkoHr., ZanyBonzy, blutorque, neocrao, bughuntoor, sa9933, smbv-1923, 0xkmg, Krace, Tendency, turvec, merlin, cawfree |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-02-telcoin-platform-audit-update-judging/issues/4
- **Contest**: https://app.sherlock.xyz/audits/contests/196

### Keywords for Search

`Front-Running, Blacklisted`

