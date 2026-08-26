# Later: `@tilelang.ascend` as a sink (not the SKU)

**Do not staff this until** one NVIDIA cubin has landed through `@choreo.v0` (schedule **consumed**, not `print_triton` comments) **and** a partner already serves on Ascend.

```
adapter_id: tilelang.ascend
face:       same Choreo Kernel AST (propose payload)
hw_id:      e.g. huawei.ascend-a2   # admission; not Kernel.target in %k
spaces:     valid-for-this-hw_id (GM / L1 / UB / L0A / L0B / L0C / …)
            not gmem/smem/tmem renamed
lowers:     TileLang-Ascend / Ascend C — *their* compiler
            Copy/Mma/Barrier/Pipeline.depth → MTE / Cube / Vector overlap
gates:      same Finding bands W|L|S|V|{compile_ok} → adapter_gate
%k:         hash(..., hw_id, adapter_id=tilelang.ascend, compiler_ver=choreoir;tilelang-ascend, ...)
```

Two sinks under one Lintel control plane. Do not average NVIDIA `tmem` and Ascend `L0C` into one `onchip` cell. Do not dual-live with the GPU sink before the first NVIDIA canary.

Ascend bar is TileLang-Ascend / Ascend C (~0.95–1.0× FA vs handwritten AscendC), **not** Cake. If the demo is “we compiled Choreo for NPU” without serving \(F\), we failed [C4](../../docs/RISKS.md) and the [data-plane buy test](../../docs/DATA_PLANE.md).
