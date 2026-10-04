---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53484
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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

[LID-25] Anyone can always transfer 1 wei stETH

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** StETH.sol:getSharesByPooledEth#L311-L315

**Description:**

The functions getSharesByPooledEth and getPooledEthByShares are used to convert from stETH to shares and vice versa. Normally, the pooled ETH amount is greater than the number of shares.

Both functions round down and as a result one would get 0 shares for 1 wei stETH. This leads to some undesired behaviour in the ERC20.transfer functions of stETH.

For example, when calling stETH.transfer(address(1337), 1), the transfer would succeed even though I would not have any stETH balance.

This is due to stETH using shares as underlying balance and the conversion leads to a transfer of 0. However, an event with the stETH amount is still emitted: Transfer(address(this), address(1337), 1). This can potentially cause problems with front-ends or trackers.
```
function getSharesByPooledEth(uint256 _ethAmount) public view returns (uint256) {
    return _ethAmount
        .mul(_getTotalShares())
        .div(_getTotalPooledEther());
}
function _transfer(address _sender, address _recipient, uint256 _amount) internal {
    uint256 _sharesToTransfer = getSharesByPooledEth(_amount);
    _transferShares(_sender, _recipient, _sharesToTransfer);
    _emitTransferEvents(_sender, _recipient, _amount, _sharesToTransfer);
}
function _emitTransferEvents(address _from, address _to, uint _tokenAmount, uint256 _sharesAmount) internal {
    emit Transfer(_from, _to, _tokenAmount);
    emit TransferShares(_from, _to, _sharesAmount);
}
```

**Remediation:**  We would recommend to consider adding an early exit if the shares amount is 0, instead of reverting.

For example:
```
function _transfer(address _sender, address _recipient, uint256 _amount) internal {
    uint256 _sharesToTransfer = getSharesByPooledEth(_amount);
    if (_sharesToTransfer == 0)
        return;
    _transferShares(_sender, _recipient, _sharesToTransfer);
    _emitTransferEvents(_sender, _recipient, _amount, _sharesToTransfer);
}
```

**Status:**  Acknowledged

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

