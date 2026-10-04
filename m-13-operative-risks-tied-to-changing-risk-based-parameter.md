---
# Core Classification
protocol: Apollon Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53853
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
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
  - Alex The Entreprenerd
---

## Vulnerability Title

[M-13] Operative Risks tied to changing Risk Based Parameter

### Overview


This report highlights the risks involved in updating and maintaining the Apollon platform. The main concern is that changing certain settings can lead to economic exploits, such as causing recovery mode, liquidations, or self-liquidations. The report also mentions the importance of considering the mechanisms for enacting these changes, such as pausing minting and borrowing, verifying user solvency, and having a buffer to prevent sudden changes in collateralization ratio. Additionally, the report emphasizes the need for a configured governance token, as it is used in the reserve pool and can also be vulnerable to exploitation. It is recommended to consult security researchers when making these changes to mitigate potential risks.

### Original Finding Content

**Executive Summary**

This is a collection of operative risks that come from maintaining and updating Apollon

I highly recommend you go through this list, create your own list, and ensure that at all times these risks are considered


**Updating `setCollTokenSupportedCollateralRatio` can cause multiple economic exploits**

```solidity
  function setCollTokenSupportedCollateralRatio(
    address _collTokenAddress,
    uint _supportedCollateralRatio
  ) external override onlyOwner {
    if (_supportedCollateralRatio < MCR) revert SupportedRatioUnderMCR();
    collTokenSupportedCollateralRatio[_collTokenAddress] = _supportedCollateralRatio;
    emit CollTokenSupportedCollateralRatioSet(_collTokenAddress, _supportedCollateralRatio);
  }
```

Updating this ratio can:

- Cause Recovery Mode
- Be sandwhiched to trigger Recovery Mode
- Cause Liquidations
- Be sandwhiched to cause self-liquidations

The setter itself is not a vulnerability, however, the mechanisms around changing these risk-based values are very commonly a pre-condition to Critical Severity Exploits

The most important consideration is tied to how exactly a change in Collateral Ratio would be enacted

- Can you pause minting and borrowing?
- Can you verify that all users are solvent and will remain solvent after the change?
- Can you have a buffer that will prevent actors from having a step-wise change in their Collateralization Ratio?
- Will the governance proposal be executable by anyone?
- Will you liquidate any unhealthy position as part of the proposal?

Due to the complexity, I'm flagging this as a delicate Operational Security area, however, I will not be able to provide specific advice at this time

**`setAlternativePriceFeed` can cause liquidations, self-liquidations or insolvency and bad debt**

This change could also cause positions to go from healthy to undercollateralized

The change may also be sandwiched

More importantly, if governance changes can be broadcasted by anyone, the sandwiched will not be mitigable and would be a perfect opportunity for an economic exploit

**Gov token must be configured**

Since gov token is used as part of reserve pool, then it must be configured to have some validity as collateral

**Mitigation**

Recognize the risks tied to changing these settings and plan accordingly, do consult Security Researchers at that time

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Apollon Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-22-Apollon_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

