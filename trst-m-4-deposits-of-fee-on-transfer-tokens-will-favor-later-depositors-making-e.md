---
# Core Classification
protocol: Orbital Finance
chain: everychain
category: uncategorized
vulnerability_type: fee_on_transfer

# Attack Vector Details
attack_type: fee_on_transfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19031
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-28-Orbital Finance.md
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
  - fee_on_transfer

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-4 Deposits of fee-on-transfer tokens will favor later depositors, making earlier investors lose funds

### Overview


This bug report is about a calculation error in a smart contract that processes deposits. The calculation leads to incorrect results when using fee-on-transfer (tax) tokens. This is because the "before-tax" amount of the depositor is compared to the "after-tax" amount in the contract balance, which is exploitable by immediately withdrawing the shares, thus receiving more tokens than the amount contributed. 

The recommended mitigation is to compare the balance before and after the `safeTransferFrom()` call. The team response was to update the calculation of "amt" by comparing vault balances before and after the `safeTransferFrom()` call, and updating the values of "N" and "D" afterwards.

### Original Finding Content

**Description:**
When deposits are processed, the percentage of **Denominator** minted to the depositor is 
linear to the contribution, compared to the current balance. 
```solidity
         uint256 T = vlt.virtualTotalBalance(); //will be at least 1
         uint256 D = vlt.D();
         if (functions.willOverflowWhenMultiplied(amt, D)) {
            require(T > amt || T > D, "overflow");
         }
         deltaN = Arithmetic.overflowResistantFraction(amt, D, T);
             vlt.setN(msg.sender, vlt.N(msg.sender) + deltaN);
                  vlt.setD(D + deltaN); //D always kept = sum of all Ns, plus 
                    vlt.initD()
         for (uint256 i = 0; i < tkns.length; i++) {
            if (amts[i] > 0) {
         IERC20(tkns[i]).safeTransferFrom(msg.sender, vaultAddress, amts[i]);
            }
         }
```
The calculation will lead to incorrect results when using fee-on-transfer (tax) tokens. The 
"before-tax" amount of the depositor will be compared to the "after-tax" amount in the 
contract balance. It is exploitable by immediately withdrawing the shares, receiving more 
tokens than the amount contributed (unless fees are higher than the token tax). 

**Recommended mitigation:**
Compare the balance before and after the `safeTransferFrom()` call.

**Team response:**
"amt now calculated by comparing vault balances before and after safeTransferFrom. N and 
D updated afterwards. "

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Orbital Finance |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-28-Orbital Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Fee On Transfer`

