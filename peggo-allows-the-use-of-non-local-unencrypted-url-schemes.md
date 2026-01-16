---
# Core Classification
protocol: Umee
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16923
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
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
finders_count: 2
finders:
  - Paweł Płatek
  - Dominik Czarnota
---

## Vulnerability Title

Peggo allows the use of non-local unencrypted URL schemes

### Overview


This bug report is about a vulnerability in the Peggo orchestrator command, which takes --tendermint-rpc and --cosmos-grpc flags for remote procedure call (RPC) URLs. If an unencrypted non-local URL scheme, such as http://<some-external-ip>/, is used, Peggo will not reject it or issue a warning. This could allow an attacker on the same local network to launch a man-in-the-middle attack and intercept and modify the device's network traffic.

To prevent this type of attack, users should be warned that they risk a man-in-the-middle attack if they set the RPC endpoint addresses to external hosts that use unencrypted schemes such as http://. In the short term, this is the best way to protect against this vulnerability.

### Original Finding Content

## Diﬃculty: Medium

## Type: Timing

## Target: Peggo

## Description
The Peggo orchestrator command takes `--tendermint-rpc` and `--cosmos-grpc` flags specifying Tendermint and Cosmos remote procedure call (RPC) URLs. If an unencrypted non-local URL scheme (such as `http://<some-external-ip>/`) is passed to one of those flags, Peggo will not reject it or issue a warning to the user. As a result, an attacker connected to the same local network as the system running Peggo could launch a man-in-the-middle attack, intercepting and modifying the network traffic of the device.

```
$ peggo orchestrator {gravityAddress}  \
--eth-pk=  $ETH_PK  \
--eth-rpc=  $ETH_RPC  \
--relay-batches=  true  \
--relay-valsets=  true  \
--cosmos-chain-id=...  \
--cosmos-grpc=  "tcp://..."  \
--tendermint-rpc=  "http://..."  \
--cosmos-keyring=...  \
--cosmos-keyring-dir=...  \
--cosmos-from=...
```

*Figure 30.1: The problematic flags*

## Exploit Scenario
A user sets up Peggo with an external Tendermint RPC address and an unencrypted URL scheme (`http://`). An attacker on the same network performs a man-in-the-middle attack, modifying the values sent to the Peggo orchestrator to his advantage.

## Recommendations
Short term, warn users that they risk a man-in-the-middle attack if they set the RPC endpoint addresses to external hosts that use unencrypted schemes such as `http://`. 

---

**Trail of Bits**  
**UMEE Security Assessment**  
**PUBLIC**

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Umee |
| Report Date | N/A |
| Finders | Paweł Płatek, Dominik Czarnota |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Umee.pdf

### Keywords for Search

`vulnerability`

