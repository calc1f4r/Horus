---
# Core Classification
protocol: Ethereum Foundation
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19369
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/ethereum-foundation/ef-kzg/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/ethereum-foundation/ef-kzg/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Inconsistent Handling of Zero X-Coordinate and Point at Infinity

### Overview

See description below for full details.

### Original Finding Content

## KZG-10: Active Contributor State Does Not Update on Error

## Asset
`kzg-ceremony-sequencer/src/api/v1/contribute.rs`

## Status
Resolved: See Resolution

## Rating
Informational

## Description
During processing a user’s contribution, if an error occurs in the `signer receipt.sign()` on line [88], it triggers an immediate return without modifying the contributor state. The result is that the `active_contributor` state would be stuck in `Contributing` until the `expire_current_contributor()` thread is triggered. This unnecessarily consumes the sequencer’s contributing time as `lobby/try_contribute` will not promote any other users to the `active_contributor`.

Furthermore, the transcript state is updated before `receipt.sign()` and the storage state is updated after. Therefore, the storage state and transcript state will no longer be synchronized. This issue is raised as informational as it should not occur in production. For `receipt.sign()` to error, an external signer must be used, which is a signer where the private key is not handled directly by the `kzg-ceremony-sequence` program.

## Recommendations
Move `receipt.sign()` after `lobby_state.clear_current_contributor()`, `storage.finish_contribution()`, and `num_contributions.fetch_add()`, so an error will not impact the transcript, lobby, or storage state.

## Resolution
PR #150 resolves this issue by applying the recommendation. The transcript, lobby, and storage states will now remain synchronized.

---

## KZG-11: Potential Panics if `bytes_to_hex()` is Called With Disproportionate Sizes

## Asset
`crypto/src/hex_format.rs`

## Status
Resolved: See Resolution

## Rating
Informational

## Description
The function `bytes_to_hex()` can panic if the input arguments `N` or `M` are of disproportionate size.

```rust
pub fn bytes_to_hex<S: Serializer, const N: usize, const M: usize>(
    serializer: S,
    bytes: [u8; N],
) -> Result<S::Ok, S::Error> {
    assert_eq!(2 + 2 * N, M);
    if serializer.is_human_readable() {
        let mut hex = [0_u8; M];
        hex[0] = b'0';
        hex[1] = b'x';
        hex::encode_to_slice(bytes, &mut hex[2..])
            .expect("BUG: output buffer is of the correct size");
        let str = std::str::from_utf8(&hex).expect("BUG: hex is valid UTF-8");
        serializer.serialize_str(str)
    } else {
        serializer.serialize_bytes(&bytes)
    }
}
```

The first panic will occur on line [16] if the `assert_eq!()` macro fails. A second index out of bounds panic will occur if `N = 0` and `M = 2`, when `hex[2..]` is indexed on line [21]. These values are type-level arguments that are supplied at compile time. All occurrences in the `kzg-ceremony-sequencer` repository have been checked against the panic conditions, thus the issue is raised as informational.

## Recommendations
Consider returning an error for both potential panics. That is, if `N == 0 || 2 + 2 * N != M`.

## Resolution
The code has been updated so that it will not panic in the case of malformed arguments. Two separate pull requests have been made to resolve this issue, PR #161 and PR #150.

---

## KZG-12: Inefficient Conversion of `Uint8Array` to String

## Asset
`trusted-setup-frontend/src/pages/entropyInput.tsx`

## Status
Resolved: See Resolution

## Rating
Informational

## Description
There is an inefficient conversion of `Uint8Array` to string and then back to `Uint8Array`. The following code snippet is from the function `processGeneratedEntropy()`.

```javascript
const entropy = mouseEntropy + keyEntropy + randomBytes(32);
const entropyAsArray = Uint8Array.from(
    entropy.split('').map((x) => x.charCodeAt(0))
);
```

`randomBytes(32)` is of type `Uint8Array`, and `mouseEntropy` and `keyEntropy` are of type string. Therefore, `entropy` is of type string. `randomBytes(32)` is cast to a string object using the default format `1,2,3,4,5,6,...,32`. `entropyAsArray` reads each character in the string as an ASCII value. The values of `randomBytes(32)` will be 44 (",") or 48-57 ("0"-"9"). It is inefficient to cast the values of a `Uint8Array` to string and then back to `Uint8Array`. The issue is raised as informational as there is no loss in cryptographic entropy used in HKDF.

## Recommendations
Consider having `entropy` only include `mouseEntropy` and `keyEntropy`, convert this to a `Uint8Array`, then append `randomBytes(32)`.

## Resolution
The issue is mitigated by first converting entropy input from the mouse and keyboard to a `Uint8Array`, then appending `randomBytes()`. Commit `46f5532` contains the updated functionality.

---

## KZG-13: Error Handling in Lobby Will Continue to Loop

## Asset
`trusted-setup-frontend/src/pages/lobby.tsx`

## Status
Resolved: See Resolution

## Rating
Informational

## Description
The function `poll()` will intermittently call the API `/lobby/try_contribute`. Certain errors are non-recoverable, such as `TryContributeError::RateLimited`, which removes the user when they are rate limited, and `TryContributeError::UnknownSessionId`, which implies the user does not have a valid bearer token. These errors will continue the recursion, although they cannot recover.

```javascript
async function poll(): Promise<void> {
    // periodically post /slot/join
    const res = await tryContribute.mutateAsync();
    if (isSuccessRes(res) && res.hasOwnProperty('contributions')) {
        updateContribution(JSON.stringify(res));
        navigate(ROUTES.CONTRIBUTING);
    } else {
        const resError = res as ErrorRes;
        switch (resError.code) {
            case 'TryContributeError::RateLimited':
                setError(resError.error);
                break;
            case 'TryContributeError::UnknownSessionId':
                setError(
                    resError.error +
                    '. You might have taken more time to get into the lobby. Please reload and sign in again'
                );
                break;
            case 'TryContributeError::AnotherContributionInProgress':
                setError(resError.error);
                break;
            default:
                setError('Unknown error code: ' + resError.code);
                break;
        }
        // try again after LOBBY_CHECKIN_FREQUENCY
        await sleep(LOBBY_CHECKIN_FREQUENCY);
        return await poll();
    }
}
poll();
```

The code block above shows how `TryContributeError::UnknownSessionId` and `TryContributeError::RateLimited` will break the switch statement and then recursively call `poll()`. Each recursion iteration will repeat these errors, except `TryContributeError::RateLimited` removes the session; hence, the next error will be `TryContributeError::UnknownSessionId`. The issue is considered informational as it does not pose a security risk. The client will continue the recursion, causing the `/lobby/try_contribute` API to be called every `LOBBY_CHECKIN_FREQUENCY`, which is a minor drain on resources for both the client and server.

## Recommendations
Consider handling the non-recoverable errors by displaying the error message and either redirecting to the sign-in page or stopping the recursion.

## Resolution
Commit `bdff216` adds a case to handle the `LobbyIsFull` error.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Ethereum Foundation |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/ethereum-foundation/ef-kzg/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/ethereum-foundation/ef-kzg/review.pdf

### Keywords for Search

`vulnerability`

