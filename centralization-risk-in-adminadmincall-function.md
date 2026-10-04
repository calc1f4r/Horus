---
# Core Classification
protocol: Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52130
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/holograph/protocol
source_link: https://www.halborn.com/audits/holograph/protocol
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
  - Halborn
---

## Vulnerability Title

Centralization risk in Admin.adminCall() function

### Overview


The `Admin` contract has a function called `adminCall()` which allows any admin to perform a low-level call on behalf of the contract. This function was misused in a previous exploit, causing a loss of $14 million. The function makes the system vulnerable to abuse by any trusted admin. It is recommended to remove this function from the contract. However, the Holograph team has accepted the risk and plans to remove the function as the protocol becomes more decentralized. 

### Original Finding Content

##### Description

The `Admin` contract implements the function `adminCall()`:

```
function adminCall(address target, bytes calldata data) external payable onlyAdmin {
  assembly {
    calldatacopy(0, data.offset, data.length)
    let result := call(gas(), target, callvalue(), 0, data.length, 0, 0)
    returndatacopy(0, 0, returndatasize())
    switch result
    case 0 {
      revert(0, returndatasize())
    }
    default {
      return(0, returndatasize())
    }
  }
}
```

This function allows any admin to perform a low-level call impersonating the actual contract that inherits from the `Admin` contract itself. Moreover, this function is the one that was abused by the privileged 0xc0ffee address that performed the Holograph exploit, last June:

*"The exploit was due to unauthorized admin access of a proxy wallet by a disgruntled former contractor who minted approximately $14 million worth of new HLG & sold it on the open market, crashing the price".*

During this exploit, the attacker, who was an admin, called the `LayerZeroModuleProxy.adminCall()` to call the `crossChainMessage()` function in the `HolographOperator` contract on behalf of the LayerZero module. This way, he managed to create jobs to mint HLG tokens.

The `adminCall()`makes the system vulnerable to abuse by any trusted admin.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:N/R:N/S:U (5.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:M/A:N/D:N/Y:N/R:N/S:U)

##### Recommendation

Consider removing the `adminCall()` function from the `Admin` contract.

##### Remediation

**RISK ACCEPTED:** The **Holograph team** accepted the risk of this finding. The **Holograph team** plans are to remove this function as the protocol grows older. This issue is known, but also by design, so the **Holograph Protocol team** can administer the protocol and upgrade as necessary. Additionally, this requires multiple parties to sign off on `adminCall` transactions via the Protocol Management Multisig on each network.

Eventually, the **Holograph team** plans to progressively decentralize and remove `adminCall` and hand over changes to the protocol to the community via governance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Protocol |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/holograph/protocol
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/holograph/protocol

### Keywords for Search

`vulnerability`

