---
# Core Classification
protocol: Tensor Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46758
audit_firm: OtterSec
contest_link: https://tensor.foundation/
source_link: https://tensor.foundation/
github_link: https://github.com/tensor-foundation

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Improper Rent Calculation

### Overview


The bug in the price-lock program allows an attacker to deposit a large amount of SOL (a cryptocurrency) into an account, which can prevent trades from being executed. This happens because the program uses a method called get_lamports to determine the rent (a fee) for the account instead of calculating it correctly. As a result, the program may fail to execute trades and render the option worthless. The issue has been fixed in a recent update.

### Original Finding Content

## Price Lock Vulnerability Overview

`price-lock` utilizes `token_account.get_lamports` to determine the rent instead of calculating the proper rent-exemption reserve. If an attacker (maker) deposits a large amount of SOL (more than the rent-exemption reserve) into an account, it may prevent trades from executing. Since the program only expects a minimal amount for rent and does not handle large balances, the excess SOL will block the processing of the trade, rendering the option worthless.

## Example Case

In the `TAmmSellNftTokenPool`, `get_lamports` is utilized to determine the amount of SOL held in the `order_ta` account. If a very large amount of SOL is deposited into the `order_ta` account, the program will assume this large balance represents the necessary rent to perform operations. The program will fail to execute trades because the logic incorrectly assumes that the large SOL deposit represents the required rent.

### Code Snippet

```rust
fn return_rent(&self, order_seeds: [&[&[u8]]; 1]) -> Result<()> {
    let token_account_rent = self.token.order_ta.get_lamports();
    let record_rent = Rent::get()?.minimum_balance(TokenRecord::LEN);
    // For the token pool, the seller receives everything back.
    let excess_rent = 2 * token_account_rent + record_rent;
    self.trade.return_rent_for_sell(excess_rent, order_seeds)
}
```

The `return_rent` logic tries to return any excess rent from `order_ta` back to the `order_vault`. It assumes that all SOL in the `order_ta` account should be returned. Since the program does not calculate the actual rent exemption correctly, it transfers a large portion of SOL, which includes both the genuine rent and the attacker’s deposit, into the `order_vault`, resulting in improper SOL transfers and an imbalance in the vault’s holdings. Thus, the option becomes worthless, as no trades may be executed, locking up trade executions.

## Remediation

Ensure that the rent exemption reserve is properly calculated utilizing the size of the account instead of its lamports.

## Patch

Resolved in commit `84d4928`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Tensor Foundation |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://tensor.foundation/
- **GitHub**: https://github.com/tensor-foundation
- **Contest**: https://tensor.foundation/

### Keywords for Search

`vulnerability`

