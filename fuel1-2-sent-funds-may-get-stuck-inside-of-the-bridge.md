---
# Core Classification
protocol: Fuel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53519
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-04-15-Fuel.md
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
  - Hexens
---

## Vulnerability Title

[FUEL1-2] Sent funds may get stuck inside of the bridge

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** bridge-fungible-token/src/main.sw#L343-L361, bridge-fungible-token/src/main.sw#L170-L187

**Description:**

In the `bridge-fungible-token/src/main.sw` contract while processing the message there are a couple of points in the contract where if the check isn’t passing and the call will fail for one or another reason, it calls the `register_refund()` function which will allow the user to later come and claim the stuck funds.

```
fn register_refund(
    from: b256,
    token_address: b256,
    token_id: b256,
    amount: b256,
) {
    let asset = sha256((token_address, token_id));

    let previous_amount = storage.refund_amounts.get(from).get(asset).try_read().unwrap_or(ZERO_U256);
    let new_amount = amount.as_u256() + previous_amount;

    storage.refund_amounts.get(from).insert(asset, new_amount);
    log(RefundRegisteredEvent {
        from,
        token_address,
        token_id,
        amount,
    });
}
```
When bridging the tokens, the user has the ability to specify a contract which would be called as a callback so they can do further processing with the funds. However due to missing checks, there may happen a case where the called contract reverts and no refund was registered and thus the tokens will get stuck in the contract.

```
match message_data.len {
    ADDRESS_DEPOSIT_DATA_LEN => {
        transfer(message_data.to, asset_id, amount);
    },
    CONTRACT_DEPOSIT_WITHOUT_DATA_LEN => {
        transfer(message_data.to, asset_id, amount);
    },
    _ => {
        if let Identity::ContractId(id) = message_data.to {
            let dest_contract = abi(MessageReceiver, id.into());
            dest_contract
                .process_message {
                    coins: amount,
                    asset_id: asset_id.into(),
                }(msg_idx);
        };
    },
}
```

**Remediation:**  Either add another way to retrieve the stuck funds or store the refund amount before calling the `process_message` in case of a failure and then 0 it out after a successful call.

**Status:** Acknowledged

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Fuel |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-04-15-Fuel.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

