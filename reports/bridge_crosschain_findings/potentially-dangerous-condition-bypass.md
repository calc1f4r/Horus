---
# Core Classification
protocol: LayerZero Examples
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48495
audit_firm: OtterSec
contest_link: https://layerzero.network/
source_link: https://layerzero.network/
github_link: github.com/LayerZero-Labs/solidity-examples

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
  - Shiva Shankar
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Potentially Dangerous Condition Bypass

### Overview


The report discusses a bug found in two functions, virtualfunctionsNonblockingLzApp.nonblockingLzReceive()andLzApp.LzReceive(), which implement msg.sender checks before continuing execution. However, because they are marked as virtual, developers can override these checks and potentially insert malicious code without being detected. The recommended solution is to remove the virtual keyword from these functions to prevent overrides.

### Original Finding Content

## Security Advisory: Virtual Function Vulnerabilities in LzApp

The `virtual` functions `NonblockingLzApp.nonblockingLzReceive()` and `LzApp.LzReceive()` implement `msg.sender` checks inside them before continuing further execution.

## Code Snippets

**SOLIDITY**

```solidity
// LzApp.sol
require(_msgSender() == address(lzEndpoint), "LzApp: invalid endpoint caller");

// NonblockingLzApp.sol
require(_msgSender() == address(this), "NonblockingLzApp: caller must be LzApp");
```

As both functions are marked as `virtual`, developers of custom tokens inheriting these contracts can override the functionalities and bypass the above checks, or even modify checks to introduce backdoors which might be overlooked by users given their trust in publicly audited LayerZero contracts, thereby obfuscating such code.

## Remediation

To prevent this vulnerability, remove the `virtual` keyword from `LzApp.lzReceive()` and `NonblockingLzApp.nonBlockingLzReceive()` to disallow function override.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | LayerZero Examples |
| Report Date | N/A |
| Finders | Shiva Shankar, Robert Chen, OtterSec |

### Source Links

- **Source**: https://layerzero.network/
- **GitHub**: github.com/LayerZero-Labs/solidity-examples
- **Contest**: https://layerzero.network/

### Keywords for Search

`vulnerability`

