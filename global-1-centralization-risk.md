---
# Core Classification
protocol: Key Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26757
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
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
  - Guardian Audits
---

## Vulnerability Title

GLOBAL-1 | Centralization Risk

### Overview


This bug report details the potential security risks of the `admin` address, which has the ability to negatively affect the system in various ways. These include taking all esGMX, sGMX and bnGMX via `reserveSignalTransfer` and `signalTransfer`, using the `withdrawTokens` function to take any non-WETH ERC20 rewarded to the `TransferReceiver`, locking all staked Uniswap V3 LP positions by pausing the `LPStaker` contract, locking all `GMXKey` and `MPKey` stakes by pausing the `Staker` contract, and raising fees to 100% in the `Rewards` contract.

The recommendation is to ensure that the `admin` address is a multi-sig, optionally with a timelock for improved community trust and oversight, as well as attempting to limit the scope of the admin address permissions such as locking stakes and raising fees to 100%.

The resolution is that the key team has removed the pausable modifier for functions that would lock V3 positions and privileged addresses will be multi-sigs. This will help to reduce the potential risks of the `admin` address and ensure that the system is secure.

### Original Finding Content

**Description**

The `admin` address holds the ability to negatively impact the system in numerous ways, including but not limited to:

- Take all esGMX, sGMX and bnGMX via `reserveSignalTransfer` and `signalTransfer`.
- Use the `withdrawTokens` function to take any non-WETH ERC20 rewarded to the `TransferReceiver`.
- Lock all staked Uniswap V3 LP positions by pausing the `LPStaker` contract.
- Lock all `GMXKey` and `MPKey` stakes by pausing the `Staker` contract.
- Raise fees to 100% in the `Rewards` contract.

**Recommendation**

Ensure that the `admin` address is a multi-sig, optionally with a timelock for improved community trust and oversight. Attempt to limit the scope of the admin address permissions such as locking stakes and raising fees to 100%.

**Resolution**

Key Team: We have removed the pausable modifier for functions that would lock V3 positions and privileged addresses will be multi-sigs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Key Finance |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

