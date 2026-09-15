---
# Core Classification
protocol: Layer N
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53993
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2
source_link: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

Positive and negative balances are not on the same scale in health calculations 

### Overview


The `add_token` function in the `mod.rs` file has a bug that causes an error when calling `AccountHealth::account_value` for a user with a single negative balance. This is because the positive and negative account values are not on the same scale. The negative account value has more decimals than the positive account value, resulting in incorrect calculations. This bug has been fixed in PR 870, and account health is now calculated in USD with basis points. 

### Original Finding Content

## Context
`mod.rs#L214-L255`

## Description
The `add_token` function computes the `positive_account_value` and `negative_account_value` for a given account. However, these two values are not on the same scale. The negative account value has more decimals than the positive account value. This will ultimately result in a Bankruptcy error when calling `AccountHealth::account_value` when a user has a single negative balance.

## Proof of Concept
The following snippet shows the impact of ETH token which has 9 decimals and an 8 decimals price feed (ETH/USD).

```rust
pub fn add_token(
    &mut self,
    balance: NonZeroBalance,
    token_decimals: Decimals,
    index_price: Price,
    token_weight: BasisPoints,
) {
    if balance.is_positive() {
        let balance: MarginNumber = (balance.get() as i128)
            .abs()
            .try_into()
            .ok()
            .expect("positive");
        let mut token_account_value = balance // decimals = token + weight + price = 9 + 4 + 8 = 21
            .mul(token_weight.value().into())
            .mul(index_price.mantissa().into());
        let rescale_decimals =
            -(index_price.decimals().get() as i32) - BasisPoints::DECIMALS as i32; // rescale_decimals = -price - weight = -8 - 4 = -12

        if rescale_decimals.is_positive() {
            token_account_value *= MarginNumber::from(10u32).pow(rescale_decimals as u32);
        }
        
        if rescale_decimals.is_negative() {
            token_account_value /=
            MarginNumber::from(10u32).pow(rescale_decimals.unsigned_abs()); // decimals = (token + weight + price) - abs(-price - weight) = token = 9
        }
        self.positive_account_value += token_account_value; // decimals = token = 9
        self.token_value += token_account_value;
    } else {
        let balance: MarginNumber = (balance.get() as i128)
            .abs()
            .try_into()
            .ok()
            .expect("positive");
        let mut borrow_account_value = balance.mul(index_price.mantissa().into()); // decimals = token + price = 9 + 8 = 17
        let rescale_decimals = token_decimals - index_price.decimals(); // rescale_decimals = token - price = 9 - 8 = 1

        if rescale_decimals.is_positive() {
            borrow_account_value *= MarginNumber::from(10u32).pow(rescale_decimals as u32); // decimals = (token + price) + (token - price) = 17 + 1 = 18
        }
        
        if rescale_decimals.is_negative() {
            borrow_account_value /=
            MarginNumber::from(10u32).pow(rescale_decimals.unsigned_abs() as u32);
        }
        
        let imf_base = 11_000u32 * BasisPoints::MAX.value() as u32
            / token_weight.value() as u32
            - BasisPoints::MAX.value() as u32;
        self.negative_account_value += borrow_account_value; // decimals = 18
        self.pon += borrow_account_value;
        self.imf += borrow_account_value.mul(imf_base.into());
    };
}
```

Then, `AccountHealth::account_value` will always return a Bankruptcy error as the `negative_account_value` is on a greater scale than `positive_account_value`.

```rust
pub fn account_value(&self) -> Result<MarginNumber, Error> {
    self.positive_account_value
        .checked_sub(&self.negative_account_value)
        .ok_or(Error::Bankruptcy)
}
```

## Recommendation
The positive and negative internal valuations of an account must be on the same scale to ensure correct calculations of the account value.

## LayerN
Fixed in PR 870.

## Cantina Managed
Fixed. Account health is calculated in USD with basis points. 1 represents 1 / 10,000 = 0.0001 USD. This fix applies for both negative and positive balances.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Layer N |
| Report Date | N/A |
| Finders | zigtur, Rikard Hjort, defsec |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2

### Keywords for Search

`vulnerability`

