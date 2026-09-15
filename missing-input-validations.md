---
# Core Classification
protocol: Ethena UStb token and minting
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59101
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
source_link: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
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
finders_count: 3
finders:
  - Roman Rohleder
  - Valerian Callens
  - Rabib Islam
---

## Vulnerability Title

Missing Input Validations

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> 1.   Ack - won’t fix
> 2.   Ack - won’t fix
> 3.   Ack - uniqueness of nonce is checked in verifyNonce - won’t fix
> 4.   Ack - won’t fix

**File(s) affected:**`UStb.sol, UStbMinting.sol`

**Description:** It is important to validate inputs, even if they only come from trusted addresses, to avoid human error:

1.   In `UStb.sol`, function `initialize()`, the address `minterContract` may not be a contract;
2.   In `UStb.sol`, function `addBlacklistAddress()`, it is possible to blacklist: 

- the minter contract and this could temporarily disrupt the mint and redeem operations; 

- the address with the role `DEFAULT_ADMIN_ROLE`, and this could temporarily disrupt the operation to redistribute locked amounts;
3.   In `UStbMinting.sol`, function `verifyOrder()`, the uniqueness and the size of `Order.order_id` is not checked;
4.   In `UStbMinting.sol`, function `setUStb()`, the value of `_ustb` is not checked to be: 

- Different from `address(0x0)`; 

- Different from existing supported assets; 

- Different from existing custodian;

**Recommendation:** Consider adding the relevant checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethena UStb token and minting |
| Report Date | N/A |
| Finders | Roman Rohleder, Valerian Callens, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html

### Keywords for Search

`vulnerability`

