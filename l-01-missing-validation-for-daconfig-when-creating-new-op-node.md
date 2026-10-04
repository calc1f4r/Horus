---
# Core Classification
protocol: PepeUnchained-November
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43903
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/PepeUnchained-security-review-November.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[L-01] Missing validation for daConfig when creating new op-node

### Overview

See description below for full details.

### Original Finding Content

When creating a new op-node, all the configuration is validated except for the `daConfig`.

```go
// Check verifies that the given configuration makes sense
func (cfg *Config) Check() error {
	...
	if err := cfg.AltDA.Check(); err != nil {
		return fmt.Errorf("altDA config error: %w", err)
	}
	if cfg.AltDA.Enabled {
		log.Warn("Alt-DA Mode is a Beta feature of the MIT licensed OP Stack.  While it has received initial review from core contributors, it is still undergoing testing, and may have bugs or other issues.")
	}
	if err := cfg.DaConfig.Check(); err != nil { // @audit no validate config
		return fmt.Errorf("da config error: %w", err)
	}
	return nil
}
```

The `Check()` function for daConfig is empty:

```go
func (c CLIConfig) Check() error {
	return nil
}
```

It's recommended to validate the config such as `RpcURL` or `FallbackMode` in the `daConfig` struct.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | PepeUnchained-November |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/PepeUnchained-security-review-November.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

