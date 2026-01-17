---
# Core Classification
protocol: Atlas NEAR
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51719
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/atlas-protocol/atlas-near
source_link: https://www.halborn.com/audits/atlas-protocol/atlas-near
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
  - Halborn
---

## Vulnerability Title

Missing Input Validation May Result In Corrupted Deposits, Leading To A Loss Of Funds

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the `deposit::insert_deposit_btc` [function](https://github.com/atlasprotocol-com/atlasprotocol/blob/46760b44faf88f23ae5d1aa41d0936f7d1769f40/contract/src/modules/deposits.rs#L28) of the Atlas contract, the `minted_txn_hash` field is not validated to be an empty string:

```
pub fn insert_deposit_btc(
    &mut self,
    btc_txn_hash: String,
    btc_sender_address: String,
    receiving_chain_id: String,
    receiving_address: String,
    btc_amount: u64,
    minted_txn_hash: String,
    timestamp: u64,
    remarks: String,
    date_created: u64,
) {
    self.assert_admin();

    // Validate mandatory input fields
    assert!(!btc_txn_hash.is_empty(), "BTC transaction hash cannot be empty");
    assert!(!btc_sender_address.is_empty(), "Sender address cannot be empty");
    assert!(!receiving_chain_id.is_empty(), "Receiving chain ID cannot be empty");
    assert!(!receiving_address.is_empty(), "Receiving address cannot be empty");
    assert!(btc_amount > 0, "BTC amount must be greater than zero");
    assert!(timestamp > 0, "Timestamp must be greater than zero");
    assert!(date_created > 0, "Date created must be greater than zero");

    // Check for duplicate transaction hash
    if self.deposits.contains_key(&btc_txn_hash) {
        env::panic_str("Deposit with this transaction hash already exists");
    }

    let record = DepositRecord {
        btc_txn_hash: btc_txn_hash.clone(),
        btc_sender_address,
        receiving_chain_id,
        receiving_address,
        btc_amount,
        minted_txn_hash,
        timestamp,
        status: DEP_BTC_PENDING_MEMPOOL,
        remarks,
        date_created,
        verified_count: 0,
    };

    self.deposits.insert(btc_txn_hash, record);
}
```

  

As a result, providing a non-empty `minted_txn_hash` will make it impossible to change the deposit status to `DEP_BTC_DEPOSITED_INTO_ATLAS` later on through the `update_deposit_btc_deposited` [function](https://github.com/atlasprotocol-com/atlasprotocol/blob/46760b44faf88f23ae5d1aa41d0936f7d1769f40/contract/src/modules/deposits.rs#L101) and it will stay permanently in the `DEP_BTC_PENDING_MEMPOOL` status without a way to revert:

```
pub fn update_deposit_btc_deposited(&mut self, btc_txn_hash: String, timestamp: u64) {
        
    self.assert_admin();

    // Validate input parameters
    assert!(!btc_txn_hash.is_empty(), "BTC transaction hash cannot be empty");
    assert!(timestamp > 0, "Timestamp must be greater than zero");

    // Check if the deposit exists for the given btc_txn_hash
    if let Some(mut deposit) = self.deposits.get(&btc_txn_hash).cloned() {
        // Check all specified conditions
        if deposit.status == DEP_BTC_PENDING_MEMPOOL
            && deposit.remarks.is_empty()
            && deposit.minted_txn_hash.is_empty()
        {
            // All conditions are met, proceed to update the deposit status
            deposit.status = DEP_BTC_DEPOSITED_INTO_ATLAS;
            deposit.timestamp = timestamp;
            self.deposits.insert(btc_txn_hash.clone(), deposit);
            log!("Deposit status updated to DEP_BTC_DEPOSITED_INTO_ATLAS for btc_txn_hash: {}", btc_txn_hash);
        } else {
            // Log a message if conditions are not met
            log!("Conditions not met for updating deposit status for btc_txn_hash: {}. 
                  Status: {}, Remarks: {}, Minted txn hash: {}",
                  btc_txn_hash,
                  deposit.status,
                  deposit.remarks,
                  deposit.minted_txn_hash);
        }
    } else {
        env::panic_str("Deposit record not found");
    }
}
```

  

This will invalidate the provided BTC transaction hash, preventing the user who has potentially paid with native `BTC` from receiving `atBTC` and making it impossible for them to reclaim their `BTC` during the redemption phase.

  

Although the entire transaction sequence is likely automated from the server side, a malicious admin could frontrun the execution and call the smart contract directly with a non-empty `minted_txn_hash`, preventing users from recovering their funds.

##### Proof of Concept

**PoC Explanation:** The PoC performs the following steps:

1. Setup an instance of the Atlas contract
2. Insert a new deposit with a non-empty `minted_txn_hash` field
3. Validate the initial deposit status
4. Attempt to update the deposit status to deposited (`DEP_BTC_DEPOSITED_INTO_ATLAS`)
5. Validate that the deposit status did not change and is still set to `DEP_BTC_PENDING_MEMPOOL`

The following test was added to the `contract/tests/update_deposit_tests.rs` file:

```
#[tokio::test]
async fn test_create_corrupted_deposit() {
    // Setup atlas contract
    let mut atlas = setup_atlas();
    
    // Insert a new deposit with non-empty minted_txn_hash
    let btc_txn_hash = "btc_txn_hash".to_string();
    atlas.insert_deposit_btc(
        btc_txn_hash.clone(),
        "btc_sender_address".to_string(),
        SIGNET.to_string(),
        "receiving_address".to_string(),
        1000,
        "non-empty minted_txn_hash".to_string(),
        1234567890,
        "".to_string(),
        1234567890,
    );

    // Validate that the initial deposit status is set to DEP_BTC_PENDING_MEMPOOL
    let mut deposit = atlas.get_deposit_by_btc_txn_hash(btc_txn_hash.clone()).unwrap();
    assert_eq!(deposit.status, DEP_BTC_PENDING_MEMPOOL);

    // Update the deposit status to "Deposited"
    atlas.update_deposit_btc_deposited(btc_txn_hash.clone(), 1234567891);

    // Validate that the deposit status did not change
    deposit = atlas.get_deposit_by_btc_txn_hash(btc_txn_hash.clone()).unwrap();
    assert_eq!(deposit.status, DEP_BTC_PENDING_MEMPOOL);
}
```

  

Executing the PoC produces the following result:

![Result of test_create_corrupted_deposit](https://halbornmainframe.com/proxy/audits/images/67176af5c2200d26cd016828)

##### BVSS

[AO:S/AC:L/AX:L/R:N/S:U/C:N/A:C/I:M/D:C/Y:N (2.8)](/bvss?q=AO:S/AC:L/AX:L/R:N/S:U/C:N/A:C/I:M/D:C/Y:N)

##### Recommendation

It is recommended to ensure that the `minted_txn_hash` field is an empty string when creating a new deposit.

##### Remediation

**SOLVED**: The **Atlas Protocol team** solved the issue in the specified commit id.

##### Remediation Hash

<https://github.com/atlasprotocol-com/atlasprotocol/commit/d8fc7390e7f98a9f9e285dd26d318811b0b63fa2>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Atlas NEAR |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/atlas-protocol/atlas-near
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/atlas-protocol/atlas-near

### Keywords for Search

`vulnerability`

