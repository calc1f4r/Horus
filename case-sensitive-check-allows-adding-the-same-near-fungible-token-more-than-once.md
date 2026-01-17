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
solodit_id: 52716
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment
source_link: https://www.halborn.com/audits/octopus-network/octopus-network-anchor-near-smart-contract-security-assessment
github_link: none

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
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

CASE SENSITIVE CHECK ALLOWS ADDING THE SAME NEAR FUNGIBLE TOKEN MORE THAN ONCE

### Overview


This bug report describes an issue in the `register_near_fungible_token()` function in the `appchain-anchor/src/assets/near_fungible_tokens.rs` file. The function only checks if the symbol of the token already exists, but the check is case-sensitive, allowing the owner to register the same token more than once. This can lead to users distributing their funds under different NEAR token contracts, reducing liquidity and rewards. The bug has been solved by the Octopus Network team in a recent commit.

### Original Finding Content

##### Description

The `register_near_fungible_token()` function in \"appchain-anchor/src/assets/near\_fungible\_tokens.rs\" only checks if the symbol of the token passed to it already exists, however the check is case-sensitive, so it can be bypassed. This allows the owner to register the same token more than once, which can lead to users distributing their funds under different NEAR token contracts instead of one, reducing liquidity and the rewards.

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

The following test case reproduces the issue and prints the two tokens that were registered with similar names:

```
#[test]
fn test_same_token_registeration(){
    let total_supply = common::to_oct_amount(TOTAL_SUPPLY);
    let (root, _, _registry, anchor, _) = common::init(total_supply, false);
    let result = call!(root, anchor.register_near_fungible_token(
        "HLB".to_string(), "Halborn".to_string(),
        2, "test1".to_string(), U128::from(1)
    ));
    result.assert_success();
    let result = call!(root, anchor.register_near_fungible_token(
        "hlb".to_string(), "halborn".to_string(),
        2, "test2".to_string(), U128::from(5)
    ));
    result.assert_success();
    let result2 = view!(anchor.get_near_fungible_tokens());
    let tokens = result2.unwrap_json::<Vec<NearFungibleToken>>();
    tokens.iter().for_each(|token|{
        println!("Token name: {}, symbol: {}", token.metadata.name, token.metadata.symbol);
    });
}

```

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

**SOLVED**: The `Octopus Network team` solved the issue in [commit ef2219a37c5be402cec720d9db03501981c2ca80](https://github.com/octopus-network/octopus-appchain-anchor/commit/ef2219a37c5be402cec720d9db03501981c2ca80)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

