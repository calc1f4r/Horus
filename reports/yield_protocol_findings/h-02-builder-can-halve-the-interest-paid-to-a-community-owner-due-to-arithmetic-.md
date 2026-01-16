---
# Core Classification
protocol: Rigor Protocol
chain: everychain
category: arithmetic
vulnerability_type: rounding

# Attack Vector Details
attack_type: rounding
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3100
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-08-rigor-protocol-contest
source_link: https://code4rena.com/reports/2022-08-rigor
github_link: https://github.com/code-423n4/2022-08-rigor-findings/issues/180

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.70
financial_impact: high

# Scoring
quality_score: 3.5
rarity_score: 1.5

# Context Tags
tags:
  - rounding

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 11
finders:
  - TrungOre
  - Deivitto
  - 0x52
  - simon135
  - rbserver
---

## Vulnerability Title

[H-02] Builder can halve the interest paid to a community owner due to arithmetic rounding

### Overview


A bug has been identified in the code for the Community.sol contract. This bug allows a builder to halve the APR paid to a community owner by paying every 1.9999 days. This would allow a builder to advertise very high APR rates to secure funding, but then pay back much lower rates than advertised. This bug occurs in the calculation of `noOfDays` in `returnToLender()` which calculates the number of days since interest has last been calculated. If a builder repays a very small amount of tokens every 1.9999 days, then the `noOfDays` will be rounded down to `1 days` however `lastTimestamp` is updated to the current timestamp anyway, so the builder essentially accumulates only 1 day of interest after 2 days.

This is considered high severity because a community owner can have a drastic decrease in interest gained from a loan which counts as lost rewards. Additionally, this problem does not require a malicious builder because if a builder pays at a wrong time, the loaner receives less interest anyway.

Two possible mitigations have been proposed. The first solution is to add a scalar to `noOfDays` so that any rounding which occurs is negligible. The second solution is to remove the `noOfDays` calculation and calculate interest in one equation which reduces arithmetic rounding.

### Original Finding Content

_Submitted by scaraven, also found by 0x52, auditor0517, Deivitto, hansfriese, Lambda, rbserver, simon135, smiling&#95;heretic, sseefried, and TrungOre_

[Community.sol#L685-L686](https://github.com/code-423n4/2022-08-rigor/blob/5ab7ea84a1516cb726421ef690af5bc41029f88f/contracts/Community.sol#L685-L686)<br>

Due to arithmetic rounding in `returnToLender()`, a builder can halve the APR paid to a community owner by paying every 1.9999 days. This allows a builder to drastically decrease the amount of interest paid to a community owner, which in turn allows them to advertise very high APR rates to secure funding, most of which they will not pay.

This issue occurs in the calculation of `noOfDays` in `returnToLender()` which calculates the number of days since interest has last been calculated. If a builder repays a very small amount of tokens every 1.9999 days, then the `noOfDays` will be rounded down to `1 days` however `lastTimestamp` is updated to the current timestamp anyway, so the builder essentially accumulates only 1 day of interest after 2 days.

I believe this is high severity because a community owner can have a drastic decrease in interest gained from a loan which counts as lost rewards. Additionally, this problem does not require a malicious builder because if a builder pays at a wrong time, the loaner receives less interest anyway.

### Proof of Concept

1.  A community owner provides a loan of 500\_000 tokens to a builder with an APR of 10% (ignoring treasury fees)
2.  Therefore, the community owner will expect an interest of 136.9 tokens per day (273.9 per 2 days)
3.  A builder repays 0.000001 tokens at `lastTimestamp + 2*86400 - 1`
4.  `noOfDays` rounds down to 1 thereby accumulating `500_000 * 100 * 1 / 365000 = 136` tokens for 2 days
5.  Therefore, the community owner only receives 5% APR with negligible expenses for the builder

### Tools Used

VS Code

### Recommended Mitigation Steps

There are two possible mitigations:

1.  Add a scalar to `noOfDays` so that any rounding which occurs is negligible

i.e.

```solidity
        uint256 _noOfDays = (block.timestamp -
            _communityProject.lastTimestamp) * SCALAR / 86400; // 24*60*60


        /// Interest formula = (principal * APR * days) / (365 * 1000)
        // prettier-ignore
        uint256 _unclaimedInterest = 
                _lentAmount *
                _communities[_communityID].projectDetails[_project].apr *
                _noOfDays /
                365000 /
                SCALAR;
```

2.  Remove the `noOfDays` calculation and calculate interest in one equation which reduces arithmetic rounding

```solidity
uint256 _unclaimedInterest = 
                _lentAmount *
                _communities[_communityID].projectDetails[_project].apr *
                (block.timestamp -
            _communityProject.lastTimestamp) /
                365000 /
                86400;
```

**[zgorizzo69 (Rigor) confirmed](https://github.com/code-423n4/2022-08-rigor-findings/issues/180)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3.5/5 |
| Rarity Score | 1.5/5 |
| Audit Firm | Code4rena |
| Protocol | Rigor Protocol |
| Report Date | N/A |
| Finders | TrungOre, Deivitto, 0x52, simon135, rbserver, auditor0517, scaraven, Lambda, smiling_heretic, hansfriese, sseefried |

### Source Links

- **Source**: https://code4rena.com/reports/2022-08-rigor
- **GitHub**: https://github.com/code-423n4/2022-08-rigor-findings/issues/180
- **Contest**: https://code4rena.com/contests/2022-08-rigor-protocol-contest

### Keywords for Search

`Rounding`

