---
# Core Classification
protocol: BitFluxFi - Stable AMM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 50868
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/coredao/bitfluxfi-stable-amm
source_link: https://www.halborn.com/audits/coredao/bitfluxfi-stable-amm
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
  - Halborn
---

## Vulnerability Title

Non compliance with Curve implementation

### Overview

See description below for full details.

### Original Finding Content

##### Description

### Context

The `stable-amm` is an implementation of Curve's stable swap, and the `Halborn` team verified the proper implementation by inspecting the differences with the `SwapTemplateBase.vy` contract from the [b0bbf77](https://github.com/curvefi/curve-contract/commit/b0bbf77f8f93c9c5f4e415bce9cd71f0cdee960e) commit.

  

Inconsistencies were identified in:

* `calculateTokenAmount` from `SwapUtils.sol`
* `getAdminbalance` from `Swap.sol`
* `stopRampA` from `AmplificationUtils.sol`
* `killMe` feature

  

### Calculate token amount

It was found that the `calculateTokenAmount` of the `SwapUtils.sol` library returns a positive amount when the total supply of the liquidity pool is zero, while the original Curve implementation simply returns a zero amount. The affected function is only for view purposes so it does not affect the pool state, but could cause unplanned behaviour in external contracts.

  

* The `Curve` implementation in `SwapTemplateBase.vy`:

```
def calc_token_amount(_amounts: uint256[N_COINS], _is_deposit: bool) -> uint256:
    """
    @notice Calculate addition or reduction in token supply from a deposit or withdrawal
    @dev This calculation accounts for slippage, but not fees.
         Needed to prevent front-running, not for precise calculations!
    @param _amounts Amount of each coin being deposited
    @param _is_deposit set True for deposits, False for withdrawals
    @return Expected amount of LP tokens received
    """
    amp: uint256 = self._A()
    balances: uint256[N_COINS] = self.balances
    D0: uint256 = self._get_D_mem(balances, amp)
    for i in range(N_COINS):
        if _is_deposit:
            balances[i] += _amounts[i]
        else:
            balances[i] -= _amounts[i]
    D1: uint256 = self._get_D_mem(balances, amp)
    token_amount: uint256 = CurveToken(self.lp_token).totalSupply()
    diff: uint256 = 0
    if _is_deposit:
        diff = D1 - D0
    else:
        diff = D0 - D1
    return diff * token_amount / D0
```

  

* The `Bitflux` implementation in `SwapUtils.sol` the new stable pool invariant `d1` is returned:

```
function calculateTokenAmount(
    Swap storage self,
    uint256[] calldata amounts,
    bool deposit
) external view returns (uint256) {
    uint256 a = _getAPrecise(self);
    uint256[] memory balances = self.balances;
    uint256[] memory multipliers = self.tokenPrecisionMultipliers;

    uint256 d0 = getD(_xp(balances, multipliers), a);
    for (uint256 i = 0; i < balances.length; i++) {
        if (deposit) {
            balances[i] = balances[i].add(amounts[i]);
        } else {
            balances[i] = balances[i].sub(
                amounts[i],
                "Cannot withdraw more than available"
            );
        }
    }
    
    uint256 d1 = getD(_xp(balances, multipliers), a);
    uint256 totalSupply = self.lpToken.totalSupply();

    if (totalSupply == 0) {
        return d1; // first depositor take it all
    }

    if (deposit) {
        return d1.sub(d0).mul(totalSupply).div(d0);
    } else {
        return d0.sub(d1).mul(totalSupply).div(d0);
    }
}
```

  

### Get admin balance

It was found that the `getAdminbalance` from the `Swap.sol` contract was not following the same logic than the admin\_balances counterpart in the Curve implementation.

  

* The `Curve` implementation in `SwapTemplateBase.vy`:

```
def admin_balances(i: uint256) -> uint256:
    return ERC20(self.coins[i]).balanceOf(self) - self.balances[i]
```

  

* The `Bitflux` implementation in `Swap.sol`:

```
function getAdminBalances() external view returns (uint256[] memory adminBalances) {
    uint256 length = swapStorage.pooledTokens.length;
    adminBalances = new uint256[](length);
    for (uint256 i = 0; i < length; i++) {
        adminBalances[i] = swapStorage.getAdminBalance(i);
    }
}
```

  

### Stop ramp A

It was found that the `stopRampA` of the `AmplificationUtils.sol` library included an additional check, in comparison to the original implementation. The `stopRampA` function stops the transition of the amplifier factor of the stable pool, during its transition. That additional check only makes sure that the function cannot be called outside a transition, which has essentially no impact.

  

* The `Curve` implementation in `SwapTemplateBase.vy`:

```
def stop_ramp_A():
    assert msg.sender == self.owner  # dev: only owner

    current_A: uint256 = self._A()
    self.initial_A = current_A
    self.future_A = current_A
    self.initial_A_time = block.timestamp
    self.future_A_time = block.timestamp
    # now (block.timestamp < t1) is always False, so we return saved A

    log StopRampA(current_A, block.timestamp)
```

  

* The `Bitflux` implementation in `AmplificationUtils.sol` (note that the `onlyOwner` modifier is present upstream):

```
function stopRampA(SwapUtils.Swap storage self) external {
    require(self.futureATime > block.timestamp, "Ramp is already stopped");

    uint256 currentA = _getAPrecise(self);
    self.initialA = currentA;
    self.futureA = currentA;
    self.initialATime = block.timestamp;
    self.futureATime = block.timestamp;

    emit StopRampA(currentA, block.timestamp);
}
```

  

### Kill feature

The original Curve contract has a `killMe` feature that allows an owner to shut down a contract, also able to revive it later. It was found that the current implementation does not support this feature. An external contract may assume this feature to be implemented an malfunction as it is not.

  

* The `kill_me` definition in `SwapTemplateBase.vy`:

```
is_killed: bool
kill_deadline: uint256
KILL_DEADLINE_DT: constant(uint256) = 2 * 30 * 86400
```

  

* The `kill_me` toggles in `SwapTemplateBase.vy`:

```
@external
def kill_me():
    assert msg.sender == self.owner  # dev: only owner
    assert self.kill_deadline > block.timestamp  # dev: deadline has passed
    self.is_killed = True


@external
def unkill_me():
    assert msg.sender == self.owner  # dev: only owner
    self.is_killed = False
```

  

* Example usage of the `kill_me` feature in the `add_liquidity` function of `SwapTemplateBase.vy`:

```
@external
@nonreentrant('lock')
def add_liquidity(_amounts: uint256[N_COINS], _min_mint_amount: uint256) -> uint256:
    """
    @notice Deposit coins into the pool
    @param _amounts List of amounts of coins to deposit
    @param _min_mint_amount Minimum amount of LP tokens to mint from the deposit
    @return Amount of LP tokens received by depositing
    """
    assert not self.is_killed  # dev: is killed

    amp: uint256 = self._A()
    old_balances: uint256[N_COINS] = self.balances

```

##### BVSS

[AO:A/AC:L/AX:M/R:N/S:C/C:N/A:N/I:N/D:L/Y:N (2.1)](/bvss?q=AO:A/AC:L/AX:M/R:N/S:C/C:N/A:N/I:N/D:L/Y:N)

##### Recommendation

It is recommended to review the differences between the origin implementation and the current one, and make sure that all deviations are design choices.

##### Remediation

**NOT APPLICABLE:** The **BitFlux team** highlighted that the issue is not applicable and mentioned the following:

*We recognize that our implementation differs from Curve’s original design in certain areas, such as calculateTokenAmount, getAdminBalance, and stopRampA. These differences were intentional design choices made to optimize performance and improve usability for our specific use case. For example, returning a positive amount when the total supply is zero in calculateTokenAmount simplifies initial liquidity provision without affecting pool state or security. Similarly, our additional check in stopRampA ensures that transitions are handled more safely without introducing any negative side effects.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | BitFluxFi - Stable AMM |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/coredao/bitfluxfi-stable-amm
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/coredao/bitfluxfi-stable-amm

### Keywords for Search

`vulnerability`

