---
# Core Classification
protocol: Babylon
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62359
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-01-17-Babylon.md
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
  - Hexens
---

## Vulnerability Title

[BAB-1] Missing zero address checks

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Informational

**Path:** TokensController.sol:setBabylonCore (L43-45), BabylonEditionsExtension.sol:setBabylonCore (L60-66), RandomProvider.sol:setBabylonCore (L46-48)

**Description:** In all of the contracts, the parameter core for the function setBabylonCore is not checked against the zero address. If this address is set to the zero address, then no one can call the functions TokensController.sol:sendItem, BabylonEditionsExtension.sol:mintEdition, RandomProvider.sol:fulfillRandomWords and RandomProvider.sol:requestRandom.
```
contract TokensController is ITokensController, Ownable {
    [..]
    function setBabylonCore(address core) external onlyOwner {
        _core = core;
    }
    [..]
}

contract RandomProvider is IRandomProvider, Ownable, VRFConsumerBaseV2 {
    [..]
    function setBabylonCore(IBabylonCore core) external onlyOwner {
        _core = core;
    }
    [..]
}

contract BabylonEditionsExtension is Ownable, IEditionsExtension, ICreatorExtensionTokenURI {
    [..]
    function setBabylonCore(address core) external onlyOwner {
        _core = core;
    }
    [..]
}
```

**Remediation:**  Add a check to validate the parameter core again the zero address. 

For example:
```
require(core != address(0), "NOT_ZERO");
```

**Status:** Fixed


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Babylon |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-01-17-Babylon.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

