---
# Core Classification
protocol: Ethernote
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26719
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-05-09-Ethernote.md
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


A bug report has been made regarding the `owner` of `ethernote2` and `ethernotePresale` having authority over certain functions that could be used to disrupt the project. These functions include ceasing available notes to prevent minting, withdrawing all available wstETH, draining the contract’s Ether balance, and setting the `ethernote` address in the `EthernotePresale` to siphon user funds. The recommendation is to ensure the `owner` is a multi-sig and/or introduce a timelock for improved community oversight. 

The Ethernote team has taken steps to resolve the issue. These include adding a reentrancy guard on the `withdrawFees` function, removing the `denomination` and edition being changeable from the `UpdateNote` function, adding a constant MAX_FEE variable, adding a require check in `updateNote` and `createNote`, updating the index is not possible, and making the `owner` a multi-sig after deployment with the `transferOwnership` function. Lastly, once a note is minted, there is no ability for the team to pause redemption, only new minting.

### Original Finding Content

**Description**

The `owner` for `ethernote2` and `ethernotePresale` has authority over many functions that may be used to negatively disrupt the project.
Some possible attack vectors include:

- Ceasing the available notes to prevent minting
- Updating an edition’s validator status to prevent minting
- Calling `approveWstEth` and withdrawing all available wstETH
- Reentering on `withdrawFees` until the contract’s Ether balance is drained
- Updating a note’s `redeemFee` to 100% as it is not capped
- Updating a note’s edition index which would prevent minting due to an out-of-bounds error
- Setting the `ethernote` address in the `EthernotePresale` to siphon user funds

**Recommendation**

Ensure that the `owner` is a multi-sig and/or introduce a timelock for improved community oversight. Optionally introduce `require` statements to limit the scope of the exploits that can be carried out by the `owner`.

**Resolution**

Ethernote Team:

- Add reentrancy guard on `withdrawFees` function
- Remove `denomination` and edition being changeable from `UpdateNote` function
- Add constant MAX_FEE variable - Set currently to 501 (5%) , Add require check in `updateNote` and `createNote` - See NTE-3
- Updating index is not possible - the ID is just used to change that ID's attributes not the actual ID
- `owner` will also be a multi-sig after deployment with function `transferOwnership` function via OpenZeppelin's `Ownable.sol` contract
- Although the contract has an ACTIVE OWNERSHIP, once a note is minted, there is no ability for us to pause redemption, only new minting

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Ethernote |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-05-09-Ethernote.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

