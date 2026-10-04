---
# Core Classification
protocol: GooseFX v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47707
audit_firm: OtterSec
contest_link: https://www.goosefx.io/
source_link: https://www.goosefx.io/
github_link: https://github.com/GooseFX1/gfx-ssl-v2

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
finders_count: 4
finders:
  - OtterSec
  - Robert Chen
  - Ajay Kunapareddy
  - Thibault Marboud
---

## Vulnerability Title

Code Quality

### Overview

See description below for full details.

### Original Finding Content

## General Findings

1. In the broader code base, there are multiple places where `oracle_price_history::get_and_update_price` is called, and after calling it, there is a matching case to handle specific errors and return the latest price from history. Identical error handling and return logic are duplicated in multiple places where `get_and_update_price` is invoked. This results in unwanted redundancy in the code base.

2. In `create_pair::process`, the fee destination validation checks are placed within the main body of the function alongside other parameter validations, affecting the readability.

3. Currently, in the code base, `is_not_suspended` is consistently used throughout to check the status of `ssl_pool`. This presents a problem as `is_not_suspended` does not guarantee an 'active' status exclusively, as this condition may be true even for states such as Invalid and Uninitialized, which yields unexpected behavior.

4. The program uses `UncheckedAccount<>` in `ConfigPair` to handle optional accounts, requiring manual checks and deserialization of the accounts when passed.

    ```rust
    #[derive(Accounts)]
    pub struct ConfigPair<'info> {
        pub mint_one_fee_destination: UncheckedAccount<'info>,
        pub mint_two_fee_destination: UncheckedAccount<'info>,
        // [... other fields ...]
    }
    ```

5. It is possible to deposit or withdraw a value of zero currently, which is not an intended value while utilizing these functions, and hence, enforcing that the amount is strictly greater than zero ensures consistency with the expected behavior of deposit and withdraw operations.

6. In the context of `Swap::process`, the variable name `fee_destination` may cause confusion as it’s uncertain whether the fees are attributed to the input or output token.

## Remediation

1. Transfer this logic inside `get_and_update_price` itself instead of having error handling logic after each call to `get_and_update_price`.

2. Move these fee destination validation checks to the accounts section within `create_pair::process`.

3. Utilize `is_active` instead, which explicitly checks if the pool is active. This change ensures that the code accurately reflects the intention of checking for an actively operating pool.

4. Prefer the usage of `Optional<Account<'info, TokenAccount>>` for dealing with optional accounts, as it allows leveraging the constraints provided by the Anchor framework without manual deserialization and additional error checks.

5. Ensure that the amount parameter is strictly greater than zero to ensure consistency with the expected behavior of deposit and withdraw operations.

6. Use a purposefully chosen variable name such as `ssl_out_fee_vault` to clearly indicate that the fee vault is associated with the output token.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | GooseFX v2 |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Ajay Kunapareddy, Thibault Marboud |

### Source Links

- **Source**: https://www.goosefx.io/
- **GitHub**: https://github.com/GooseFX1/gfx-ssl-v2
- **Contest**: https://www.goosefx.io/

### Keywords for Search

`vulnerability`

