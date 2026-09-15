---
# Core Classification
protocol: MobileCoin BFT
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18143
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/MobileCoinBFT.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/MobileCoinBFT.pdf
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
finders_count: 3
finders:
  - Dominik Czarnota
  - Samuel Moelius
  - Will Song
---

## Vulnerability Title

Potential denial of service due to excessive gRPC message-length limit

### Overview


A Denial of Service vulnerability has been identified in the mobilecoin/consensus/service/src/byzantine_ledger/worker.rs code. This vulnerability could allow an attacker to exhaust the server's memory by sending large requests to the mobilecoind-json server. The issue was also reported to the library's upstream repository. To prevent a Denial of Service attack, a maximum gRPC message-length limit of a few megabytes should be implemented. In the long term, any decisions to deviate from network-related defaults should be carefully weighed and only done when absolutely necessary. This will help keep systems secure and not attract unwanted attention.

### Original Finding Content

## Type: Denial of Service
**Target:** mobilecoin/consensus/service/src/byzantine_ledger/worker.rs

## Difficulty: High

## Description
The `mobilecoind-json` server sets a ~2 GB message-length limit for receiving and sending gRPC messages (figure 11.1). Setting such a big limit may allow an attacker to exhaust the server's memory by sending big requests to the `mobilecoind-json` server. We also reported an issue about an incorrectly documented `max_receive_message_len` function to the library's upstream repository on [grpc-rs#491](https://github.com/grpc/grpc-rs/issues/491).

```rust
// Set up the gRPC connection to the mobilecoind client
let env = Arc::new(grpcio::EnvBuilder::new().build());
let ch = ChannelBuilder::new(env)
    .max_receive_message_len(std::i32::MAX)
    .max_send_message_len(std::i32::MAX)
    .connect_to_uri(&config.mobilecoind_uri, &logger);
```

**Figure 11.1:** mobilecoin/mobilecoind-json/src/bin/main.rs#L646-L647

## Exploit Scenario
Alice sets up a MobileCoin node with a `mobilecoind-json` server. Eve sends big HTTP requests to Alice's server, exhausting its available memory and causing a denial of service.

## Recommendations
- **Short term:** Implement a maximum gRPC message-length limit of a few megabytes to prevent denial-of-service attacks prompted by massive server requests.
- **Long term:** Carefully consider decisions to deviate from network-related defaults. These defaults are based on the experience of the community as a whole, so deviations must be absolutely necessary and weighed carefully. This will keep your systems configured to withstand common threats and to not attract undue attention.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | MobileCoin BFT |
| Report Date | N/A |
| Finders | Dominik Czarnota, Samuel Moelius, Will Song |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/MobileCoinBFT.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/MobileCoinBFT.pdf

### Keywords for Search

`vulnerability`

