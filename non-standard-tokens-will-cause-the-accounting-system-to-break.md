---
# Core Classification
protocol: Venus Income Allocation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60364
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/venus-income-allocation/2a859db7-4605-44e6-9662-b0a55928ecb2/index.html
source_link: https://certificate.quantstamp.com/full/venus-income-allocation/2a859db7-4605-44e6-9662-b0a55928ecb2/index.html
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
  - Shih-Hung Wang
  - Nikita Belenkov
  - Michael Boyle
  - Mostafa Yassin
---

## Vulnerability Title

Non-Standard Tokens Will Cause the Accounting System to Break

### Overview


The client has found an issue with the `updateAssetsState()` function in the `contracts/ProtocolReserve/ProtocolShareReserve.sol` file. This function is used to keep track of newly transferred ERC20 tokens, but it does not account for certain types of tokens, like rebasing tokens, that may decrease in value. This can lead to a situation where the contract does not have enough funds to complete a transfer. The recommendation is to update the function to also account for decreases in token balance for these types of tokens.

### Original Finding Content

**Update**
The client has acknowledged the issue and commented: "We will prevent adding such non-standard ERC20 tokens that decrease the balance of an account. We have an internal guideline for new markets. Rebase tokens, or fee-on-transfer tokens, for example, are not initially supported by the protocol".

**File(s) affected:**`contracts/ProtocolReserve/ProtocolShareReserve.sol`

**Description:**`updateAssetsState()` function is usually called when a transfer of ERC20 assets has been made to the contract. It can also be called by any user of the platform. The idea behind this function is to account for newly transferred ERC20 tokens by taking the difference between the current balance of the contract and the accounted balance of the contract. It is assumed that there should be no case where the `currentBalance` will be less than the already accounted `assetReserve`.

This is not strictly the case, as if the asset is a rebasing token such as Ampelforth, the number of tokens in the contract balance will vary depending on the current market conditions and the underlying peg-keeping algorithm. These types of balance changes are also common in other types of non-standard tokens.

When `releaseFunds()` is called with the correct parameters, the income of such rebasing token would be distributed based on the last `updateAssetsState()` balance, which might not be the same as the current contract balance and could be potentially lower than the `schemaBalances` accounted balance. Leading to an issue where the last transfer will fail due to insufficient funds in the contract.

**Recommendation:**`updateAssetsState()` should also account for the decrease in contract balance for such tokens when called.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Venus Income Allocation |
| Report Date | N/A |
| Finders | Shih-Hung Wang, Nikita Belenkov, Michael Boyle, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/venus-income-allocation/2a859db7-4605-44e6-9662-b0a55928ecb2/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/venus-income-allocation/2a859db7-4605-44e6-9662-b0a55928ecb2/index.html

### Keywords for Search

`vulnerability`

