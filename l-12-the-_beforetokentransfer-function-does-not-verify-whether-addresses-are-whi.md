---
# Core Classification
protocol: Ethena Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45275
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-11-ethena-labs
source_link: https://code4rena.com/reports/2024-11-ethena-labs
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 1.00
financial_impact: low

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - staking_pool
  - decentralized_stablecoin

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-12] The `_beforeTokenTransfer()` function does not verify whether addresses are whitelisted when `WHITELIST_ENABLED` is set.

### Overview

See description below for full details.

### Original Finding Content


As noted in line 191, the function only checks if the address `to` is not blacklisted. Consequently, unwhitelisted users can still receive UStb when `WHITELIST_ENABLED` is active. This issue appears in several locations.

https://github.com/code-423n4/2024-11-ethena-labs/blob/main/contracts/ustb/UStb.sol#L165-L218

```solidity
    function _beforeTokenTransfer(address from, address to, uint256) internal virtual override {
        // State 2 - Transfers fully enabled except for blacklisted addresses
        if (transferState == TransferState.FULLY_ENABLED) {

            ...

        } else if (transferState == TransferState.WHITELIST_ENABLED) {
            if (hasRole(MINTER_CONTRACT, msg.sender) && !hasRole(BLACKLISTED_ROLE, from) && to == address(0)) {
                // redeeming
191         } else if (hasRole(MINTER_CONTRACT, msg.sender) && from == address(0) && !hasRole(BLACKLISTED_ROLE, to)) {
                // minting
            } else if (hasRole(DEFAULT_ADMIN_ROLE, msg.sender) && hasRole(BLACKLISTED_ROLE, from) && to == address(0)) {
                // redistributing - burn
            } else if (
                hasRole(DEFAULT_ADMIN_ROLE, msg.sender) && from == address(0) && !hasRole(BLACKLISTED_ROLE, to)
            ) {
                // redistributing - mint
            } else if (hasRole(WHITELISTED_ROLE, msg.sender) && hasRole(WHITELISTED_ROLE, from) && to == address(0)) {
                // whitelisted user can burn
            } else if (
                hasRole(WHITELISTED_ROLE, msg.sender) &&
                hasRole(WHITELISTED_ROLE, from) &&
                hasRole(WHITELISTED_ROLE, to) &&
                !hasRole(BLACKLISTED_ROLE, msg.sender) &&
                !hasRole(BLACKLISTED_ROLE, from) &&
                !hasRole(BLACKLISTED_ROLE, to)
            ) {
                // n.b. an address can be whitelisted and blacklisted at the same time
                // normal case
            } else {
                revert OperationNotAllowed();
            }
            // State 0 - Fully disabled transfers
        } else if (transferState == TransferState.FULLY_DISABLED) {
            revert OperationNotAllowed();
        }
    }
```

Include checks to ensure that the addresses are whitelisted.

**[iethena (Ethena Labs) acknowledged and commented](https://github.com/code-423n4/2024-11-ethena-labs-findings/issues/12#issuecomment-2480339994):**
 > Fixed L-01. L-02, L-08 in ethena-labs/ethena-ustb-contest/pull/2

**EV_om (judge) commented via private message to C4 staff:**
> L-01 Invalid
> L-02 Low
> L-03 Low
> L-04 Invalid
> L-05 Non-Critical
> L-06 Non-Critical
> L-07 Low
> L-08 Non-Critical
> L-09 Invalid
> L-10 Invalid
> L-11 Non-Critical
> L-12 Invalid
>
>
> The judge also highlighted the downgraded issues [#7](https://github.com/code-423n4/2024-11-ethena-labs-findings/issues/7) and [#8](https://github.com/code-423n4/2024-11-ethena-labs-findings/issues/8) to be linked in this report for completeness.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Ethena Labs |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-11-ethena-labs
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-11-ethena-labs

### Keywords for Search

`vulnerability`

