---
# Core Classification
protocol: MorpheusAI
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41611
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clrzgrole0007xtsq0gfdw8if
source_link: none
github_link: https://github.com/Cyfrin/2024-01-Morpheus

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - chainNue
  - Auditism
  - smbv1923
  - Night
  - greatlake
---

## Vulnerability Title

Create Pool in Mock Distribution is missing validations; allowing duplicates, wrong decreaseInterval value and payoutStart value

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-01-Morpheus/blob/07c900d22073911afa23b7fa69a4249ab5b713c8/contracts/mock/DistributionV2.sol#L18-L20">https://github.com/Cyfrin/2024-01-Morpheus/blob/07c900d22073911afa23b7fa69a4249ab5b713c8/contracts/mock/DistributionV2.sol#L18-L20</a>



## Summary
The `createPool` function in the mock `DistributionV2` contract lacks essential validation checks, posing potential risks related to the pool's payout start, decrease interval, and the prevention of duplicate pools. The absence of these checks could lead to unexpected behavior, disruptions, and complexities in managing the system. The recommended checks aim to enhance the robustness and security of the contract.

## Vulnerability Details
1. **Payout Start Validation Missing:**
   - The `createPool` function does not check whether `pool_.payoutStart` is set to a future timestamp. This absence allows the possibility of setting payout start to 0 or a past date.
  
2. **Decrease Interval Validation Missing:**
   - The function does not verify if `pool_.decreaseInterval` is greater than zero. This lack of validation can lead to unexpected behavior, especially if the contract performs calculations involving `decreaseInterval`.

3. **Duplicate Pool Check Missing:**
   - The function does not check for duplicate pools before adding them to the `pools` array. This absence may result in confusion and complexity in managing and maintaining the system, as duplicate pools may be inadvertently added.

4. Even there is no access control, so anyone can call this function.

## Impact
1. **Payout Start Validation Missing:**
   - The absence of a payout start validation check could allow users to set payout start to 0 or a past date. This may impact functions relying on payout start, potentially leading to unexpected behavior.

2. **Decrease Interval Validation Missing:**
   - Lack of validation for `decreaseInterval` may introduce vulnerabilities, impacting calculations and potentially causing transaction reverts or unexpected results.

3. **Duplicate Pool Check Missing:**
   - The absence of a duplicate pool check may lead to confusion and complexities in managing pools, as unintended duplicate entries could be added to the `pools` array.

4. Anyone can call this

## Tools Used
Manual review and analysis 

## Recommendations
1. **Payout Start Validation:**
   - Add the following check to ensure that `payoutStart` is set to a future timestamp:
     ```solidity
     require(pool_.payoutStart > block.timestamp, "DS: invalid payout start value");
     ```

2. **Decrease Interval Validation:**
   - Add the following check to ensure that `decreaseInterval` is greater than zero:
     ```solidity
     require(pool_.decreaseInterval > 0, "DS: invalid decrease interval");
     ```

3. **Duplicate Pool Check:**
   - Implement a check to ensure that duplicate pools are not added to the `pools` array. This can be achieved by verifying the uniqueness of pool attributes before appending a new pool.

4. Add access control.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | MorpheusAI |
| Report Date | N/A |
| Finders | chainNue, Auditism, smbv1923, Night, greatlake, oualidpro, Heba, 0xTheBlackPanther |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-01-Morpheus
- **Contest**: https://codehawks.cyfrin.io/c/clrzgrole0007xtsq0gfdw8if

### Keywords for Search

`vulnerability`

