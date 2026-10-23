# L-008 — A proxy measurement is indistinguishable from a device measurement

**Gap.** The bench labels its measurements `measured: false` (proxy). `admit-record.v0` has no field for that label, so a frozen record can carry a proxy number as if it were performance — the exact thing rule 4 ("numbers keep their denominators") forbids.

**Carrier.** A bench admit record with `measure: {measured: false, proxy: labelled, F: null}` and one with `measured: true, device: …, denominator: tokens/s`.

**Change.** `admit-record.v1`: `measure` object with `measured` (bool), `device` or `proxy`, and `denominator`. A `land` with `measured: false` is schema-valid only when `decision: freeze` is absent (proxy walks may `reject`/`revert`, never freeze).

**Falsifier.** A freeze that is legal on a proxy, or a measured record that cannot name its denominator. Survey item: P9, survey §4.3.

**Loop.** application

**Depends on.** none

**Status.** open
