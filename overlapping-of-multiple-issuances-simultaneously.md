---
# Core Classification
protocol: Etherfuse Stablebond
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46990
audit_firm: OtterSec
contest_link: https://www.etherfuse.com/
source_link: https://www.etherfuse.com/
github_link: https://github.com/etherfuse/stablebond

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Overlapping of Multiple Issuances Simultaneously

### Overview


The report highlights a bug in the InitializeIssuance and StartIssuance instructions, which allows multiple issuances to be active at the same time. This can lead to complications in the distribution of interest and rewards among bondholders. Additionally, the CollectPayment instruction only allows payments to be collected from the latest active issuance, potentially causing funds to be locked if a new issuance starts before the previous one is settled. To fix this issue, a check should be included in the InitializeIssuance instruction to ensure no active issuance is currently running, and the CollectPayment instruction should be modified to allow payment collection from any active issuance in which the user holds bonds. This bug has been resolved in the latest update.

### Original Finding Content

## Issue with Multiple Active Issuances

The `InitializeIssuance` and `StartIssuance` instructions do not check if there is an active issuance already running under the bond before initiating a new one. This oversight allows multiple issuances to be active simultaneously. The design flaw allows the possibility of multiple overlapping issuances under the same bond. Since all issuances are tied to the same bond token, each issuance accrues interest over time. If multiple issuances overlap, it complicates the distribution of interest and rewards because the interest calculation and reward distribution mechanisms are designed to handle a single active issuance at a time.

> _ src/commands/initialize_issuance.rs rust

```rust
pub fn handle_initialize_issuance(args: InitializeIssuanceArgs) -> Result<()> {
    [...]
    let estimated_start_datetime = if bond.issuance_number == 0 {
        match args.estimated_start_datetime {
            Some(estimated_start_datetime) => estimated_start_datetime,
            None => bail!("Estimated start datetime required for first issuance"),
        }
    } else {
        match args.estimated_start_datetime {
            Some(estimated_start_datetime) => bail!(
                "Estimated start datetime only allowed for first issuance, provided {}",
                estimated_start_datetime
            ),
            None => {
                let issuance_account = find_issuance_pda(bond_account, bond.issuance_number).0;
                let data = config.client.get_account_data(&issuance_account)?;
                let issuance = Issuance::from_bytes(&data).unwrap();
                issuance.actual_start_datetime + issuance.length_in_seconds
            }
        }
    };
    [...]
}
```

With overlapping issuances, users who hold bond tokens from different issuances may receive improper or incorrect distributions of rewards. For example, interest accrued for a bond might be incorrectly allocated across multiple issuances, resulting in improper distribution among bondholders.

Furthermore, the `CollectPayment` instruction allows delegators to collect payments from a bond issuance. However, the current implementation restricts the delegator to collecting payments only from the latest active issuance. This restriction may result in a scenario where user funds are locked if a new issuance starts before the previous one is fully settled and users have purchased bonds in both issuances.

## Remediation

Include a check in `InitializeIssuance` to ensure no active issuance is currently running. Specifically, for any new issuance (`issuance_number > 0`), before initializing a new issuance, calculate the `end_time` of the latest active issuance. Ensure that the `estimated_start_datetime` of the new issuance is after this `end_time`. Also, modify the `CollectPayment` instruction to allow payment collection from any active issuance in which the user holds bonds, not just the latest.

## Patch

Resolved in #104.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Etherfuse Stablebond |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.etherfuse.com/
- **GitHub**: https://github.com/etherfuse/stablebond
- **Contest**: https://www.etherfuse.com/

### Keywords for Search

`vulnerability`

