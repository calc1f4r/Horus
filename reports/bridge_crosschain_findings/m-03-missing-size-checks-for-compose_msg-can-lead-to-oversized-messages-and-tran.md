---
# Core Classification
protocol: Kanpaipandas Lzapponft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45131
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/KanpaiPandas-LzAppONFT-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[M-03] Missing Size Checks for `compose_msg` can Lead to Oversized Messages and Transaction Failures

### Overview


This bug report describes a medium risk issue in the ONFT implementation, where there are no size checks for the `compose_msg` parameter in its encoding functions. This could lead to the creation of oversized messages, potentially causing problems with cross-chain communication and Solana transaction processing. The vulnerable code is found in the `msg_codec.rs` and `compose_msg_codec.rs` files. The impact of this bug includes cross-chain communication failures and a risk of denial of service attacks. The recommendation is to implement a maximum size limit for the `compose_msg` parameter and the team has already fixed the issue.

### Original Finding Content

## Severity

Medium Risk

## Description

The ONFT implementation currently lacks explicit size checks for the `compose_msg` parameter in its encoding functions. This omission could potentially lead to the creation of oversized messages, which might cause issues with cross-chain communication and Solana transaction processing. Solana imposes a maximum transaction size limit of 1232 bytes, and exceeding this size can result in failed transactions.

The vulnerable code resides primarily in the `msg_codec.rs` and `compose_msg_codec.rs` files:

### Affected Code Snippets

**Encoding Function** (from `msg_codec.rs`):

```rs
pub fn encode(
    send_to: [u8; 32],
    amount_sd: u64,
    sender: Pubkey,
    compose_msg: &Option<Vec<u8>>,
) -> Vec<u8> {
    if let Some(msg) = compose_msg {
        let mut encoded = Vec::with_capacity(72 + msg.len()); // 32 + 8 + 32
        encoded.extend_from_slice(&send_to);
        encoded.extend_from_slice(&amount_sd.to_be_bytes());
        encoded.extend_from_slice(sender.to_bytes().as_ref());
        encoded.extend_from_slice(&msg);
        encoded
    } else {
        let mut encoded = Vec::with_capacity(40); // 32 + 8
        encoded.extend_from_slice(&send_to);
        encoded.extend_from_slice(&amount_sd.to_be_bytes());
        encoded
    }
}
```

**Receiving Function** (from `Lz_receive.rs`):

```rs
if let Some(message) = msg_codec::compose_msg(&params.message) {
    oapp::endpoint_cpi::send_compose(
        ctx.accounts.ONft_config.endpoint_program,
        ctx.accounts.ONft_config.key(),
        &ctx.remaining_accounts[Clear::MIN_ACCOUNTS_LEN..],
        seeds,
        SendComposeParams {
            to: to_address,
            guid: params.guid,
            index: 0, // only 1 compose msg per lzReceive
            message: compose_msg_codec::encode(
                params.nonce,
                params.src_eid,
                amount_received_ld,
                &message,
            ),
        },
    )?;
}
```

Without proper size limitations, excessively large `compose_msg` values can easily breach transaction size limits, potentially resulting in DoS (Denial of Service) vulnerabilities during cross-chain operations or failed transactions on Solana.

## Impact

- **Cross-chain communication failures**: Oversized messages can prevent successful transaction execution, especially when the total transaction size exceeds Solana's 1232-byte limit.
- **DoS risk**: Repeated oversized messages could result in denial of service, as nodes might reject oversized transactions or consume excessive resources attempting to process them.

## Recommendation

Implement a maximum size limit for the `compose_msg` parameter to avoid oversized messages. Add a constant to enforce the limit during message composition.

### Sample Implementation

Define a constant for the maximum allowed size:

```rs
const MAX_MSG_SIZE: usize = 1024; // Adjust based on protocol requirements
```

Modify the `encode` function to include a size check:

```rs
pub fn encode(
    send_to: [u8; 32],
    amount_sd: u64,
    sender: Pubkey,
    compose_msg: &Option<Vec<u8>>,
) -> Result<Vec<u8>, OFTError> {
    if let Some(msg) = compose_msg {
        if msg.len() > MAX_MSG_SIZE {
            return Err(OFTError::MessageTooLarge);
        }
        let mut encoded = Vec::with_capacity(72 + msg.len());
        encoded.extend_from_slice(&send_to);
        encoded.extend_from_slice(&amount_sd.to_be_bytes());
        encoded.extend_from_slice(sender.to_bytes().as_ref());
        encoded.extend_from_slice(&msg);
        Ok(encoded)
    } else {
        let mut encoded = Vec::with_capacity(40);
        encoded.extend_from_slice(&send_to);
        encoded.extend_from_slice(&amount_sd.to_be_bytes());
        Ok(encoded)
    }
}
```

This approach ensures that message sizes remain within safe limits, preventing transaction failures or potential DoS attacks.

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Kanpaipandas Lzapponft |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/KanpaiPandas-LzAppONFT-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

