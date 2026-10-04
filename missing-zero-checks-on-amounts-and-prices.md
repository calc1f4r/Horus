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
solodit_id: 52710
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

MISSING ZERO CHECKS ON AMOUNTS AND PRICES

### Overview


This bug report is about a missing check in the code that sets the price of a token. The code is located in a file called "lib.rs" and the specific method is called "set_price_of_oct_token()". The problem is that this method does not check to make sure the price of the token is not set to zero. The impact of this bug is rated as a 4 out of 10 and the likelihood of it occurring is a 2 out of 10. The recommendation is marked as "not applicable" by the Octopus Network team because setting the token price to zero is necessary for removing a restriction on cross-chain asset transfers.

### Original Finding Content

##### Description

Checks should be implemented on amount and price values to make sure they are not set to invalid values, including setting such fields to zero. The `set_price_of_oct_token()` method implemented in the `AppchainAnchor` struct in \"appchain-anchor/src/lib.rs\" does not employ such checks to validate that the price of the OCT token does not drop to 0.

Code Location
-------------

#### appchain-anchor/src/lib.rs

```
pub fn set_price_of_oct_token(&mut self, price: U128) {
    let anchor_settings = self.anchor_settings.get().unwrap();
    assert_eq!(
        env::predecessor_account_id(),
        anchor_settings.token_price_maintainer_account,
        "Only '{}' can call this function.",
        anchor_settings.token_price_maintainer_account
    );
    let mut oct_token = self.oct_token.get().unwrap();
    oct_token.price_in_usd = price;
    self.oct_token.set(&oct_token);
}

```

##### Score

Impact: 4  
Likelihood: 2

##### Recommendation

**NOT APPLICABLE**: The `Octopus Network team` marked the issue as not applicable, as setting OCT to 0 is needed to remove the cross-chain asset transfer restriction.

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

