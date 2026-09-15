---
# Core Classification
protocol: Thala Bazaar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47424
audit_firm: OtterSec
contest_link: https://github.com/bazaar-Labs/Bazaar-contracts
source_link: https://github.com/bazaar-Labs/Bazaar-contracts
github_link: https://github.com/bazaar-Labs/Bazaar-contracts

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Robert Chen
  - Matteo Oliva
  - Nicholas R.Putra
---

## Vulnerability Title

Mitigating Unexpected Abort Risks

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability in handleV3AcrossMessage Handler

The vulnerability in `handleV3AcrossMessage` handler is related to unexpected aborts during the execution of `_handleSwap`. `handleV3AcrossMessage` directly calls `_handleSwap` to perform the swap based on the provided parameters. If any unexpected issues, such as errors in `abi.decode` or other unforeseen exceptions, occur during the execution of `_handleSwap`, the entire transaction may abort.

```solidity
// Implementation of the AcrossMessageHandler interface allowing the
// SpokePool to call into the handler to conduct the swap when relaying
// a message (v3)
function handleV3AcrossMessage(address tokenSent, uint256 amount,
    address /* relayer */, bytes memory message) override external {
    _handleSwap(IERC20(tokenSent), amount, message);
}
```

## Remediation

Wrap the call to `_handleSwap` in a try/catch block. In case of an unexpected abort during the swap, the catch block should handle the situation by using `SafeERC20.safeTransfer` to transfer the original tokens back to the user.

## Patch

Resolved in `65e6d0f`.

© 2024 Otter Audits LLC. All Rights Reserved. 9/14

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Thala Bazaar |
| Report Date | N/A |
| Finders | Robert Chen, Matteo Oliva, Nicholas R.Putra |

### Source Links

- **Source**: https://github.com/bazaar-Labs/Bazaar-contracts
- **GitHub**: https://github.com/bazaar-Labs/Bazaar-contracts
- **Contest**: https://github.com/bazaar-Labs/Bazaar-contracts

### Keywords for Search

`vulnerability`

