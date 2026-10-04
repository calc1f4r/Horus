---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18288
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

_pullTokenInputAndPayProtocolFee() doesn't check that tokens are received

### Overview


This bug report is about a risk in the function _pullTokenInputAndPayProtocolFee() in the LSSVMPairERC20.sol file. The function does not verify that it has received the tokens after doing a safeTransferFrom(), which can lead to an issue with the fee on transfer tokens. It is also an issue with non-existing tokens, as safeTransferFrom() will not revert in that case. The proof of concept provided shows an example of how this issue can manifest.

The recommendation is to check the balance before and after the safeTransferFrom() to ensure that it is working correctly. It is also suggested to check the token addresses for tokens that are to be listed in the LSSVMPairFactory.

Sudorandom Labs and Spearbit have acknowledged the issue and the recommendation.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
`LSSVMPairERC20.sol#L34-L115`

## Description
The function `_pullTokenInputAndPayProtocolFee()` doesn't verify that it actually received the tokens after performing `safeTransferFrom()`. This can be problematic with fee-on-transfer tokens. It can also be an issue with (accidentally) non-existing tokens, as `safeTransferFrom()` won't revert on that. See the Proof of Concept below.

**Note:** Also see the issue "Malicious router mitigation may break for deflationary tokens".

```solidity
function _pullTokenInputAndPayProtocolFee(...) ... {
    ...
    _token.safeTransferFrom(msg.sender, _assetRecipient, saleAmount);
    ...
}
```

## Proof Of Concept
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.18;

import "hardhat/console.sol";
import {ERC20} from "https://raw.githubusercontent.com/transmissions11/solmate/main/src/tokens/ERC20.sol";
import {SafeTransferLib} from "https://raw.githubusercontent.com/transmissions11/solmate/main/src/utils/SafeTransferLib.sol";

contract test {
    using SafeTransferLib for ERC20;

    function t() public {
        ERC20 _token = ERC20(address(1));
        _token.safeTransferFrom(msg.sender, address(0), 100);
        console.log("after safeTransferFrom");
    }
}
```

## Recommendation
Check the balance before and after `safeTransferFrom()`. Consider verifying that the tokens exist in `LSSVMPairFactory`.

## Acknowledgments
- **Sudorandom Labs:** Acknowledged. Pair owners should verify the token addresses for tokens they want to list. Separately, fee-on-transfer tokens are beyond the current scope of the protocol, so undefined behavior is an acceptable risk.
- **Spearbit:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

