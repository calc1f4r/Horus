---
# Core Classification
protocol: Elixir Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41646
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Damilola Edwards
  - Emilio López
  - Bo Henderson
  - Artur Cygan
---

## Vulnerability Title

Redpanda exposed to the Internet

### Overview


The report discusses a high difficulty bug related to the configuration of Elixir's off-chain system architecture. This exposes the Redpanda broker to the internet, making it vulnerable to attacks. The report also mentions two specific findings related to this design decision. The potential exploit scenario involves a vulnerability being discovered and easily exploited due to the broker's accessibility. The recommendations include hiding Redpanda instances and limiting access through ACLs, as well as adding functionality to the API service. In the long term, it is advised to limit public network access and only expose necessary APIs. This report was conducted by Trail of Bits for the Elixir Protocol Security Assessment.

### Original Finding Content

## Diﬃculty: High

## Type: Conﬁguration

## Description
The consequence of Elixir’s oﬀ-chain system architecture is that the Redpanda broker is exposed to the internet, as the strategy executors connect directly to the broker. This makes Redpanda easily accessible to attackers, as they can directly try to exploit the service over the network. The consequences of this design decision also manifest in findings TOB-ELIXIR-9 and TOB-ELIXIR-20.

## Exploit Scenario
A remotely exploitable vulnerability, such as CVE-2023-50976, is discovered in Redpanda. Because Redpanda is accessible over the network to anyone, attackers easily exploit this vulnerability, potentially gaining write access or performing a denial-of-service attack.

## Recommendations
- **Short term**: Hide Redpanda instances so they are accessible only on the internal network to the relevant services. Use ACLs to limit access to the minimum required by each service. Add functionality to the API service to stream data frames to and receive order proposals from strategy executors.
- **Long term**: Always limit public network access as much as possible and expose only the necessary APIs.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Elixir Protocol |
| Report Date | N/A |
| Finders | Damilola Edwards, Emilio López, Bo Henderson, Artur Cygan |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-08-elixir-technologies-ltd-elixir-protocol-securityreview.pdf

### Keywords for Search

`vulnerability`

