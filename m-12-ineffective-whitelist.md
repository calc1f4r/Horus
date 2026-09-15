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
solodit_id: 1482
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-aave-lens-contest
source_link: https://code4rena.com/reports/2022-02-aave-lens
github_link: https://github.com/code-423n4/2022-02-aave-lens-findings/issues/30

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

[M-12] Ineffective Whitelist

### Overview


This bug report is about the vulnerability in the code of the LensHub.sol smart contract. The code requires that the caller of the `LensHub.createProfile` function be whitelisted. However, a single whitelisted account can create as many profiles as they want and send the profile NFT to other users. This renders the whitelist ineffective. To mitigate this vulnerability, the authors suggest limiting the number of profile creations per whitelisted user or severely limiting who is allowed to create profiles, making profile creation a centralized system.

### Original Finding Content

_Submitted by cmichel_

[LensHub.sol#L146](https://github.com/code-423n4/2022-02-aave-lens/blob/aaf6c116345f3647e11a35010f28e3b90e7b4862/contracts/core/LensHub.sol#L146)<br>

Creating profiles through `LensHub.createProfile` requires the caller to be whitelisted.

```solidity
function _validateCallerIsWhitelistedProfileCreator() internal view {
    if (!_profileCreatorWhitelisted[msg.sender]) revert Errors.ProfileCreatorNotWhitelisted();
}
```

However, a single whitelisted account can create as many profiles as they want and send the profile NFT to other users.<br>
They can create unlimited profiles on behalf of other users which makes the whitelist not effective.

### Recommended Mitigation Steps

Consider limiting the number of profile creations per whitelisted user or severely limiting who is allowed to create profiles, basically making profile creation a centralized system.

**[oneski (Aave Lens) commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/30#issuecomment-1042138981):**
 > Declined, this is by design.
> 
> Governance will decide what contracts are allowed to mint via the allowlist. If governance wishes to have a more centralized system, it will only approve contracts that have numerical caps within their code.

**[Zer0dot (Aave Lens) disputed](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/30)**

**[0xleastwood (judge) marked invalid and commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/30#issuecomment-1118548551):**
 > I agree with the sponsor, I think this can already be handled by the governance strictly approving contracts with numerical caps or limiting the allowlist of who can create a profile. As such, I'm inclined to mark this as `invalid` because the recommendation can already be implemented or adhered to by the governance.

**[0xleastwood (judge) re-assessed as Medium severity and commented](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/30#issuecomment-1118566774):**
 > In light of another issue, I will mark this as a valid issue because [#66](https://github.com/code-423n4/2022-02-aave-lens-findings/issues/66) outlines a similar concern. The two issues reference different parts of the codebase so I think its fair to keep them distinct. However, I'd normally like to see a bit more detail on how non-whitelisted users can benefit from an infinite minter.



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
- **GitHub**: https://github.com/code-423n4/2022-02-aave-lens-findings/issues/30
- **Contest**: https://code4rena.com/contests/2022-02-aave-lens-contest

### Keywords for Search

`vulnerability`

