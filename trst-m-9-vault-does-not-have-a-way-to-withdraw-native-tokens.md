---
# Core Classification
protocol: Mozaic Archimedes
chain: everychain
category: uncategorized
vulnerability_type: fund_lock

# Attack Vector Details
attack_type: fund_lock
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19005
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - fund_lock

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-9 Vault does not have a way to withdraw native tokens

### Overview


This bug report is about a flaw in the Vault code which sets the LayerZero fee refund address to itself. This means that funds are stuck in the Vault and can only be used for future transactions. The recommended mitigation was to add a native token withdrawal function. The team response was that it was fixed, and the mitigation review included a new `withdraw()` function to vacate any ETH stored in the controller and vaults. However, this can be exploited since attackers can call `withdraw()` and cause a lack of native tokens, leading to messaging failure and making the system unusable.

### Original Finding Content

**Description:**
The Vault sets the LayerZero fee refund address to itself:
```solidity
        /// @notice Report snapshot of the vault to the controller.
        function reportSnapshot() public onlyBridge {
                 MozBridge.Snapshot memory _snapshot = _takeSnapshot();
             MozBridge(mozBridge).reportSnapshot(_snapshot, 
          payable(address(this)));
        }
```
However, there is no function to withdraw those funds, making them forever stuck in the vault 
only available for paying for future transactions.

**Recommended mitigation:**
Add a native token withdrawal function.

**Team response:**
Fixed.

**Mitigation review:**
The fix includes a new `withdraw()` function. Its intention is to vacate any ETH stored in the 
controller and vaults.

```solidity
        function withdraw() public {
        // get the amount of Ether stored in this contract
            uint amount = address(this).balance;
        // send all Ether to owner
        // Owner can receive Ether since the address of owner is payable
            (bool success, ) = treasury.call{value: amount}("");
                 require(success, "Controller: Failed to send Ether");
         }
```
In fact, attackers can simply call `withdraw()` to make messaging fail due to lack of native
tokens. This could be repeated in every block to make the system unusable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Trust Security |
| Protocol | Mozaic Archimedes |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-23-Mozaic Archimedes.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Fund Lock`

