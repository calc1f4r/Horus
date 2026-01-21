---
# Core Classification
protocol: Aligned Layer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38369
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2024/08/aligned-layer/
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
finders_count: 2
finders:
  - Martin Ortner
  -  George Kobakhidze
                        
---

## Vulnerability Title

BatcherPaymentService - Non-Atomic Contract Deployment and Initialization Forge Script Can Be Front Run ✓ Fixed

### Overview


The BatcherPaymentService deployment script using Forge has a vulnerability that could allow a malicious actor to front-run the deployment and take control of the newly deployed contract. This could result in the deployer having to redeploy the contracts. To fix this, the recommendation is to include initialization calldata when deploying the ERC1967Proxy to ensure that the contract is initialized in the same transaction as its deployment and prevent potential attacks. This issue has been resolved with a fix that can be found in the yetanotherco/aligned_layer#828 pull request.

### Original Finding Content

#### Resolution



 Fixed with [yetanotherco/aligned\_layer\#828](https://github.com/yetanotherco/aligned_layer/pull/828) by initializing the Proxy directly with the internal `upgradeToAndCall` during deployment.
 

#### Description


The `BatcherPaymentService` deployment script using Forge performs a two\-step deployment and initialization process. Between the `startBroadcast` and `stopBroadcast` directives, the script executes three transactions:


1. Deploys a new `BatcherService` contract.
2. Deploys a new `ERC1967Proxy` without initialization calldata.
3. Initializes the `BatcherPaymentService` contract through the proxy.


**contracts/script/deploy/BatcherPaymentServiceDeployer.s.sol:L31\-L44**



```
vm.startBroadcast();

BatcherPaymentService batcherPaymentService = new BatcherPaymentService();
ERC1967Proxy proxy = new ERC1967Proxy(
    address(batcherPaymentService),
    ""
);
BatcherPaymentService(payable(address(proxy))).initialize(
    alignedLayerServiceManager,
    batcherPaymentServiceOwner,
    batcherWallet
);

vm.stopBroadcast();

```
Since these transactions are broadcast individually, there is a risk that a malicious actor could front\-run the third transaction to claim control of the newly deployed contract. This issue could force the deployer to re\-deploy the contracts.


For further details, refer to the [Forge script documentation](https://book.getfoundry.sh/tutorials/best-practices?highlight=VulnerableScript#scripts).


#### Recommendation


To mitigate this risk, include the initialization calldata when deploying the `ERC1967Proxy`. This approach ensures that the contract is initialized in the same transaction as its deployment, preventing potential front\-running attacks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Aligned Layer |
| Report Date | N/A |
| Finders | Martin Ortner,  George Kobakhidze
                         |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2024/08/aligned-layer/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

