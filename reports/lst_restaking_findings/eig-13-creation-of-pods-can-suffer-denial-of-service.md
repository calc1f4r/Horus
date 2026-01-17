---
# Core Classification
protocol: Eigenlayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53498
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-16-EigenLayer.md
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
  - Hexens
---

## Vulnerability Title

[EIG-13] Creation of pods can suffer denial of service

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** EigenPodManager.sol:_deployPod#L378-L396

**Description:**  

The function to deploy a pod uses a counter `numPods` to check the total amount of pods against the `maxPods` configuration variable.

An attacker can create as many pods as needed in order to reach `maxPods` and prevent anyone else to create more pods or stake.

`maxPods` can be increased, however, the attacker can always quickly increase `numPods` with the creation of more pods for as long as maxPods low enough. Setting `maxPods` to a very high value would also negate the reason for its existence in such context.

```
    function _deployPod() internal onlyWhenNotPaused(PAUSED_NEW_EIGENPODS) returns (IEigenPod) {
        // check that the limit of EigenPods has not been hit, and increment the EigenPod count
        require(numPods + 1 <= maxPods, "EigenPodManager._deployPod: pod limit reached");
        ++numPods;
        // create the pod
        IEigenPod pod = IEigenPod(
            Create2.deploy( 
                0,
                bytes32(uint256(uint160(msg.sender))),
                // set the beacon address to the eigenPodBeacon and initialize it
                abi.encodePacked(beaconProxyBytecode, abi.encode(eigenPodBeacon, ""))
            )
        );
        pod.initialize(msg.sender);
        // store the pod in the mapping
        ownerToPod[msg.sender] = pod;
        emit PodDeployed(address(pod), msg.sender);
        return pod;
    }
```


**Remediation:**  We recommend to remove the cap on the number of pods as it does not seem to have any actual purpose. 

**Status:**   Acknowledged


- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Eigenlayer |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-10-16-EigenLayer.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

