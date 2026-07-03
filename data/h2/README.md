# H2 motion data

Place retargeted clips under **`data/h2/<dataset>/`** in this repo (not under wbc-mjlab). Layout matches
[wbc-mjlab `data/README.md`](https://github.com/wbc-mjlab/wbc-mjlab/blob/main/data/README.md):

```
data/h2/<dataset>/
  *.pkl / *.csv      # source clips (version-controlled, or under raw/)
  npz/<clip>.npz     # per-clip FK exports — local only, never committed
  <dataset>.npz      # optional stacked cache (--cache-motion-bundle)
```

Only source clips and READMEs are version-controlled. After clone, run `wbc-mjlab-data-to-npz` before train, play, or vis.

## Bundled samples

[`samples/`](samples/) ships **13 GMR PKL clips** (LAFAN1 + BONES-SEED retargets). See [samples/README.md](samples/README.md) for the clip list and credits.

```bash
# Required once per clone (or after adding new PKL)
uv run wbc-mjlab-data-to-npz --robot h2 --dataset samples

uv run wbc-mjlab-data-vis --robot h2 --dataset samples
uv run wbc-mjlab-train --task Wbc-H2 --dataset samples
uv run wbc-mjlab-play --task Wbc-H2 --dataset samples
```

## DOF layout

The Unitree H2 asset in this repo has **31 actuated joints** (legs, waist, arms, head).
Motion files must match the model `qpos[7:]` joint order from the MJCF.

Use FK conversion against this package's asset:

```bash
uv run wbc-mjlab-data-to-npz --robot h2 --dataset-path ./data/h2/samples
```

Or with a named dataset folder:

```bash
# from wbc-mjlab-extension-h2 repo root — resolves data/h2/samples/ here
uv run wbc-mjlab-data-to-npz --robot h2 --dataset samples
```

For GMR pickle inputs, the converter auto-detects `gmr_pkl` from the `.pkl` extension. Large libraries: add `--batch-size N` for parallel FK on GPU.

## Training

```bash
uv run wbc-mjlab-train --task Wbc-H2 --dataset walk
uv run wbc-mjlab-train --task Wbc-H2 --dataset-path ./data/h2/walk
```

Logs: `logs/rsl_rl/wbc_h2/` (gitignored).

## Retargeting your own clips

Retarget mocap to this MJCF (GMR, custom pipeline, or Unitree tooling), then convert with `wbc-mjlab-data-to-npz`.

Joint/body names must match
[`src/wbc_mjlab_h2/robots/h2/xmls/h2.xml`](../../src/wbc_mjlab_h2/robots/h2/xmls/h2.xml).
