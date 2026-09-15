---
# Core Classification
protocol: BendDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36886
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-benddao
source_link: https://code4rena.com/reports/2024-07-benddao
github_link: https://github.com/code-423n4/2024-07-benddao-findings/issues/55

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
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0x73696d616f
---

## Vulnerability Title

[M-04] Unhandled request invalidation by the owner of Etherfi will lead to stuck debt

### Overview


The owner of Etherfi can cause a denial-of-service (DoS) attack on the `YieldEthStakingEtherfi` protocol by invalidating withdrawal requests without repaying the debt. There is also a way for the owner to manually claim the invalidated withdrawals, leaving them in a DoSed state. This can result in the debt never being repaid. The issue can be mitigated by creating a mechanism to handle these invalidated withdrawals or those claimed by the owner. The recommended steps are to contact Etherfi and manually handle these cases, and to trust that Etherfi will not intentionally invalidate requests. The severity level of this bug may be adjusted to Informative.

### Original Finding Content


The `owner` of Etherfi has the ability to invalidate withdrawal requests, which will DoS `YieldEthStakingEtherfi::protocolClaimWithdraw()` without ever repaying the debt. Additionally, Etherfi has a mechanism to manually claim the invalidated withdrawal, which will leave the withdraw request in a DoSed state in `YieldEthStakingEtherfi`.

### Proof of Concept

`WithdrawRequestNFT::claimWithdraw()` from Etherfi [checks](https://github.com/etherfi-protocol/smart-contracts/blob/master/src/WithdrawRequestNFT.sol#L94) that the request is valid. The owner of `WithdrawRequestNFT` may [invalidate](https://github.com/etherfi-protocol/smart-contracts/blob/master/src/WithdrawRequestNFT.sol#L174) the request at any time and claim it for [itself](https://github.com/etherfi-protocol/smart-contracts/blob/master/src/WithdrawRequestNFT.sol#L135).

Thus, as withdrawals in `YieldEthStakingEtherfi` can not be canceled and there is no way to handle invalidated withdrawals, the debt from the nft will never be repaid if the owner claims the nft for itself. If the owner validates the request later, there will still be a period of unknown duration during which it's not possible to repay the debt.

### Tools Used

Vscode, Foundry

### Recommended Mitigation Steps

Create a mechanism to handle invalidated withdrawals or withdrawals that have been claimed by the owner.

**[thorseldon (BendDAO) acknowledged and commented](https://github.com/code-423n4/2024-07-benddao-findings/issues/55#issuecomment-2301250858):**
 > After carefully reading the `WithdrawRequestNFT` code, we decided that we could only contact Etherfi and manually handle this special case of InvalidRequest according to the actual situation. Only after understanding the details can we give a reasonable solution. We can trust that Etherfi will not maliciously invalidate requests.
> 
> We suggest adjust the severity level to Informative.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BendDAO |
| Report Date | N/A |
| Finders | 0x73696d616f |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-benddao
- **GitHub**: https://github.com/code-423n4/2024-07-benddao-findings/issues/55
- **Contest**: https://code4rena.com/reports/2024-07-benddao

### Keywords for Search

`vulnerability`

