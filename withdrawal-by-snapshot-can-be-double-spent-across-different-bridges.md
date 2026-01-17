---
# Core Classification
protocol: Chromia - Postchain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59089
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/chromia-postchain/51a07493-6141-4d50-8316-5c66e4185de7/index.html
source_link: https://certificate.quantstamp.com/full/chromia-postchain/51a07493-6141-4d50-8316-5c66e4185de7/index.html
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
finders_count: 3
finders:
  - Ed Zulkoski
  - Ibrahim Abouzied
  - Roman Rohleder
---

## Vulnerability Title

Withdrawal by Snapshot Can Be Double-Spent Across Different Bridges

### Overview


The client has updated the documentation to warn of a vulnerability in the `withdrawBySnapshot()` function in the `TokenBridgeWithdrawBySnapshot.sol` and `hbridge/snapshot.rell` files. This vulnerability could allow users to call the function across different bridges on the same network during a mass exit. The recommendation is to avoid using `header.discriminator == allowedDiscriminator1` to prevent this issue. 

### Original Finding Content

**Update**
Marked as "Fixed" by the client. No code changes were made, instead the client updated the documentation to warn of this vulnerability. Thus the status has been marked as Acknowledged. Addressed in: `07959260996dad19474aa71906e0d27dbf28dd94`.

**File(s) affected:**`TokenBridgeWithdrawBySnapshot.sol`, `hbridge/snapshot.rell`

**Description:** In `withdrawBySnapshot()`, the `ERC20StateHeader` is validated to confirm that the withdrawal snapshot is intended for the bridge contract. A snapshot can either be authorized for any bridge on a given network, or a specific bridge on the network. The relevant code is reproduced below:

```
// assume networkId must fit in 96 bits
uint256 allowedDiscriminator1 = networkId << 160; // discriminator allows any bridge contract on the network
uint256 allowedDiscriminator2 = allowedDiscriminator1 + uint160(address(this));

require((header.discriminator == allowedDiscriminator1)
            || (header.discriminator == allowedDiscriminator2),
            "TokenBridge: invalid bridge contract");
```

`hbridge/snapshot.rell` indicates that the open discriminator is used as a default:

```
function network_id_to_discriminator(network_id: integer): big_integer {
    return big_integer(network_id) * big_integer.from_hex("1" + "00".repeat(20));
}

function maybe_create_local_erc20_state_slot(account: ft4.accounts.account, erc20_asset): state_slot? {
    ....
    if (not exists(existing_slot)) {
        existing_slot = create state_slot (
            id = get_next_state_slot_id(),
            network_id,
            recipient_address = account_address,
            type = state_slot_type.erc20,
            discriminator = network_id_to_discriminator(network_id), // Open discriminator
            local = true
        );
    }
    ....
}
```

If a mass exit is triggered across multiple bridges on the same network, then `header.discriminator == allowedDiscriminator1` would allow users to call `withdrawBySnapshot()` across different bridges.

**Recommendation:** Avoid the use of `header.discriminator == allowedDiscriminator1`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Chromia - Postchain |
| Report Date | N/A |
| Finders | Ed Zulkoski, Ibrahim Abouzied, Roman Rohleder |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/chromia-postchain/51a07493-6141-4d50-8316-5c66e4185de7/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/chromia-postchain/51a07493-6141-4d50-8316-5c66e4185de7/index.html

### Keywords for Search

`vulnerability`

