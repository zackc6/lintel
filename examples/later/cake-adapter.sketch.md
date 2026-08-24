# Later: `@cake.v0` as a plugin (not the SKU)

**Do not staff this until** the Triton typed-schedule PoC has a partner canary **and** either a public Cake compiler exists or a customer pays for the wrap.

```
adapter_id: cake.v0
schedule:   <Cake's published agent-facing types, mapped 1:1>
gates:      Cake {where} bands, passed through to Lintel adapter_gate
lowers:     *their* compiler, not ours
%k:         hash(..., adapter_id=cake.v0, ...)   # new keys, no shared cache with Triton
```

If this wrap becomes the only demo (“we compiled Cake”), we have failed [C4](../../docs/RISKS.md) and the [data-plane buy test](../../docs/DATA_PLANE.md).
