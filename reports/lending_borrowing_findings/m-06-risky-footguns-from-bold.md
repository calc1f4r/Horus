---
# Core Classification
protocol: Quill Finance Report
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53923
audit_firm: Recon Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-Quill_Finance_Report.md
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

[M-06] Risky Footguns from Bold

### Overview


This bug report highlights a potential issue with a code snippet that can be found on GitHub. The code in question can be very dangerous and has the potential to be exploited if certain precautions are not taken. The report provides a theoretical proof of this issue and suggests some ways to mitigate it. These include validating the initiator and consuming the receiver. It is important to address this issue to prevent potential exploitation.

### Original Finding Content

**Impact**
These 3 lines can be VERY dangerous

https://github.com/GalloDaSballo/quill-review/blob/8d6e4c8ed0759cea1ff0376db9fd55db864cd7e8/contracts/src/Zappers/Modules/FlashLoans/BalancerFlashLoan.sol#L46-L52

```solidity
        // This will be used by the callback below no
        receiver = IFlashLoanReceiver(msg.sender);

        vault.flashLoan(this, tokens, amounts, userData);

        // Reset receiver
        receiver = IFlashLoanReceiver(address(0));
```

The reason why this code is safe for BOLD is becasue `vault` has a Reentrancy guard

In lack of that guard many projects can get exploited

**Theoretical Proof Of Code**

https://gist.github.com/GalloDaSballo/a4dd8c2b77a64d602983152d621f55c3

**Theoretical Mitigation**

- Validate AAVE initiator
- Consume the receiver

```solidity
    function receiveFlashLoan(
        IERC20[] calldata tokens,
        uint256[] calldata amounts,
        uint256[] calldata feeAmounts,
        bytes calldata userData
    ) external override {
        require(msg.sender == address(vault), "Caller is not Vault");
        require(address(receiver) != address(0), "Flash loan not properly initiated");

        // NOTE: Validate initiator (if available) (e.g. AAVE)
        // NOTE: Why not consume receiver?
        IFlashLoanReceiver public cachedReceiver = receiver;
        receiver = IFlashLoanReceiver(address(0));
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Recon Audits |
| Protocol | Quill Finance Report |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Recon Audits/2025-03-23-Quill_Finance_Report.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

