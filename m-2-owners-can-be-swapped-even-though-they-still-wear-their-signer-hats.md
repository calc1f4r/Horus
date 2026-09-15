---
# Core Classification
protocol: Hats
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6722
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/48
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-hats-judging/issues/118

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - staking_pool
  - liquid_staking
  - bridge
  - yield
  - launchpad

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dug
  - minhtrng
---

## Vulnerability Title

M-2: Owners can be swapped even though they still wear their signer hats

### Overview


This bug report is about an issue found in the `HatsSignerGateBase` contract, which does not check for a change of owners post-flight. This would allow a group of malicious actors to collude and replace opposing signers with cooperating signers, even though the replaced signers still wear their signer hats. This would bypass the requirement of only being able to replace an owner if he does not wear his signer hat anymore as used in `_swapSigner`. This could lead to bypassing restrictions and performing actions that should be disallowed. The bug was found by Dug and minhtrng and manually reviewed. The recommendation to fix this issue is to perform a pre- and post-flight comparison on the safe owners, analogous to what is currently done with the modules. A discussion was also had on the issue and a pull request was created.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-hats-judging/issues/118 

## Found by 
Dug, minhtrng

## Summary

`HatsSignerGateBase` does not check for a change of owners post-flight. This allows a group of actors to collude and replace opposing signers with cooperating signers, even though the replaced signers still wear their signer hats.

## Vulnerability Detail

The `HatsSignerGateBase` performs various checks to prevent a multisig transaction to tamper with certain variables. Something that is currently not checked for in `checkAfterExecution` is a change of owners. A colluding group of malicious signers could abuse this to perform swaps of safe owners by using a delegate call to a corresponding malicious contract. This would bypass the requirement of only being able to replace an owner if he does not wear his signer hat anymore as used in `_swapSigner`:

```js
for (uint256 i; i < _ownerCount - 1;) {
    ownerToCheck = _owners[i];

    if (!isValidSigner(ownerToCheck)) {
        // prep the swap
        data = abi.encodeWithSignature(
            "swapOwner(address,address,address)",
            ...
```

## Impact

bypass restrictions and perform action that should be disallowed.

## Code Snippet

https://github.com/Hats-Protocol/hats-zodiac/blob/9455cc0957762f5dbbd8e62063d970199109b977/src/HatsSignerGateBase.sol#L507-L529

## Tool used

Manual Review

## Recommendation

Perform a pre- and post-flight comparison on the safe owners, analogous to what is currently done with the modules.

## Discussion

**spengrah**

https://github.com/Hats-Protocol/hats-zodiac/pull/5

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Hats |
| Report Date | N/A |
| Finders | Dug, minhtrng |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-hats-judging/issues/118
- **Contest**: https://app.sherlock.xyz/audits/contests/48

### Keywords for Search

`vulnerability`

