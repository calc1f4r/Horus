---
# Core Classification
protocol: Wido Comet Collateral Swap Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32833
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/wido-comet-collateral-swap-contracts
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Unexpected Entry Point Leads to User Impersonation

### Overview


The bug report discusses a vulnerability in two functions, `WidoCollateralSwap_Aave.executeOperation` and `WidoCollateralSwap_ERC3156.onFlashLoan`, which do not check if the sender of a flash loan is authorized and if the loan originated from the swap contract itself. This allows malicious users to impersonate others and manipulate sensitive parameters, potentially causing financial harm. The report suggests adding a `require` statement to enforce that the initiator of the flash loan is the swap contract itself. This issue has been resolved in a recent update to the code.

### Original Finding Content

Both `WidoCollateralSwap_Aave.executeOperation` and `WidoCollateralSwap_ERC3156.onFlashLoan` check if the message sender is an authorized flash loan provider but neither check to see if the loan originated from the swap contract itself. This is important because these flash loan callbacks are expecting the respective `swapCollateral` function to have encoded the correct `msg.sender` within the `params` or `data` parameter. By allowing anyone to initiate a flash loan from the correct provider and then call into the `executeOperation`/`onFlashLoan` functions, a malicious user is able to impersonate another by providing whatever bytes they want for those sensitive parameters. An example would be front-running a user who has exposed their signatures to force them to swap to different assets. Indeed, arbitrageurs would be incentivized to perform this attack.


Consider adding a `require` statement to enforce that `initiator == address(this)`.


***Update**: Resolved in [pull request #35](https://github.com/widolabs/wido-contracts/pull/35/files) at commit [f6aa4b7](https://github.com/widolabs/wido-contracts/tree/e093542385a1fc21803a5ada683a7adb2f6548af).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Wido Comet Collateral Swap Contracts |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/wido-comet-collateral-swap-contracts
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

