---
# Core Classification
protocol: Waterusdc and Vaultka Solana Programs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52170
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/vaultka/waterusdc-and-vaultka-solana-programs
source_link: https://www.halborn.com/audits/vaultka/waterusdc-and-vaultka-solana-programs
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

RISK OF OUTDATED PRICE FEED

### Overview

See description below for full details.

### Original Finding Content

##### Description

The program relies on the Pyth oracle to retrieve the current USD prices of JLP and USDC tokens. However, the maximum age for the price feed update is currently set to 120,000 seconds (approximately 33.3 hours). If prices become outdated, such as during a Pyth oracle outage, and market volatility is high, both the user and the protocol risk losses due to incorrect exchange rates.

*waterusdc/src/lib.rs*

```
pub fn get_pyth_price_helper<'info>(price_account: &Account<'info, PriceUpdateV2>,feed_id: [u8; 32]) -> Result<u64> {
    let price_update = price_account;
    // get_price_no_older_than will fail if the price update is more than 30 seconds old
    let maximum_age: u64 = 120000; 
    // get_price_no_older_than will fail if the price update is for a different price feed.
    // This string is the id of the WIF/USD feed (close to JLP price). See https://pyth.network/developers/price-feed-ids for all available IDs.
    //let feed_id: [u8; 32] = get_feed_id_from_hex("0x4ca4beeca86f0d164160323817a4e42b10010a724c2217c6ee41b54cd4cc61fc")?;
    let price = price_update.get_price_no_older_than(&Clock::get()?, maximum_age, &feed_id)?;
    // Sample output:
    // The price is (7160106530699 ± 5129162301) * 10^-8
    msg!("The price is ({} ± {}) * 10^{}", price.price, price.conf, price.exponent);
    let final_price = price.price as u64;

    Ok(final_price)
}
```

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:M/R:P/S:U (2.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:M/R:P/S:U)

##### Recommendation

To address this issue, it is recommended to reduce the maximum age parameter.

##### Remediation

**SOLVED:** The **Vaultka team** solved the issue by decreasing the maximum age parameter to 120 seconds and thus reducing the risk of outdated price feed.

##### Remediation Hash

<https://github.com/Vaultka-Project/vaultkarust/commit/3d3ea42c829469c87f9af464b4604337054916d0>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Waterusdc and Vaultka Solana Programs |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/vaultka/waterusdc-and-vaultka-solana-programs
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/vaultka/waterusdc-and-vaultka-solana-programs

### Keywords for Search

`vulnerability`

