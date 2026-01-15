---
# Core Classification
protocol: Etherfuse Stablebond
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47002
audit_firm: OtterSec
contest_link: https://www.etherfuse.com/
source_link: https://www.etherfuse.com/
github_link: https://github.com/etherfuse/stablebond

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Additional Safety Checks

### Overview

See description below for full details.

### Original Finding Content

## Issues and Remediation

## Issues

1. **Writable Account Checks**
   The writable account checks may not be stringent in the codebase currently, relying on CPI calls to catch errors if an account is not writable when expected. These checks are performed indirectly through error handling in CPI calls, which implies issues may not be immediately obvious or may only surface during more complex interactions.

2. **NFT Collection Mint Validation**
   In the current implementation of `purchase_order::process_create_purchase_order`, there is no validation to ensure that the `nft_collection_mint` specified in the config matches the `nft_collection_mint_account_info.key`. As a result, any NFT collection mint may be utilized.

3. **Payment Token Account Verification**
   In `PurchaseBond`, when handling payments or transactions, the system does not verify if the payment token accounts are Associated Token Accounts (ATAs). Thus, it does not ensure that the payment accounts utilized are properly set up as ATAs for the specific token involved. Therefore, the admin ends up tracking all token accounts, including those that may not be properly set up or managed, resulting in additional overhead and management complexity for the admin.

4. **Price Reliability Checks**
   The program does not ensure the reliability of the prices fetched from Pyth and Switchboard due to a lack of threshold and price confidence checks. This may result in the application utilizing inaccurate or unreliable price data, negatively affecting the overall system integrity. Additionally, the account owner check is missing in `SwitchboardV2PriceFeed::load_checked`.

   ```rust
   src/state/oracle.rs
   pub fn load_checked(
       ai: &AccountInfo,
       current_time: i64,
       max_age: u64,
   ) -> Result<Self, ErrorCode> {
       let price_feed = load_pyth_price_feed(ai)?;
       let ema_price = price_feed
           .get_ema_price_no_older_than(current_time, max_age)
           .ok_or(ErrorCode::StaleOracle)?;
       [...]
   }
   ```

## Remediation

1. Raise custom errors when writable checks fail to provide immediate feedback. This allows faster identification of issues with account permissions or state, without waiting for errors to propagate through CPI calls.

2. Check that `config.nft_collection_mint` is equal to `nft_collection_mint_account_info.key` in `purchase_order::process_create_purchase_order`.

3. Implement checks in the `PurchaseBond` process to verify that the payment token accounts are ATAs.

4. Ensure that the price data meets a minimum threshold of confidence to help avoid issues arising from incorrect or volatile price feeds. Also, add the account owner check in `SwitchboardV2PriceFeed::load_checked`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Etherfuse Stablebond |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.etherfuse.com/
- **GitHub**: https://github.com/etherfuse/stablebond
- **Contest**: https://www.etherfuse.com/

### Keywords for Search

`vulnerability`

