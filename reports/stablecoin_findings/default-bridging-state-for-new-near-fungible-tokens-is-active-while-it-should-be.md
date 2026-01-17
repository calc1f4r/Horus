---
# Core Classification
protocol: Octopus Network Anchor
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52714
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment
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

DEFAULT BRIDGING STATE FOR NEW NEAR FUNGIBLE TOKENS IS `ACTIVE` WHILE IT SHOULD BE `CLOSED`

### Overview

See description below for full details.

### Original Finding Content

##### Description

The implementation detail document states that newly registered NEAR fungible tokens should have their bridging state set to `Closed`. However, `the register_near_fungible_token()` function in \"appchain-anchor/src/assets/near\_fungible\_tokens.rs\" registers the token with the bridging state of `Active`.

Code Location
-------------

#### appchain-anchor/src/assets/near\_fungible\_tokens.rs

```
fn register_near_fungible_token(
    &mut self,
    symbol: String,
    name: String,
    decimals: u8,
    contract_account: AccountId,
    price: U128,
) {
    self.assert_owner();
    let mut near_fungible_tokens = self.near_fungible_tokens.get().unwrap();
    assert!(
        !near_fungible_tokens.contains(&symbol),
        "Token '{}' is already registered.",
        &symbol
    );
    near_fungible_tokens.insert(&NearFungibleToken {
        metadata: FungibleTokenMetadata {
            spec: "ft-1.0.0".to_string(),
            symbol,
            name,
            decimals,
            icon: None,
            reference: None,
            reference_hash: None,
        },
        contract_account,
        price_in_usd: price,
        locked_balance: U128::from(0),
        bridging_state: BridgingState::Active,
    });
    self.near_fungible_tokens.set(&near_fungible_tokens);
}

```

##### Score

Impact: 2  
Likelihood: 2

##### Recommendation

**SOLVED**: The `Octopus Network team` solved the issue in [commit ef2219a37c5be402cec720d9db03501981c2ca80](https://github.com/octopus-network/octopus-appchain-anchor/commit/ef2219a37c5be402cec720d9db03501981c2ca80)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Octopus Network Anchor |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment

### Keywords for Search

`vulnerability`

