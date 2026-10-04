---
# Core Classification
protocol: Aave Lens
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1481
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-aave-lens-contest
source_link: https://code4rena.com/reports/2022-02-aave-lens
github_link: https://github.com/code-423n4/2022-02-aave-lens-findings/issues/22

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
  - cdp
  - services
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-11] Approvals not cleared when transferring profile

### Overview


This bug report is about the `ApprovalFollowModule.approve` function in the code linked in the report. The bug is that when an NFT (Non-fungible token) is transferred, the old approvals are not cleared. This can lead to similar issues as OpenSea not cancelling their sale offers upon NFT transfer. When the NFT is transferred back to the original owner, all the old approvals are still intact which might not be expected by the owner. The recommended mitigation step for this bug is to consider resetting all approvals upon transfer.

### Original Finding Content

_Submitted by cmichel_

[ApprovalFollowModule.sol#L32](https://github.com/code-423n4/2022-02-aave-lens/blob/aaf6c116345f3647e11a35010f28e3b90e7b4862/contracts/core/modules/follow/ApprovalFollowModule.sol#L32)<br>

The `ApprovalFollowModule.approve` function is indexed by both (`owner = IERC721(HUB).ownerOf(profileId)`, `profileId`) in case the profileId NFT is transferred.<br>
However, upon transfer, the old approvals are not cleared.

This can lead to similar issues as OpenSea not cancelling their sale offers upon NFT transfer.<br>
When the NFT is at some point transferred back to the original owner, all the old approvals are still intact which might not be expected by the owner.

### Recommended Mitigation Steps

Consider resetting all approvals upon transfer.

**[Zer0dot (Aave Lens) disputed and commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/22#issuecomment-1039792144):**
 > This is known and acceptable, users should be able to check their approvals even if they don't have the profile.
>
 > Paging @oneski if you have any input.

**[0xleastwood (judge) commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/22#issuecomment-1118551248):**
 > I think this issue is entirely valid, it should not be on the users to manage their approvals so much. It would be much safer to wipe approvals on transfers and avoid this issue altogether.
>
 > Keeping this issue open and as is.

**[donosonaumczuk (Aave Lens) commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/22#issuecomment-1125224994):**
 > I would say wiping on transfers is a bit annoying as I could be transferring my profile between two addresses I own. It would be a better alternative to wipe on re-initialization by passing a boolean `keepPreviousState` flag (or something similar).

**[Zer0dot (Aave Lens) commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/22#issuecomment-1125580300):**
 > So after some more discussion, I think the points here are valid, but we were aware of this from the beginning. There are pros and cons to maintaining state. This module will not be present at launch and further iteration can modify it. Unfortunately there is no profile NFT transfer hook in follow modules currently. As this is still in my eyes not a direct vulnerability but more a caveat of how this specific system is designed, I would no longer dispute it but I would mark it as a low severity issue.

**[0xleastwood (judge) commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/22#issuecomment-1125798004):**
 > While I agree with you that giving users the ability to save the previous state on transfer makes sense and understand that the necessary changes to do this can be put in place in the future. I think its best I stay consistent with the judging rulebook as per below:<br>
> `
> 2 — Med (M): vulns have a risk of 2 and are considered “Medium” severity when assets are not at direct risk, but the function of the protocol or its availability could be impacted, or leak value with a hypothetical attack path with stated assumptions, but external requirements.
> `
> 
> I believe the functionality of the protocol is impacted in this scenario so I think its fair to keep this as `medium` risk.

**[Zer0dot (Aave Lens) acknowledged and commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/22#issuecomment-1126098865):**
 > Sounds fair, acknowledging. This is something we're going to look into deeper for newer or updated functionality (we won't be deploying this module yet).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Aave Lens |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-aave-lens
- **GitHub**: https://github.com/code-423n4/2022-02-aave-lens-findings/issues/22
- **Contest**: https://code4rena.com/contests/2022-02-aave-lens-contest

### Keywords for Search

`vulnerability`

