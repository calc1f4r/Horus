---
# Core Classification
protocol: Stusdcxbloom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55685
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
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
  - @IAm0x52
---

## Vulnerability Title

[M-05] In the event of yield loss, yield will be double counted leading to excess fees

### Overview


The bug report is about a contract called StUsdc.sol that has an issue with double counting fees. The contract takes a fee whenever there is a yield, but this can lead to double counting if the share price decreases and then increases again. The report recommends implementing a highwater tracker to prevent this issue. This bug has been fixed in a pull request on the stakeup-contracts repository.

### Original Finding Content

**Details**

[StUsdc.sol#L171-L181](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L171-L181)

    if (newUsdPerShare > lastUsdPerShare) {
        uint256 yieldPerShare = newUsdPerShare - lastUsdPerShare;
        // Calculate performance fee
        uint256 fee = _calculateFee(yieldPerShare, globalShares_);
        // Calculate the new total value of the protocol for users
        uint256 userValue = protocolValue - fee;
        newUsdPerShare = userValue.divWad(globalShares_);
        // Update state to distribute yield to users
        _setUsdPerShare(newUsdPerShare);
        // Process fee to StakeUpStaking
        _processFee(fee);

Whenever yield is accumulated by the contract, a fee is taken. In itself this is fine but it can lead to double counted yield in the event that the share price decrease. Take the following example, the share price increases from 1 -> 1.1. A fee will be taken on the 0.1 share price gain. Now the token decreases and increases again as follows 1.1 -> 1.05 -> 1.1. On the move from 1.05 -> 1.1 the fee will be taken again, effectively double charging fees to the users.

**Lines of Code**

[StUsdc.sol#L154-L190](https://github.com/stakeup-protocol/stakeup-contracts/blob/b4d8a83e9455efb8c7543a0fc62b5aea598c7f49/src/token/StUsdc.sol#L154-L190)

**Recommendation**

The contract should implement a highwater tracker for the share price and only pay out fees for increase above that mark.

**Remediation**

Fixed as recommended in stakeup-contracts [PR#89](https://github.com/stakeup-protocol/stakeup-contracts/pull/89)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Stusdcxbloom |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2024-09-22-stUSDCxBloom.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

