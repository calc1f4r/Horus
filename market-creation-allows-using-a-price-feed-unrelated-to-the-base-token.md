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
solodit_id: 54002
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e130af9-2dbf-41f3-8cd7-df28be1006f2
source_link: https://cdn.cantina.xyz/reports/cantina_layern_august2024.pdf
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
finders_count: 3
finders:
  - zigtur
  - Rikard Hjort
  - defsec
---

## Vulnerability Title

Market creation allows using a price feed unrelated to the base token 

### Overview

See description below for full details.

### Original Finding Content

## Market Configuration Issue

## Context
`book.rs#L407-L448`

## Description
During the creation of a market, the `base_token_id` field and the `oracle_symbol` field are passed by the admin. The "base token" is already attached to a price feed. However, the market can be created with another price feed unrelated to the one attached to the "base token". 

Due to a lack of check, the market configuration may end up with:
- `base_token.price_feed = 1`
- `market.price_feed = 2`

This will leave the market with incorrect pricing data. Moreover, there is no mechanism to disable or modify this market configuration.

## Proof of Concept
Add the following content to `nord/src/devsetup.rs` and execute `cargo test create_a_market_with_incorrect_oracle`:

```rust
mod tests {
    use super::*;

    #[tokio::test]
    async fn create_a_market_with_incorrect_oracle() {
        use std::time::SystemTime;
        let base = url::Url::parse("http://127.0.0.1:3000/").unwrap();
        let key: Vec<u8> = vec![172, 9, 116, 190, 195, 154, 23, 227, 107, 164, 166, 180, 210, 56, 255, 148,
            75, 172, 180, 120, 203, 237, 94, 252, 174, 120, 77, 123, 244, 242, 255, 128];
        let admin_key = k256::ecdsa::SigningKey::from_slice(&key).unwrap();
        let kind = ActionKind::CreateMarket(CreateMarket {
            symbol: "brokenETHUSDC".to_string(),
            oracle_symbol: "WETH/USD".to_string(), // @POC: WETH oracle
            market_type: MarketType::Spot,
            base_token_id: ETH_ASSET_ID, // @POC: ETH asset
            price_decimals: Decimals::from_repr(1),
            size_decimals: Decimals::from_repr(5),
            margins: Margins::from_basis_points(
                BasisPoints::MAX,
                BasisPoints::from_repr(5000),
                BasisPoints::from_repr(2000),
            )
            .unwrap(),
        });
        let client = reqwest::Client::new();
        let action = Action {
            timestamp: SystemTime::now().duration_since(SystemTime::UNIX_EPOCH).unwrap().as_secs().try_into().unwrap(),
            nonce: 0,
            kind,
        };
        let response = client
            .post(base.join("/action").unwrap())
            .body(sign_message(action, &admin_key))
            .send()
            .await
            .unwrap()
            .bytes()
            .await
            .unwrap();
        let receipt = engine::decode_receipt_length_delimited(&response).expect("receipt is valid");
        if let engine::proto::Receipt {
            kind: Some(engine::proto::receipt::Kind::Err(e)),
        } = receipt {
            panic!(
                "Failed to create markets: {:?}",
                engine::Error::try_from(e).unwrap()
            )
        }
        tracing::info!("{receipt:?}");
    }
}
```

## Recommendation
Add a check in `insert_market` to ensure that the Pyth Feed used by the market is the same as the Pyth Feed attached to the base token.

## LayerN
Fixed in PR 870.

## Cantina Managed
Fixed. A check to ensure that the `base_token_id` is associated with the Pyth feed has been implemented for spot markets.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

