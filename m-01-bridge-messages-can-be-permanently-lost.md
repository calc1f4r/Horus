---
# Core Classification
protocol: Nucleus_2024-12-14
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58325
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nucleus-security-review_2024-12-14.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Bridge messages can be permanently lost

### Overview


This report describes a high severity bug in the `MultiChainHyperlaneTellerWithMultiAssetSupport` contract. The contract includes a pause mechanism that can block all message handling, which creates a vulnerability in the cross-chain bridge flow. If the contract is paused during the relay period, message delivery will fail and result in the user's shares being burned on the source chain with no shares minted on the destination chain. There is currently no guarantee of indefinite retries for relayers, so there is no recovery mechanism for the lost funds. The recommendation is to handle the case where the `handle` transaction fails due to the paused state.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

The `MultiChainHyperlaneTellerWithMultiAssetSupport` contract includes a pause mechanism that blocks all message handling through the `_beforeReceive` check in the `handle` function:

```solidity
    function handle(uint32 origin, bytes32 sender, bytes calldata payload) external payable {
        _beforeReceive();
        ...
    }

    function _beforeReceive() internal virtual {
        if (isPaused) revert TellerWithMultiAssetSupport__Paused();
    }
```

This creates a vulnerability in the cross-chain bridge flow:

- User initiates a bridge transaction by calling `bridge` which burns their shares on the source chain
- Hyperlane relayer picks up the message and attempts delivery
- If the contract is paused during the relay period, message delivery will fail


Per Hyperlane docs, relayers do not guarantee infinite retries:

```
The retry count of a message determines its next delivery attempt according to an exponential backoff strategy.
Currently, there is no fixed maximum number of retries after which the relayer will cease to attempt processing a message. 
However, this is not a guarantee of indefinite retries, and operators should not rely on this as a service level agreement (SLA).
``` 
https://docs.hyperlane.xyz/docs/protocol/agents/relayer#the-submitter

It results in:
- User's shares burned on the source chain
- No shares minted on the destination chain
- Funds effectively lost with no recovery mechanism

## Recommendations

Handle the case where the `handle` transaction fails due to the paused state.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nucleus_2024-12-14 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nucleus-security-review_2024-12-14.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

