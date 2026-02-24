---
# Core Classification
protocol: Rocketpool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13447
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/04/rocketpool/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Martin Ortner
  - Dominik Muhs
  -  David Oz Kashi
---

## Vulnerability Title

Deployment - Docker containers running as root

### Overview


This bug report is about the security vulnerability of Docker containers running commands as the `root` user. This means that if an attacker is able to break into the container, they will be able to execute commands and ignore file permissions. This bug can be seen in the SmartNode Dockerfiles, which are missing `USER` instructions. To resolve this issue, the Dockerfiles should create an unprivileged user and use the `USER` instruction to switch. This will ensure that the entrypoint launching the SmartNode or the POW Proxy is secure.

### Original Finding Content

#### Description


By default, Docker containers run commands as the `root` user. This means that there is little to no resistance for an attacker who has managed to break into the container and execute commands. This effectively negates file permissions already set into the system, such as storing wallet-related information with `0600` as an attacker will most likely drop into the container as `root` already.


#### Examples


Missing `USER` instructions affect both SmartNode Dockerfiles:


**smartnode-2.5-Tokenomics/docker/rocketpool-dockerfile:L25-L36**



```
## Start from ubuntu image
FROM ubuntu:20.10

## Install OS dependencies
RUN apt-get update && apt-get install -y ca-certificates

## Copy binary
COPY --from=builder /go/bin/rocketpool /go/bin/rocketpool

## Container entry point
ENTRYPOINT ["/go/bin/rocketpool"]


```
**smartnode-2.5-Tokenomics/docker/rocketpool-pow-proxy-dockerfile:L24-L35**



```
## Start from ubuntu image
FROM ubuntu:20.10

## Install OS dependencies
RUN apt-get update && apt-get install -y ca-certificates

## Copy binary
COPY --from=builder /go/bin/rocketpool-pow-proxy /go/bin/rocketpool-pow-proxy

## Container entry point
ENTRYPOINT ["/go/bin/rocketpool-pow-proxy"]


```
#### Recommendation


In the Dockerfiles, create an unprivileged user and use the `USER` instruction to switch. Only then, the entrypoint launching the SmartNode or the POW Proxy should be defined.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Rocketpool |
| Report Date | N/A |
| Finders | Martin Ortner, Dominik Muhs,  David Oz Kashi |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/04/rocketpool/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

