---
# Core Classification
protocol: Eco Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11698
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/eco-contracts-audit/
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

protocol_categories:
  - dexes
  - yield
  - cross_chain
  - launchpad
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[P3-M05] Failed vote ends with no error

### Overview


This bug report is about the `computeVote` function of the `CurrencyGovernance` contract. This function emits a `VoteResults` event when the current contract is not the policy for `ID_CURRENCY_GOVERNANCE` or when the number of valid votes revealed is 0. This behavior is misleading and does not follow the principle of failing as early and loudly as possible. It also produces the same behavior as a successful vote that ends in a tie, which may lead to confusion. The bug report suggests emitting a `VoteFailed` event on these cases and ensuring that `computeVote` cannot be called again. However, this has not been fixed yet. The reason for this is that the result of the vote is that 0 inflation is printed, 0 tokens are distributed to each prize winner, 0 tokens are accepted for deposit certificates, and 0 interest is paid on deposit certificates. This is accurately represented by the `VoteResult(0,0,0,0)` event that the system emits, and the regular vote tally process already ensures that `computeVote` cannot be called a second time.

### Original Finding Content

###### Medium


In the [`computeVote`](https://github.com/BeamNetwork/currency/blob/51b65c5c7af455391af2bc30d13d761566d8c236/contracts/inflation/CurrencyGovernance.sol#L226) [function of the](https://github.com/BeamNetwork/currency/blob/51b65c5c7af455391af2bc30d13d761566d8c236/contracts/inflation/CurrencyGovernance.sol#L226) [`CurrencyGovernance`](https://github.com/BeamNetwork/currency/blob/51b65c5c7af455391af2bc30d13d761566d8c236/contracts/inflation/CurrencyGovernance.sol#L226) [contract](https://github.com/BeamNetwork/currency/blob/51b65c5c7af455391af2bc30d13d761566d8c236/contracts/inflation/CurrencyGovernance.sol#L226), there are two cases when a failed vote ends with no error and instead emits a `VoteResults` event:


* [The current contract is not the policy for](https://github.com/BeamNetwork/currency/blob/51b65c5c7af455391af2bc30d13d761566d8c236/contracts/inflation/CurrencyGovernance.sol#L232) [`ID_CURRENCY_GOVERNANCE`](https://github.com/BeamNetwork/currency/blob/51b65c5c7af455391af2bc30d13d761566d8c236/contracts/inflation/CurrencyGovernance.sol#L232).
* [The number of valid votes revealed is 0](https://github.com/BeamNetwork/currency/blob/51b65c5c7af455391af2bc30d13d761566d8c236/contracts/inflation/CurrencyGovernance.sol#L254).


This is misleading, and it does not follow the principle of [failing as early and loudly as possible](https://blog.zeppelin.solutions/onward-with-ethereum-smart-contract-security-97a827e47702). It also produces the same behavior as a successful vote that ends in a tie, which may lead to confusion.


Consider emitting a `VoteFailed` event on these cases and ensuring that `computeVote` cannot be called again.


***Update:** Not fixed. Eco’s statement for this issue:* 



> In both of the cases covered the result of the vote is that 0 inflation is printed, 0 tokens are distributed to each prize winner, 0 tokens are accepted for deposit certificates, and 0 interest is paid on deposit certificates. We concluded that this is accurately represented by the `VoteResult(0,0,0,0)` event that the system emits, and the regular vote tally process already ensures that `computeVote` cannot be called a second time.
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Eco Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/eco-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

