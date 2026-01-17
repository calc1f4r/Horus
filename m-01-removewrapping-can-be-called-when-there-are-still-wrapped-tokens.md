---
# Core Classification
protocol: Axelar Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25357
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-07-axelar
source_link: https://code4rena.com/reports/2022-07-axelar
github_link: https://github.com/code-423n4/2022-07-axelar-findings/issues/23

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
  - bridge
  - services
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] `removeWrapping` can be called when there are still wrapped tokens

### Overview


This bug report was submitted by Lambda, also found by 0x52 and cryptphi. It was found in the XC20Wrapper.sol#L66 code. The bug is that an owner can call the removeWrapping method, even if there are still circulating wrapped tokens. This will cause the unwrapping of those tokens to fail, as the unwrapped[wrappedToken] will be address(0). The recommended mitigation steps is to track how many wrapped tokens are in circulation, and only allow the removal of a wrapped token when there are 0 to ensure users can always unwrap. Axelar (re1ro) confirmed and commented, and the mitigation was to remove the removeWrapping method. Alex the Entreprenerd (judge) agreed with the Medium Severity, and the sponsor had confirmed and mitigated the bug.

### Original Finding Content

_Submitted by Lambda, also found by 0x52 and cryptphi_

[XC20Wrapper.sol#L66](https://github.com/code-423n4/2022-07-axelar/blob/a1205d2ba78e0db583d136f8563e8097860a110f/xc20/contracts/XC20Wrapper.sol#L66)<br>

An owner can call `removeWrapping`, even if there are still circulating wrapped tokens. This will cause the unwrapping of those tokens to fail, as `unwrapped[wrappedToken]` will be `addres(0)`.

### Recommended Mitigation Steps

Track how many wrapped tokens are in circulation, only allow the removal of a wrapped tokens when there are 0 to ensure for users that they will always be able to unwrap.

**[re1ro (Axelar) confirmed and commented](https://github.com/code-423n4/2022-07-axelar-findings/issues/23#issuecomment-1205933537):**
 > Valid observation. We will consider a different approach.
> 
> **Mitigation**<br>
> `removeWrapping` method was removed<br>
> https://github.com/axelarnetwork/axelar-xc20-wrapper/pull/4

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-07-axelar-findings/issues/23#issuecomment-1229574297):**
 > The warden has shown how the Admin can remove the mapping that allows to redeem bridged tokens, because this will cause the inability to unwrap, and can be operated by the admin, I agree with Medium Severity.
> 
> The sponsor has confirmed and they have mitigated by removing the function.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Axelar Network |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-axelar
- **GitHub**: https://github.com/code-423n4/2022-07-axelar-findings/issues/23
- **Contest**: https://code4rena.com/reports/2022-07-axelar

### Keywords for Search

`vulnerability`

