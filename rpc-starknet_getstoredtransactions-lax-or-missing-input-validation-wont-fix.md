---
# Core Classification
protocol: MetaMask/Partner Snaps - StarknetSnap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 22094
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/06/metamask/partner-snaps-starknetsnap/
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
  - Martin Ortner

---

## Vulnerability Title

RPC starkNet_getStoredTransactions - Lax or Missing Input Validation  Won't Fix

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



Won’t fix. The client provided the following statement:



> 
> not fix, minor impact
> 
> 
> 


We want to note that strict input validation should be performed on all untrusted inputs for read/write and read-only methods. Just because the method is read-only now does not necessarily mean it will stay that way. Leaving untrusted inputs unchecked may lead to more severe security vulnerabilities with a growing codebase in the future.




#### Description


Potentially untrusted inputs, e.g. addresses received via RPC calls, are not always checked to conform to the StarkNet address format. For example, `requestParamsObj.senderAddress` is never checked to be a valid StarkNet address.


**packages/starknet-snap/src/getStoredTransactions.ts:L18-L26**



```
const transactions = getTransactions(
 state,
 network.chainId,
 requestParamsObj.senderAddress,
 requestParamsObj.contractAddress,
 requestParamsObj.txnType,
 undefined,
 minTimeStamp,
);

```
#### Recommendation


This method is read-only, and therefore, severity is estimated as Minor. However, it is always suggested to perform strict input validation on all user-provided inputs for read-only and read-write methods.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | MetaMask/Partner Snaps - StarknetSnap |
| Report Date | N/A |
| Finders | Martin Ortner
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/06/metamask/partner-snaps-starknetsnap/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

