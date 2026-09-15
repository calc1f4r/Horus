---
# Core Classification
protocol: stake.link
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49805
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clqf7mgla0001yeyfah59c674
source_link: none
github_link: https://github.com/Cyfrin/2023-12-stake-link

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
finders_count: 3
finders:
  - touqeershah32
  - holydevoti0n
  - draiakoo
---

## Vulnerability Title

Fee Calculation inconsistency in WrappedTokenBridge

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-stake-link/blob/549b2b8c4a5b841686fceb9c311dca9ac58225df/contracts/core/ccip/WrappedTokenBridge.sol#L126-L132">https://github.com/Cyfrin/2023-12-stake-link/blob/549b2b8c4a5b841686fceb9c311dca9ac58225df/contracts/core/ccip/WrappedTokenBridge.sol#L126-L132</a>


## Summary
The WrappedTokenBridge contract exhibits a critical issue in its fee calculation logic. Specifically, the getFee function uses a hardcoded value of `1000 ether`, leading to potentially incorrect fee assessments for CCIP transfers. As the router from chainlink also accounts for the amount of tokens to determine the charged fee.


## Vulnerability Details
The problem lies in the getFee function where it constructs a Client.EVM2AnyMessage with a hardcoded `1000 ether` amount. This approach does not accurately reflect the dynamic nature of fee calculations, which should consider the actual amount of tokens being transferred.
```
        Client.EVM2AnyMessage memory evm2AnyMessage = _buildCCIPMessage(
            address(this),
            1000 ether,
            _payNative ? address(0) : address(linkToken)
        );


        return IRouterClient(this.getRouter()).getFee(_destinationChainSelector, evm2AnyMessage);
```

## Impact
This hardcoded value can result in incorrect fee estimations, potentially leading to overcharging or undercharging users for CCIP transfers. This issue undermines the reliability and trustworthiness of the fee assessment mechanism in the contract.

## Tools Used
Manual Review

## Recommendations
Revise the getFee function to dynamically calculate fees based on the actual token amount being transferred. Ensure that the fee computation aligns with the varying amounts and conditions of each transfer, providing an accurate and fair fee estimation for users.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | stake.link |
| Report Date | N/A |
| Finders | touqeershah32, holydevoti0n, draiakoo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-stake-link
- **Contest**: https://codehawks.cyfrin.io/c/clqf7mgla0001yeyfah59c674

### Keywords for Search

`vulnerability`

