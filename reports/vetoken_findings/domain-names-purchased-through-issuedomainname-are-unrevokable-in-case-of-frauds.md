---
# Core Classification
protocol: 3DNS Inc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40784
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/fa944e34-21d5-40a7-bc05-d91c46bdb68c
source_link: https://cdn.cantina.xyz/reports/cantina_competition_3dns_mar2024.pdf
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
finders_count: 4
finders:
  - 0xhuy0512
  - Vijay
  - elhaj
  - ethan
---

## Vulnerability Title

Domain names purchased through issuedomainname() are unrevokable in case of frauds 

### Overview


The issueDomainName() function is supposed to register a domain name for users who pay with a credit card or Stripe. However, it bypasses the on-chain commitment process and locks the domain for 30 days to prevent fraud. However, there is no function to revoke the domain if the user charges back their funds. This creates an opportunity for malicious users to exploit the system by purchasing a domain, initiating a chargeback, and then selling the domain after the 30-day lock period. This undermines the purpose of locking the domain and allows for free domain names to be sold. To address this issue, it is recommended to flag domains issued through the issueDomainName() function and allow a trusted role to delete them during the lock period. This trusted role should also be limited to burning only flagged domains and only during the lock period to prevent fraud.

### Original Finding Content

## Issue Overview

## Context
(No context files were provided by the reviewer)

## Description
The `issueDomainName()` function registers a domain name for a user paying via credit card or Stripe, bypassing the on-chain commitment process. To mitigate fraud and chargeback issues that are known for this type of payment, the domain is locked for 30 days after purchase, preventing transfers during this period:

```solidity
function issueDomainName(
    bytes calldata fqdn_,
    address registrant_,
    uint64 duration_,
    Datastructures.AuthorizationSignature memory sig_
) external {
    bytes32 node_ = _calculateNode(fqdn_);
    _offchainCommitment__validate(node_, registrant_, duration_, sig_);
    _createRegistration(fqdn_, registrant_, 0, duration_);
    uint64 lockedUntil_ = uint64(block.timestamp + 30 * 24 * 60 * 60);
    RegistrarStorage.setDomainLockData(node_, lockedUntil_); // Here
    emit IssuedDomainName(node_, msg.sender);
}
```

However, locking a domain name fails to have the necessary impact in fraud cases. If the user chargebacks the funds they used to buy this domain name, the domain name should be revoked on-chain, and this user shouldn't be the owner of this domain. But because there is no function to do that, this user will remain the owner of that domain name even though they charged back their funds. This creates an opportunity for malicious users to exploit the system:

1. A malicious user purchases a domain using a credit card.
2. The user initiates a successful chargeback to reclaim the funds and get their money back.
3. The malicious user, after the 30-day lock expires, sells the domain name, getting paid for a domain that they issued for free.

## Impact
Locking a domain name doesn't prevent fraud, as someone could cheat the system and obtain free domain names. Then, they could sell these domains after waiting for the 30-day lock period.

## Recommendations
I recommend flagging domain names issued through the `issueDomainName()` function and allowing a trusted role (like the issuer role) to delete them if needed during the lock period. Additionally, to maintain trust and prevent misuse, I suggest only authorizing this trusted role to burn only flagged domain names (issued through the `issueDomainName()` function), and the burn of these domains should be limited to the lock period to effectively address potential fraud scenarios.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | 3DNS Inc |
| Report Date | N/A |
| Finders | 0xhuy0512, Vijay, elhaj, ethan |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_3dns_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/fa944e34-21d5-40a7-bc05-d91c46bdb68c

### Keywords for Search

`vulnerability`

