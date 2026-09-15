---
# Core Classification
protocol: zkSync
chain: everychain
category: uncategorized
vulnerability_type: admin

# Attack Vector Details
attack_type: admin
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5748
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-zksync-v2-contest
source_link: https://code4rena.com/reports/2022-10-zksync
github_link: https://github.com/code-423n4/2022-10-zksync-findings/issues/46

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - admin

protocol_categories:
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - HE1M
  - codehacker
---

## Vulnerability Title

[M-01] `diamondCut` is not protected in case of governor's key leakage

### Overview


This bug report is about a vulnerability in the zkSync project. It is related to the governor's key being leaked, and the possibility of an attacker using this key to propose malicious diamondCuts. The attacker could then potentially front-run the governor and execute the malicious diamondCut earlier than the governor can.

The code that is affected by this vulnerability is in the DiamondCut.sol and Diamond.sol files. The vulnerable code is found at lines 46 and 277 of these files.

The impact of this vulnerability is that if the governor's key is leaked and noticed by zkSync, the attacker must wait for the notice period to execute the already proposed diamondCut with the malicious `_calldata`. However, the attacker could be smarter and execute the proposal earlier than the governor with the malicious `_calldata`. This would mean that zkSync would not have enough time to protect the project.

The proof of concept for this vulnerability is also included in the report. It is found at lines 27 and 46 of the DiamondCut.sol and Diamond.sol files.

The recommended mitigation steps for this vulnerability are that the `_calldata` should be included in the proposed diamondCut, or at least one of the security council members should approve the `_calldata` during execution of the proposal.

Overall, this bug report is about a vulnerability in the zkSync project related to the governor's key being leaked and the possibility of an attacker using this key to propose malicious diamondCuts. The code that is affected by this vulnerability is in the DiamondCut.sol and Diamond.sol files, and the recommended mitigation steps are that the `_calldata` should be included in the proposed diamondCut, or at least one of the security council members should approve the `_calldata` during execution of the proposal.

### Original Finding Content


When the governor proposes a diamondCut, governor must wait for `upgradeNoticePeriod` to be passed, or security council members have to approve the proposal to bypass the notice period, so that the governor can execute the proposal.

       require(approvedBySecurityCouncil || upgradeNoticePeriodPassed, "a6"); // notice period should expire
       require(approvedBySecurityCouncil || !diamondStorage.isFrozen, "f3");

If the governor's key is leaked and noticed by zkSync, the attacker must wait for the notice period to execute the already proposed diamondCut with the malicious `_calldata` based on the note below from zkSync, or to propose a new malicious diamondCut. For, both cases, the attacker loses time.

> NOTE: proposeDiamondCut - commits data associated with an upgrade but does not execute it. While the upgrade is associated with facetCuts and (address \_initAddress, bytes \_calldata) the upgrade will be committed to the facetCuts and \_initAddress. This is done on purpose, to leave some freedom to the governor to change calldata for the upgrade between proposing and executing it.

Since, there is a notice period (as zkSync noticed the key leakage, security council member will not approve the proposal, so bypassing the notice period is not possible), there is enough time for zkSync to apply security measures (pausing any deposit/withdraw, reporting in media to not execute any transaction in zkSync, and so on).

But, the attacker can be smarter, just before the proposal be executed by the governor (i.e. the notice period is passed or security council members approved it), the attacker executes the proposal earlier than governor with the malicious `_calldata`. In other words, the attacker front runs the governor.

Therefore, if zkSync notices the governor's key leakage beforehand, there is enough time to protect the project. But, if zkSync does not notice the governor's key leakage, the attacker can change the `_calldata` into a malicious one in the last moment so that it is not possible to protect the project.

### Proof of Concept

[Diamond.sol#L277](https://github.com/code-423n4/2022-10-zksync/blob/4db6c596931a291b17a4e0e2929adf810a4a0eed/ethereum/contracts/zksync/libraries/Diamond.sol#L277)<br>
[DiamondCut.sol#L46](https://github.com/code-423n4/2022-10-zksync/blob/4db6c596931a291b17a4e0e2929adf810a4a0eed/ethereum/contracts/zksync/facets/DiamondCut.sol#L46)

### Recommended Mitigation Steps

`_calldata` should be included in the proposed diamondCut:[DiamondCut.sol#L27](https://github.com/code-423n4/2022-10-zksync/blob/4db6c596931a291b17a4e0e2929adf810a4a0eed/ethereum/contracts/zksync/facets/DiamondCut.sol#L27).

Or, at least one of the security council members should approve the `_calldata` during execution of the proposal.

**[miladpiri (zkSync) confirmed and commented](https://github.com/code-423n4/2022-10-zksync-findings/issues/46#issuecomment-1324267775):**
 > It is a valid issue, and the fix is going to be implemented, so we confirm the issue as medium! Thanks.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-10-zksync-findings/issues/46#issuecomment-1335849634):**
 > In contrast to other reports, this shows how a malicious proposal could be injected, bypassing the timelock protection, for this reason (after consulting with a second Judge), I agree with marking it as a distinct finding and agree with Medium Severity.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | zkSync |
| Report Date | N/A |
| Finders | HE1M, codehacker |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-zksync
- **GitHub**: https://github.com/code-423n4/2022-10-zksync-findings/issues/46
- **Contest**: https://code4rena.com/contests/2022-10-zksync-v2-contest

### Keywords for Search

`Admin`

