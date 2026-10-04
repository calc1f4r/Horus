---
# Core Classification
protocol: Parcl
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48418
audit_firm: OtterSec
contest_link: https://www.parcl.co/
source_link: https://www.parcl.co/
github_link: github.com/ParclFinance/parcl-v2.

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
  - Ajay Shankar
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Reversed Funding Rate

### Overview


The funding rate function in the code is reversed, causing the majority side to receive fees instead of paying them. This results in a decrease in liquidity token price, causing losses for all token holders. The issue has been resolved in the code.

### Original Finding Content

## Parcl Finance Audit 04 | Vulnerabilities

## Funding Rate

Normally, the funding rate helps decrease skew in the pool by forcing the majority side to pay fees to the minority side. However, this is reversed in the code. The `get_funding_rate` function calculates the funding rate as follows:

```
funding_rate = (OI_long − OI_short) / OI_total / seconds_per_day
```

If long open interest is greater than short open interest, `funding_rate` increases, which in turn increases the cumulative funding rate. Now, we would expect the majority long traders to pay the funding rate fee, while the short traders will receive the fee. 

However, the `get_accrued_funding` function in `position.rs` instead sends the profits to the majority side.

```rust
pub fn get_accrued_funding(
    &self,
    exit_funding_rate: i128,
    close_amount: PreciseNumberSigned,
) -> Result<PreciseNumberSigned> {
    let funding_flow = match self.direction() {
        PositionDirection::Long => exit_funding_rate
            .checked_sub(self.entry_funding_rate)
            .ok_or(CoreError::IntegerOverflow)?,
        PositionDirection::Short => self
            .entry_funding_rate
            .checked_sub(exit_funding_rate)
            .ok_or(CoreError::IntegerOverflow)?,
    };
    let funding_rate = PreciseNumberSigned::from_decimal(
        funding_flow.abs(),
        FUNDING_RATE_PRECISION,
        funding_flow.is_positive(),
    )?;
    close_amount.checked_mul(&funding_rate)
}
```

## Proof of Concept

Consider the following scenario:

1. Long amount = 1000 (majority), Short amount = 200 (minority)
2. Since long > short, the cumulative funding rate increases. Let's assume it increases by a value of 0.1.
3. Long traders accrued funding = 0.1 * 1000 = 100
4. Short traders accrued funding = -0.1 * 200 = -20

We can see that the fee is flowing from minority to majority (short to long). Since the minority cannot provide the total funding fee received by the majority (100), this leads to a decrease in the liquidity token price as all token holders, including liquidity holders, face the loss.

## Remediation

Reverse the sign of funding rate payments.

## Patch

Resolved in `945a0af`.

```diff
@@ -437,15 +437,13 @@ impl Position {
}
pub fn get_accrued_funding_rate(&self, exit_funding_rate: i128) -> Result<PreciseNumberSigned> {
- let funding_flow = match self.direction() {
-     PositionDirection::Long => exit_funding_rate
-         .checked_sub(self.entry_funding_rate)
-         .ok_or(CoreError::IntegerOverflow)?,
-     PositionDirection::Short => self
-         .entry_funding_rate
-         .checked_sub(exit_funding_rate)
-         .ok_or(CoreError::IntegerOverflow)?,
- };
+ let funding_flow = exit_funding_rate
+     .checked_sub(self.entry_funding_rate)
+     .map(|funding_flow| match self.direction() {
+         PositionDirection::Long => -funding_flow,
+         PositionDirection::Short => funding_flow,
+     })
+     .ok_or(CoreError::IntegerOverflow)?;
PreciseNumberSigned::from_decimal(
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Parcl |
| Report Date | N/A |
| Finders | Ajay Shankar, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.parcl.co/
- **GitHub**: github.com/ParclFinance/parcl-v2.
- **Contest**: https://www.parcl.co/

### Keywords for Search

`vulnerability`

