---
# Core Classification
protocol: Euler Labs - EVK
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35946
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
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
  - Christos Pap
  - M4rio.eth
  - Christoph Michel
  - David Chaparro
  - Emanuele Ricci
---

## Vulnerability Title

Governance.setInterestRateModel is missing sanity checks

### Overview


The bug report states that there is an issue with the Governance contract in lines 242-254. When a new interest rate model (IRM) is provided, the interest rate is reset to 0 and then updated. However, there are two cases where the transaction should revert: if the new model is the same as the current one, or if it is a faulty model that will cause an error when the interest rate is computed. This second case is not currently being handled, which means that the interest rate will remain at 0 and borrowers and lenders will not accrue any interest or rewards. To fix this, the computeInterestRate function needs to be refactored to handle this case. The recommendation is for the governance to prevent setting the IRM to a faulty or already used model. The team responsible for the contract, Euler, has acknowledged the issue and considers governance to be trusted, but they will address the issue promptly. Another team, Spearbit, has also acknowledged the issue.

### Original Finding Content

## Severity: Medium Risk

**Context:** Governance.sol#L242-L254

**Description:**  
The `Governance.setInterestRateModel` is not actively checking the user's `newModel` input that represents the new IRM rate model. When a new IRM is provided, the interest rate is reset to 0 and then updated via `computeInterestRate(vaultCache)`. The transaction should revert when:
- `newModel` is equal to the current model.
- `newModel` is a broken IRM model that will revert when `computeInterestRate` is executed.

The second case should be correctly handled, given that it violates a white paper invariant defined in the Interest Rate section:  
When a vault has `address(0)` installed as an IRM, an interest rate of 0% is assumed. If a call to the vault's IRM fails, the vault will ignore this failure and continue with the previous interest rate.  
Because the interest rate has been already reset to 0, when the new interest rate is called and reverts, it won't update the value to the old one but will remain equal to 0. In general, this case should be handled because the governance should not be able to actively set the IRM to a faulty one. Allowing such case will mean that borrowers won't accrue any interest on their open position and lenders will not accrue any rewards.  
To be able to handle this case, the `computeInterestRate` must be refactored to return if the IRM call has reverted.

**Recommendation:**  
Euler should prevent the governance from setting the new IRM model to the same one already used or to a faulty one that will revert when executed.

**Euler:**  
We acknowledge the issue. Governance is considered trusted. Even if a reverting IRM is installed, it will not be considered a malicious action, but a user error, and as such will be expected to be remedied promptly.

**Spearbit:**  
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Euler Labs - EVK |
| Report Date | N/A |
| Finders | Christos Pap, M4rio.eth, Christoph Michel, David Chaparro, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf

### Keywords for Search

`vulnerability`

