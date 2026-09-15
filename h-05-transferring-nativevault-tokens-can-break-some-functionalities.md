---
# Core Classification
protocol: Karak-June
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38493
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-05] Transferring `NativeVault` tokens can break some functionalities

### Overview


The report discusses a bug in the NativeVault token transfer system that could cause various issues in the protocol. These include incorrect slashing of assets, inability for recipients to use the shares, and potential exploitation by node owners to prevent certain actions. The severity of the bug is high and the likelihood is medium. The report recommends overriding the transfer functions to prevent token transfers.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

`NativeVault` tokens (shares) can be transferred from the node owner to another address. This can cause different issues in the behavior of the protocol. Here there are some examples:

1. The sender of the tokens might be slashed with more assets than he should be, as his balance would have decreased, but not the `node.totalRestakedETH` value.

```
File: NativeVault.sol

    function _transferToSlashStore(address nodeOwner) internal {
        NativeVaultLib.Storage storage self = _state();
        NativeVaultLib.NativeNode storage node = self.ownerToNode[nodeOwner];

        // slashed ETH = total restaked ETH (node + beacon) - share price equivalent ETH
  @>    uint256 slashedAssets = node.totalRestakedETH - convertToAssets(balanceOf(nodeOwner));
```

2. If the recipient of the tokens is not a node owner who has enough balance in their node, he will not be able to use the shares to withdraw or do anything else, turning the shares into a useless asset.

3. If the recipient is a node owner and there has been a slashing event in the protocol, the calculation of `slashedAssets` can underflow, as his balance would have increased, but not the `node.totalRestakedETH` value. This could potentially be used by a node owner to prevent `validateExpiredSnapshot` from being executed in the case of a slashing event in one of his validators in the Beacon Chain.

## Recommendations

Override the `transfer` and `transferFrom` functions in order to disallow transfers of the token.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Karak-June |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Karak-security-review-June.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

