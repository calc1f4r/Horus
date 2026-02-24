---
# Core Classification
protocol: SushiSwap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37838
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SushiSwap-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Incorrect `chainId` used for permit EIP712 domain separator

### Overview


This report discusses a bug found in the `SushiSwapV2ERC20` code, which is used for the `permit()` function. The bug is related to the `DOMAIN_SEPARATOR` used in the code, which is incorrectly set to the Ethereum mainnet chainId instead of the TRON network chainId. This means that certain user agents, such as browsers or wallets, may not perform the signing process correctly and prevent the `permit()` function from working. The report recommends changing the code to use the correct chainId for the TRON network.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

`SushiSwapV2ERC20` implements the EIP-712 `DOMAIN_SEPARATOR` that is used for `permit()`.

```Solidity
    constructor() public {
        uint chainId;
        assembly {
        //@audit this should not be hardcoded
>>>         chainId := 1
        }
        DOMAIN_SEPARATOR = keccak256(
            abi.encode(
                keccak256(
                    "EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"
                ),
                keccak256(bytes(name)),
                keccak256(bytes("1")),
                chainId,
                address(this)
            )
        );
    }

```

However, it incorrectly set the `chainId := 1`, which is for Ethereum mainnet and not TRON network.

Based on [EIP-712](https://eips.ethereum.org/EIPS/eip-712), when the chainId does not match the active chain, the user-agent (browser/wallet) should not perform signing. This will prevent `permit()` from working as certain user agents will follow the guidelines and refuse the signing.

> uint256 chainId the [EIP-155](https://eips.ethereum.org/EIPS/eip-155) chain id. The user-agent should refuse signing if it does not match the currently active chain.

## Recommendations

```diff
    constructor() public {
        uint chainId;
        assembly {
-            chainId := 1
+            chainId := chainid
        }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | SushiSwap |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SushiSwap-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

