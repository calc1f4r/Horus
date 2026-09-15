---
# Core Classification
protocol: Polygonzkevm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49757
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
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
  - Hexens
---

## Vulnerability Title

5. BUG IN MAXMEM HANDLING CAN HALT THE BATCH VERIFICATION

### Overview


Severity: High

Path: main.zkasm, create-terminate-context.zkasm

Description:

The zkEVM ROM has a bug where the MAXMEM register, used to set the biggest offset of memory, is not being reset after the first step of execution. This allows an attacker to manipulate the MAXMEM value and potentially cause a denial of service attack. The bug is caused by a mismatch between the MAX_MEM_EXPANSION_BYTES limit and the diffMem plookup, which can be exploited by an illicit actor to send a transaction to the trusted sequencer. This issue has been fixed by changing the diffMem plookup or shrinking the MAX_MEM_EXPANSION_BYTES limit.

Remediation: To fix this issue, the diffMem plookup can be changed to BITS17 or the MAX_MEM_EXPANSION_BYTES limit can be reduced to 2^21-32.

Status: Fixed

### Original Finding Content

**Severity:**  High

**Path:** main.zkasm, create-terminate-context.zkasm

**Description:** 

In the zkEVM ROM the MAXMEM register that is used to set the biggest offset of memory used is being set only once to zero - for the first step of the execution trace.
The contracts that will call MLOAD,MSTORE EVM-opcodes will alter the MAXMEM if the memory referenced has higher relative address than the one currently set:


```
pol addrRel = ind*E0 + indRR*RR + offset;

pol maxMemRel = isMem * addrRel;

pol maxMemCalculated = isMaxMem*(addrRel - MAXMEM) + MAXMEM;

MAXMEM' = setMAXMEM * (op0 - maxMemCalculated) + maxMemCalculated;
```
There is a plookup check for the "difference" of the current MAXMEM and the relative address:
```
pol diffMem = isMaxMem* ( (maxMemRel - MAXMEM) -
                  (MAXMEM - maxMemRel) ) +
         (MAXMEM - maxMemRel);
isMaxMem * (1 - isMaxMem) = 0;
...
diffMem in Global.BYTE2;
```
This effectively checks that the difference is not a negative number, as well as that the isMaxMem is correctly set, and also it restrains the the difference to be: |maxMemRel - MAXMEM| < 2^16
On the other hand zkEVM ROM has a limit check for the relative memory offset done in the utils.zkasm:saveMem procedure:
```
$ => B                      :MLOAD(lastMemOffset)
; If the binary has a carry, means the mem expansion is very big. We can jump to oog directly
; offset + length in B
$ => B                      :ADD, JMPC(outOfGas)
; check new memory length is lower than 2**22 - 31 - 1 (max supported memory expansion for %TX_GAS_LIMIT of gas)
%MAX_MEM_EXPANSION_BYTES => A
$                           :LT,JMPC(outOfGas)
```
Although the difference is that the MAX_MEM_EXPANSION_BYTES is equal to 2^22 - 32. As the offset that the ROM effectively uses as the relative address will be the offset/32, this means that the contract can push the memory offset to the maximum of (2^22-32) / 32 = 2^17 - 1.
Since the diffMem should be in BYTE2 range, attacker will need two MLOAD or MSTORE operations to push the MAXMEM to the value bigger than BYTE2 range, e.g. opMSTORE(1000) + opMSTORE(2^16 + 999).

As the MAXMEM is never reset and the diffMem in Global.BYTE2; does not have a selector - for the memory operations with GLOBAL/CTX or stack variables the maxMemRel will be equal to 0 (as the isMem will be 0):
```
pol maxMemRel = isMem * addrRel;
```
This will mean that the diffMem:
```
pol diffMem = isMaxMem* ( (maxMemRel - MAXMEM) -
                      (MAXMEM - maxMemRel) ) +
             (MAXMEM - maxMemRel);
```

Will either be equal to maxMemRel - MAXMEM -- a negative value or MAXMEM - maxMemRel which will be > 2^16 -1, so the consecutive plookup with BYTE2 will not be satisfied.
This gives ability to any illicit actor to send a transaction to the trusted sequencer or force it, and as soon as the batch will be sequenced it will be impossible to prove the next state transition. 

**Remediation:** One of the approaches to remediate the issue will be to change the diffMem plookup with BITS17, or to shrink the MAX_MEM_EXPANSION_BYTES to 2^21-32, so that the biggest value for MAXMEM could be 2^16-1.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Polygonzkevm |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-02-27-PolygonZkEvm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

