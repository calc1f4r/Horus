---
# Core Classification
protocol: Genius Solana Program V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51978
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/shuttle-labs/genius-solana-program
source_link: https://www.halborn.com/audits/shuttle-labs/genius-solana-program
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

Incorrect usage of Pyth price data without considering confidence interval

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `create_order` function is responsible for creating a new order in the program. It performs several critical tasks, including:

* Validating the stability of the USDC price obtained from the Pyth Network.
* Ensuring that sufficient fees are provided for cross-chain operations.
* Initializing and populating the order with details such as the source and destination chains, token amounts, and involved parties.
* Transferring USDC from the user’s token account to a vault account for order processing.

  

During the price validation step, the function fetches the USDC price using the Pyth price feed and adjusts it based on the feed's `exponent` value:

  

`create_order.rs`:

```
        msg!("deposit USDC amount: {:?}", amount);
        let price_update = &mut ctx.accounts.price_update;
        let feed_id: [u8; 32] = get_feed_id_from_hex(FEED_ID)?;
        let price = price_update.get_price_no_older_than(&Clock::get()?, MAXIMUM_AGE, &feed_id)?;

        // Adjust price to floating-point by scaling with 10^exponent
        let adjusted_price: f64 = (price.price as f64) * 10f64.powi(price.exponent);
```

  

However, this implementation does not consider the `conf` (confidence interval) parameter provided by Pyth, which represents the uncertainty range in the reported price. Ignoring `conf` might lead to decisions based on potentially unreliable price data, especially during periods of high market volatility.

By not incorporating the `conf` parameter, the program exposes itself to risks where the USDC/USD price might appear stable but has significant uncertainty. This could lead to:

  

1. **Depeg Exploitation:** If USDC experiences a depeg and the confidence interval (`conf`) is not considered, the price could appear valid while being inaccurate due to high uncertainty. Users on the Solana network could exploit this by exchanging depegged USDC tokens on Solana for more valuable tokens on another network, effectively transferring the depeg losses to the program and its users.
2. **Systemic Risks Across Chains:** As the function facilitates cross-chain operations, overlooking the confidence interval might propagate incorrect exchange rates between networks, leading to financial imbalances or exploits.
3. **Inaccurate Price Validation:** In volatile market conditions, large `conf` values signal unreliable data. Ignoring this parameter leaves the program vulnerable to decisions based on incomplete or misleading price information.

##### BVSS

[AO:A/AC:L/AX:H/R:N/S:U/C:N/A:N/I:N/D:C/Y:N (3.3)](/bvss?q=AO:A/AC:L/AX:H/R:N/S:U/C:N/A:N/I:N/D:C/Y:N)

##### Recommendation

Modify the price validation logic to incorporate the `conf` parameter. This ensures that the price used for validation is reliable and falls within an acceptable range. For example:

  

`create_order.rs`:

```
let lower_bound = (price.price - price.conf) as f64 * 10f64.powi(price.exponent);
let upper_bound = (price.price + price.conf) as f64 * 10f64.powi(price.exponent);

// Validate price bounds
require!(lower_bound > 0.99, GeniusError::StableCoinPriceTooLow);
require!(upper_bound < MAX_ACCEPTABLE_PRICE, GeniusError::StableCoinPriceTooHigh);
```

  

By incorporating the confidence interval, the program can assess the validity of the price more accurately, mitigating risks associated with volatile or unreliable price data.

##### Remediation

**SOLVED:** The **Genius team** solved the issue by adding the conf parameter to the calculation.

##### Remediation Hash

<https://github.com/Shuttle-Labs/genius-contracts-solana/commit/5f4b23d9c13ccb3ed2c2170b880654c8fd37d384#diff-e7131506b585aedb77fa151a6afbe88eb8dc131130509202b8dbbcbc9f878095>

##### References

<https://docs.pyth.network/price-feeds/best-practices#confidence-intervals>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Genius Solana Program V2 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/shuttle-labs/genius-solana-program
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/shuttle-labs/genius-solana-program

### Keywords for Search

`vulnerability`

