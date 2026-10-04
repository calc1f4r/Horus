---
# Core Classification
protocol: Level Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60878
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
source_link: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
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
  - Jeffrey Kam
  - Mustafa Hasan
  - Rabib Islam
  - Guillermo Escobero
---

## Vulnerability Title

Upgradeable Contracts Should Disable Initialization of the Implementation

### Overview


The bug report is about a security issue in some contracts that are used for upgrading other contracts. These contracts can be initialized by anyone, which could lead to potential attacks such as social engineering or phishing. The recommendation is to call a specific function in the constructors of these contracts to prevent this issue. The bug has been fixed by implementing this recommendation in multiple affected files.

### Original Finding Content

**Update**
Fixed. For the upgradeable contracts, the recommendations were implemented. For `LVLOracle` and `LevelDevFund`, the contracts no longer inherit from `Initializable`.

**File(s) affected:**`Pool.sol`, `OrderManager.sol`, `LevelStake.sol`, `LevelDevFund.sol`, `LevelReferralController.sol`, `LevelReferralRegistry.sol`, `LevelGovernance.sol`, `LyLevel.sol`, `LVLOracle.sol`, `Treasury.sol`

**Description:** The implementation contracts behind a proxy can be initialized by any address. This is not a security problem in the sense that it impacts the system directly, as the attacker will not be able to cause any contract to self-destruct or modify any values in the proxy contracts. However, taking ownership of implementation contracts can open other attack vectors, like social engineering or phishing attacks.

**Recommendation:** Call [`_disableInitializers()`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/a34dd8bb1b8e941f6e7f65c58df0b3b994afbc16/contracts/proxy/utils/Initializable.sol#L41) in constructors to avoid the initialization of the implementation contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Level Finance |
| Report Date | N/A |
| Finders | Jeffrey Kam, Mustafa Hasan, Rabib Islam, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/level-finance/929d1708-a464-476d-86f3-7d7942faa4d2/index.html

### Keywords for Search

`vulnerability`

