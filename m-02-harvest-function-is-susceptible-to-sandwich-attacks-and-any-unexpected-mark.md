---
# Core Classification
protocol: Brrito
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31484
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Brrito-security-review.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] `harvest` function is susceptible to sandwich attacks and any unexpected market events

### Overview


The report discusses a bug in a protocol where attackers can manipulate the `swap` function and steal funds or cause unexpected losses. This is because the function is vulnerable to sandwich attacks and market events. Additionally, the assumption that the `harvest` function will always be callable is incorrect, as it can be paused, leading to potential losses. The report recommends implementing a minimum output parameter and restricting access to the `harvest` function to prevent these issues.

### Original Finding Content

**Severity**

**Impact:** High, Because attackers can sandwich the operation and steal `swap` value, or in unexpected market events, the `swap` could result in an unexpectedly low value.

**Likelihood:** Medium, Because the attack vector is quite common and well-known, and price volatility is typical for non-stable coin tokens.

**Description**

While acknowledged by the protocol team, using `getSwapOutput` to calculate the minimum output of the swap on-chain is still not recommended under any circumstance or assumption. This method is not only vulnerable to sandwich attacks but also susceptible to any market events, such as rapid price changes.

Besides that, the assumption that harvest will always be callable is not correct, as `supply` functionality to `_COMET` can be paused, causing the calls to revert. In the unlikely, but possible, event that the compound pauses the WETH pool, interest would still accrue, and the reward amount would build up, becoming large enough for sandwich attacks to become feasible.

```solidity
    function harvest() external {
        // ...

        // Fetching the quote onchain means that we're subject to front/back-running but the
        // assumption is that we will harvest so frequently that the rewards won't justify the effort.
        // @audit - quote here, already deducted by fee, while the minOutput check at swap, is step before fees are deducted
>>      (uint256 index, uint256 quote) = router.getSwapOutput(
            keccak256(abi.encodePacked(rewardConfig.token, _WETH)),
            rewards
        );

        // `swap` returns the entire WETH amount received from the swap.
>>      uint256 supplyAssets = router.swap(
            rewardConfig.token,
            _WETH,
            rewards,
            quote,
            index,
            // Receives half of the swap fees (the other half remains in the router contract for the protocol).
            feeDistributor
        );

       // ...
    }
```

**Recommendations**

Consider putting the minimum output as a parameter inside the `harvest` function, and if this function is planned to be frequently called by bots, it could be restricted so that only certain roles can invoke it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Brrito |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Brrito-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

