---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31528
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-02-01-TapiocaDAO.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

[H-01] Emergency withdrawal allows depositing again

### Overview


The reported bug is a high severity issue that affects the functionality of a smart contract called `sDaiStrategy`. After an emergency withdrawal is performed by the contract's owner, users can still deposit tokens and the mass withdrawal process will not be completed. This bug has a medium likelihood of occurring as emergency withdrawals are not a common operation. The issue lies in the last step of the `emergencyWithdraw()` function, where the contract is paused but then re-enabled in order to allow users to withdraw their tokens. However, this also enables deposits, which can cause the contract to deposit all tokens again and require another emergency withdrawal. The report suggests managing separate pause types for deposits and withdrawals or simply removing the pause for withdrawals as a solution. 

### Original Finding Content

**Severity**

**Impact:** High, tokens can be deposited again after emergency withdrawal, mass withdrawal will not be finalized

**Likelihood:** Medium, emergency withdrawal is an important admin function, but still not a usual operation

**Description**

The last step of `sDaiStrategy.emergencyWithdraw()` is the conversion to tDai and setting a pause.

```
    function emergencyWithdraw() external onlyOwner {
        paused = true; // Pause the strategy

        // Withdraw from the pool, convert to Dai and wrap it into tDai
        uint256 maxWithdraw = sDai.maxWithdraw(address(this));
        sDai.withdraw(maxWithdraw, address(this), address(this));
        dai.approve(contractAddress, maxWithdraw);
        ITDai(contractAddress).wrap(address(this), address(this), maxWithdraw);
    }
```

It means that the Owner will have to disable pause so that users can withdraw tDai (otherwise tDai will stuck on the strategy).
But if the Owner disables pause it will also enable deposits again. Moreover, the first deposit will trigger the strategy to deposit all tDai balance again, requiring `emergencyWithdraw()` again.

**Recommendations**

Consider either managing different pause types for deposits and withdrawals separately or disabling deposits after `emergencyWithdraw()` is called leaving withdrawals enabled.
Also, one of the simplest solutions would be just removing the pause for withdrawals.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-02-01-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

