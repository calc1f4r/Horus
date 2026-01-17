---
# Core Classification
protocol: Ecosystem - DualCORE vault b14g
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50801
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/coredao/ecosystem-DualCORE-vault-b14g
source_link: https://www.halborn.com/audits/coredao/ecosystem-DualCORE-vault-b14g
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
  - Halborn
---

## Vulnerability Title

Missing Array Length Validation in reInvest

### Overview

See description below for full details.

### Original Finding Content

##### Description

In the `MergeMarketplaceStrategy` contract, the `reInvest()` function accepts three arrays (`withdrawData`, `stakeData`, and `indexReceivers`) through encoded input data but does not validate their lengths relative to each other. The function uses `indexReceivers` to validate both withdrawal and stake operations. Specifically, `indexReceivers[i]` is used for withdrawals, and `indexReceivers[i + withdrawData.length]` is used for stakes.

  

Code snippet:

```
function reInvest(bytes calldata data) external payable nonReentrant onlyDualCore {
    (bytes memory changeData, uint totalAmount) = abi.decode(data, (bytes, uint));
    {
        IMarketplace.WithdrawParam[] memory withdrawData;
        IMarketplace.StakeParam[] memory stakeData;
        uint[] memory indexReceivers;
        (withdrawData, stakeData, indexReceivers) = abi.decode(changeData, (IMarketplace.WithdrawParam[], IMarketplace.StakeParam[], uint[]));
        if (withdrawData.length > 0) {
            for (uint i = 0; i < withdrawData.length; i++) {
                require(
                    IMarketplace(marketplace).getRewardReceiverBatch(indexReceivers[i], indexReceivers[i] + 1)[0] == withdrawData[i].receiver,
                    "invalid receiver"
                );
            }
            IMarketplace(marketplace).withdrawCoreProxy(withdrawData);
        }
        if (stakeData.length > 0) {
            uint stakeValue;
            for (uint i = 0; i < stakeData.length; i++) {
                require(
                    IMarketplace(marketplace).getRewardReceiverBatch(indexReceivers[i + withdrawData.length], indexReceivers[i + withdrawData.length] + 1)[
```

  

Without explicit length validation, this can lead to several issues:

1. **Array Out-of-Bounds Access:** If `indexReceivers.length` is less than `withdrawData.length + stakeData.length`, the function may access invalid array indices, potentially causing a transaction revert.
2. **Invalid Receiver Validation:** Incorrect or incomplete input data may cause the `require` statements to fail during validation checks.

##### BVSS

[AO:S/AC:L/AX:L/R:N/S:C/C:N/A:M/I:M/D:M/Y:M (2.2)](/bvss?q=AO:S/AC:L/AX:L/R:N/S:C/C:N/A:M/I:M/D:M/Y:M)

##### Recommendation

Add explicit length validation after decoding `changeData` to ensure that the lengths of the arrays are consistent. For example:

```
require(
    indexReceivers.length == withdrawData.length + stakeData.length,
    "Invalid input array lengths"
);
```

##### Remediation

**SOLVED:** The **B14G team** fixed this finding in commit `09483cc` by implementing the recommended array length validation.

##### Remediation Hash

<https://github.com/b14glabs/contracts/commit/09483cc844e2c2327625fb3cba70c627f553c1a5>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Ecosystem - DualCORE vault b14g |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/coredao/ecosystem-DualCORE-vault-b14g
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/coredao/ecosystem-DualCORE-vault-b14g

### Keywords for Search

`vulnerability`

