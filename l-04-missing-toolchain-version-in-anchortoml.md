---
# Core Classification
protocol: DesciLaunchpad_2025-02-07
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55460
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/DesciLaunchpad-security-review_2025-02-07.md
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

protocol_categories:
  - launchpad

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-04] Missing toolchain version in Anchor.toml

### Overview

See description below for full details.

### Original Finding Content

The `Anchor.toml` file does not specify the `anchor_version` or `solana_version` under the `[toolchain]` section. This can lead to compatibility issues when building or deploying the program, especially if different team members or CI/CD pipelines use different versions of Anchor or Solana.

```bash
[toolchain]

[features]
resolution = true
skip-lint = false

[programs.devnet]
desci_launchpad = "BtUNgrRufngrdEbXMnqUQjWP5LhKGGkz89U75k5tuaSj"

[registry]
url = "https://api.apr.dev"

[provider]
cluster = "Devnet"
wallet = "~/.config/solana/id.json"

[scripts]
deploy = "anchor build && solana program deploy ./target/deploy/desci_launchpad.so --skip-fee-check --max-sign-attempts 60 --use-rpc --with-compute-unit-price 50000"
test = "yarn run ts-mocha -p ./tsconfig.json -t 1000000 tests/desci-launchpad.ts"

```

Recommendation:

Add the `anchor_version` and `solana_version` to the `[toolchain]` section to ensure consistent builds and deployments.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | DesciLaunchpad_2025-02-07 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/DesciLaunchpad-security-review_2025-02-07.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

