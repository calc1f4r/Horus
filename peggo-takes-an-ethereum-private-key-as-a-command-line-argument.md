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
solodit_id: 16922
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

Peggo takes an Ethereum private key as a command-line argument

### Overview


This bug report is about an issue with Peggo's command line, which could allow an attacker to gain access to a user's Ethereum private key if they gain access to a user account on a system running Peggo. This could potentially allow the attacker to steal funds from the Ethereum account. The problem arises because in Linux, all users can inspect other users' commands and their arguments, and in many Linux distributions, the proc filesystem's hidepid=2 gid=0 mount options are not enabled by default. 

In order to prevent this issue, it is recommended to avoid using a command-line argument to pass an Ethereum private key to the Peggo program, and instead, fetch the private key from the keyring.

### Original Finding Content

## Diﬃculty: High

## Type: Cryptography

## Target: Peggo’s command line

## Description
Certain Peggo commands take an Ethereum private key (`--eth-pk`) as a command-line argument. If an attacker gained access to a user account on a system running Peggo, the attacker would also gain access to any Ethereum private key passed through the command line. The attacker could then use the key to steal funds from the Ethereum account.

```bash
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

*Figure 29.1: An example of a Peggo command line*

In Linux, all users can inspect other users’ commands and their arguments. A user can enable the proc filesystem's `hidepid=2 gid=0` mount options to hide metadata about spawned processes from users who are not members of the specified group. However, in many Linux distributions, those options are not enabled by default.

## Exploit Scenario
An attacker gains access to an unprivileged user account on a system running the Peggo orchestrator. The attacker then uses a tool such as `pspy` to inspect processes run on the system. When a user or script launches the Peggo orchestrator, the attacker steals the Ethereum private key passed to the orchestrator.

## Recommendations
Short term, avoid using a command-line argument to pass an Ethereum private key to the Peggo program. Instead, fetch the private key from the keyring.

---

*Trail of Bits 65*

*UMEE Security Assessment*

*PUBLIC*

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

