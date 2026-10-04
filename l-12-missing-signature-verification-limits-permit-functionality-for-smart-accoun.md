---
# Core Classification
protocol: USDV_2025-03-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57865
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/USDV-security-review_2025-03-06.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-12] Missing signature verification limits permit functionality for smart accounts

### Overview

See description below for full details.

### Original Finding Content

Take a look at `ERC20RebasingPermitUpgradeable.sol#permit()`

```solidity
function permit(address _owner, address _spender,
    uint256 _value, uint256 _deadline,
    uint8 _v, bytes32 _r, bytes32 _s
) public virtual {
// ..snip
    address signer = ECDSA.recover(hash, _v, _r, _s);
    if (signer != _owner) {
        revert ERC2612InvalidSigner(signer, _owner);
    }

    _approve(_owner, _spender, _value);
}
```

As seen, the permit implementation relies solely on ECDSA.recover for signature verification, which prevents smart contract wallets and accounts from using the permit functionality. Many modern wallet implementations (like Gnosis Safe, Argent, etc.) cannot produce ECDSA signatures in the format expected by this implementation, i.e `v, r, s`, effectively excluding a significant portion of users from gas-efficient approvals, and these users would be expected to be integrated being the fact that protocol is a stablecoin.

Implement support for EIP-1271 signature verification to allow smart contract wallets to use the permit functionality.

Additionally, you can consider implementing EIP-6492 support for counterfactual contract wallets that haven't been deployed yet.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | USDV_2025-03-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/USDV-security-review_2025-03-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

