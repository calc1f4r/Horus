---
# Core Classification
protocol: Ethna LZ
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47432
audit_firm: OtterSec
contest_link: https://ethena.fi/
source_link: https://ethena.fi/
github_link: https://github.com/LayerZero-Labs/ethena-oft

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
finders_count: 2
finders:
  - James Wang
  - Robert Chen
---

## Vulnerability Title

Inconsistent Blacklisting In Token Bridging

### Overview


This bug report discusses an inconsistency in the treatment of blacklisted addresses when bridging tokens across different chains. The issue occurs when a user is not blacklisted on the source chain but is blacklisted on the destination chain. This causes the transaction to fail and the token to not be successfully credited to the blacklisted recipient. The suggested solution is to transfer the tokens to the contract owner instead of reverting the transaction. This issue has been fixed in the latest update.

### Original Finding Content

## Inconsistency in Blacklisted Addresses Treatment

There is an inconsistency in the treatment of blacklisted addresses when bridging tokens across different chains. This inconsistency is notable in the synchronization of blacklists between source and destination chains during token transfers, particularly within `StakedUSDeOFT`. Blacklists are managed independently on distinct chains. On the destination chain, `lzReceive` is tasked with managing the bridged token and calling `_credit` to credit the recipient.

```solidity
// contracts/susde/StakedUSDeOFTAdapter.sol
function _credit(
    address _to,
    uint256 _amountLD,
    uint32 _srcEid
) internal virtual override returns (uint256 amountReceivedLD) {
    bytes32 toBytes32;
    assembly {
        // @dev Pad the address with zeros
        mstore(toBytes32, _to)
        // If the recipient is blacklisted, emit an event, redistribute funds, and credit the owner
        if (blackList[toBytes32]) {
            emit RedistributeFunds(_to, _amountLD);
            return super._credit(owner(), _amountLD, _srcEid);
        } else {
            return super._credit(_to, _amountLD, _srcEid);
        }
    }
}
```

The problem arises when a user is not blacklisted on the source chain but is blacklisted on the destination chain. In the token credit process, `lzReceive` calls `_update`, which conducts a blacklist check on the recipient. Consequently, if the recipient is blacklisted on the destination chain, `_update` will revert the transaction, causing the failure of `lzReceive`. This results in an undeliverable message, as the token is not successfully credited to the blacklisted recipient.

```solidity
// contracts/susde/StakedUSDeOFT.sol
function _update(address _from, address _to, uint256 _amount) internal override {
    _checkBlackList(_from);
    _checkBlackList(_to);
    super._update(_from, _to, _amount);
}
```

© 2024 Otter Audits LLC. All Rights Reserved. 5/9

## Ethna OFT Audit 03 — Vulnerabilities Remediation

Adopt the strategy utilized in `StakedUSDeOFTAdapter`. Rather than reverting the transaction when the recipient is blacklisted, transfer the tokens to the contract owner (`oft owner`) to avoid the failure in `lzReceive`.

**Patch**  
Fixed in `6d89f44`.

© 2024 Otter Audits LLC. All Rights Reserved. 6/9

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Ethna LZ |
| Report Date | N/A |
| Finders | James Wang, Robert Chen |

### Source Links

- **Source**: https://ethena.fi/
- **GitHub**: https://github.com/LayerZero-Labs/ethena-oft
- **Contest**: https://ethena.fi/

### Keywords for Search

`vulnerability`

