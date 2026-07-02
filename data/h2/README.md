# H2 motion data

Place retargeted clips under **`data/h2/<dataset>/`**. Layout matches
[wbc-mjlab `data/README.md`](https://github.com/wbc-mjlab/wbc-mjlab/blob/main/data/README.md):

```
data/h2/<dataset>/
  raw/*.csv          # optional source clips
  npz/<clip>.npz     # per-clip FK exports (training source of truth)
  <dataset>.npz      # optional stacked cache (--cache-motion-bundle)
```

## DOF layout

The Unitree H2 asset in this repo has **31 actuated joints** (legs, waist, arms, head).
Motion files must match the model `qpos[7:]` joint order from the MJCF.

Use FK conversion against this package's asset:

```bash
uv run wbc-mjlab-data-to-npz --robot h2 --dataset-path ./data/h2/my_clips
```

Or with a named dataset folder:

```bash
mkdir -p data/h2/walk/raw
# copy retargeted CSV/PKL into raw/ or the dataset root
uv run wbc-mjlab-data-to-npz --robot h2 --dataset walk
```

## Training

```bash
uv run wbc-mjlab-train --task Wbc-H2 --dataset walk
uv run wbc-mjlab-train --task Wbc-H2 --dataset-path ./data/h2/walk
```

Logs: `logs/rsl_rl/wbc_h2/`.

## Retargeting

There is no bundled H2 clip library yet. Retarget mocap to this MJCF (GMR, custom
pipeline, or Unitree tooling), then convert with `wbc-mjlab-data-to-npz`.

Joint/body names must match
[`src/wbc_mjlab_h2/robots/h2/xmls/h2.xml`](../../src/wbc_mjlab_h2/robots/h2/xmls/h2.xml).
