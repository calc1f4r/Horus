---
# Core Classification
protocol: Starbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43952
audit_firm: ConsenSys
contest_link: none
source_link: https://diligence.consensys.io/audits/2024/08/starbase/
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
finders_count: 2
finders:
  - Sergii Kravchenko
  -  Vladislav Yaroshuk
                        
---

## Vulnerability Title

Missing Validations in constructor, initializer and Setter Functions ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



In the `2b508ff772206751317e8b0c6f5f70d4987a2b5e` commit provided for the fix review, the finding has been partially fixed using the provided recommendation.


**Update (commit hash `be86d6b0940556113cf04f0298c868502a58926a`):** More checks are added.




#### Description


In the code repository, there is a lack of validation for input variables in `constructor` and `initializer` functions, as well as in various setter functions. Specifically, there is no validation to ensure that the provided addresses implement the correct interface using `ERC165Checker`. Additionally, there is no validation to ensure that the input variable is not a zero address. Without these validations, there is a risk that incorrect or incompatible contracts could be assigned to these variables, potentially leading to unexpected behavior or contract failures.


#### Examples


**starbase\_swap/contracts/AggregatedSwapRouter.sol:L14\-L17**



```
constructor(address CallSwapTool_, address IWETH_) {
    _CallSwapTool = CallSwapTool_;
    _IWETH = IWETH_;
}

```
**starbase\-limitorder/src/StarBaseApprove.sol:L49\-L56**



```
constructor(address permit2){
    PERMIT2 = IAllowanceTransfer(permit2);
}

function init(address owner, address initProxyAddress) external {
    initOwner(owner);
    _StarBase_PROXY_ = initProxyAddress;
}

```
**starbase\-limitorder/src/StarBaseApprove.sol:L58\-L64**



```
function unlockSetProxy(address newStarBaseProxy) public onlyOwner {
    if(_StarBase_PROXY_ == address(0))
        _TIMELOCK_ = block.timestamp + _TIMELOCK_EMERGENCY_DURATION_;
    else
        _TIMELOCK_ = block.timestamp + _TIMELOCK_DURATION_;
    _PENDING_StarBase_PROXY_ = newStarBaseProxy;
}

```
**starbase\-limitorder/src/StarBaseApproveProxy.sol:L38\-L51**



```
constructor(address StarBaseApporve) {
    _StarBase_APPROVE_ = StarBaseApporve;
}

function init(address owner, address[] memory proxies) external {
    initOwner(owner);
    for(uint i = 0; i < proxies.length; i++)
        _IS_ALLOWED_PROXY_[proxies[i]] = true;
}

function unlockAddProxy(address newStarBaseProxy) public onlyOwner {
    _TIMELOCK_ = block.timestamp + _TIMELOCK_DURATION_;
    _PENDING_ADD_StarBase_PROXY_ = newStarBaseProxy;
}

```
**starbase\-limitorder/src/StarBaseDCA.sol:L69\-L74**



```
function init(address owner, address StarBaseApproveProxy, address feeReciver, uint160 feeRate) external {
    initOwner(owner);
    _StarBase_APPROVE_PROXY_ = StarBaseApproveProxy;
    _FEE_RECEIVER_ = feeReciver;
    _FEE_RATE_ = feeRate;
}

```
**starbase\-limitorder/src/StarBaseDCA.sol:L176\-L179**



```
function addWhiteList(address contractAddr) public onlyOwner {
    isWhiteListed[contractAddr] = true;
    emit AddWhiteList(contractAddr);
}

```
**starbase\-limitorder/src/StarBaseDCA.sol:L186\-L188**



```
function changeFeeReceiver(address newFeeReceiver) public onlyOwner {
    _FEE_RECEIVER_ = newFeeReceiver;
    emit ChangeFeeReceiver(newFeeReceiver);

```
**starbase\-limitorder/src/StarBaseDCABot.sol:L33\-L43**



```
function init(
    address owner,
    address StarBaseDCA,
    address tokenReceiver,
    address StarBaseApprove
) external {
    initOwner(owner);
    _StarBase_DCA_ = StarBaseDCA;
    _TOKEN_RECEIVER_ = tokenReceiver;
    _StarBase_APPROVE_ = StarBaseApprove;
}

```
**starbase\-limitorder/src/StarBaseDCABot.sol:L106\-L109**



```
function addAdminList (address userAddr) external onlyOwner {
    isAdminListed[userAddr] = true;
    emit addAdmin(userAddr);
}

```
**starbase\-limitorder/src/StarBaseDCABot.sol:L116\-L119**



```
function changeTokenReceiver(address newTokenReceiver) external onlyOwner {
    _TOKEN_RECEIVER_ = newTokenReceiver;
    emit changeReceiver(newTokenReceiver);
}

```
**starbase\-limitorder/src/StarBaseLimitOrder.sol:L56\-L61**



```
function init(address owner, address StarBaseApproveProxy, address feeReciver,uint160 feeRate) external {
    initOwner(owner);
    _StarBase_APPROVE_PROXY_ = StarBaseApproveProxy;
    _FEE_RECEIVER_ = feeReciver;
    _FEE_RATE_ = feeRate;
}

```
**starbase\-limitorder/src/StarBaseLimitOrder.sol:L168\-L171**



```
function addWhiteList (address contractAddr) public onlyOwner {
    isWhiteListed[contractAddr] = true;
    emit AddWhiteList(contractAddr);
}

```
**starbase\-limitorder/src/StarBaseLimitOrder.sol:L178\-L181**



```
function changeFeeReceiver (address newFeeReceiver) public onlyOwner {
    _FEE_RECEIVER_ = newFeeReceiver;
    emit ChangeFeeReceiver(newFeeReceiver);
}

```
**starbase\-limitorder/src/StarBaseLimitOrderBot.sol:L35\-L45**



```
function init(
    address owner,
    address StarBaseLimitOrder,
    address tokenReceiver,
    address StarBaseApprove
) external {
    initOwner(owner);
    _StarBase_LIMIT_ORDER_ = StarBaseLimitOrder;
    _TOKEN_RECEIVER_ = tokenReceiver;
    _StarBase_APPROVE_ = StarBaseApprove;
}

```
**starbase\-limitorder/src/StarBaseLimitOrderBot.sol:L104\-L107**



```
function addAdminList (address userAddr) external onlyOwner {
    isAdminListed[userAddr] = true;
    emit addAdmin(userAddr);
}

```
**starbase\-limitorder/src/StarBaseLimitOrderBot.sol:L114\-L117**



```
function changeTokenReceiver(address newTokenReceiver) external onlyOwner {
    _TOKEN_RECEIVER_ = newTokenReceiver;
    emit changeReceiver(newTokenReceiver);
}

```
#### Recommendation


We recommend adding `ERC165Checker` interface validation in the constructor and initializer functions to ensure that the provided addresses implement the required interfaces and are valid. Additionally, ensure that input variables are not zero addresses. This will help ensure that only compatible contracts are used, reducing the risk of errors or unexpected behavior.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Starbase |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  Vladislav Yaroshuk
                         |

### Source Links

- **Source**: https://diligence.consensys.io/audits/2024/08/starbase/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

