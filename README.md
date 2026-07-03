# WBC-MJLab extension — Unitree H2

Reference [wbc-mjlab](https://github.com/wbc-mjlab/wbc-mjlab) **robot extension** for Unitree H2: a separate repo that registers H2 via `register_wbc_extension` (not built into wbc-mjlab core).

**Plug-and-play WBC.** This extension does **not** add new presets, reward retuning, or paper-specific task variants. Training uses the same shared WBC stack as G1 — `wbc_mjlab.presets.wbc.apply_wbc` — with only robot-specific wiring (MJCF, actuators, tracking bodies, sensors, data paths). Register your robot, convert motion, run `wbc-mjlab-train --task Wbc-<Robot>`: the MDP, RSI, rewards, and CLIs are unchanged.

**This is not production-ready.** The H2 asset, actuators, and training setup are a **reference layout** for adding *your* robot in a **separate repo** — without forking wbc-mjlab. Several details still need validation against hardware and vendor data, including:

- **Motor armature and PD gains** — reflected inertias are inferred from public Unitree motor tables, not H2-specific datasheets
- **MJCF fidelity** — collision primitives, link inertias, and foot geometry are approximate
- **Sim-to-real** — no deploy pipeline or tuned policies are bundled here
- **Motion retargeting** — bundled PKL clips are early H2 retargets; artifacts remain (e.g. standing on toes, foot slip, imperfect contacts). Cleaner references would likely improve tracking policy quality; the samples here are for **illustrating the extension workflow**, not as a tuned motion library

Use this repo as a **guideline**: copy the structure (`mjlab_entry.py`, `robots/<id>/`, `data/<id>/`), swap in your MJCF and actuator tables, point `apply_wbc` at your body names, and register via `register_wbc_extension`. Expect to iterate on model accuracy as you compare sim against your platform.

## Quick start

```bash
make sync          # or make sync-cpu
make smoke         # Wbc-H2 appears in wbc-mjlab-list-envs
```

This repo ships **13 sample mocap clips** as GMR PKL under `data/h2/samples/`. They are **smoke-test references**, not production retargets — preview with `wbc-mjlab-data-vis` before training. **NPZ is not bundled** — run FK conversion once after clone:

```bash
# 1. Required: PKL → NPZ (creates data/h2/samples/npz/*.npz locally)
uv run wbc-mjlab-data-to-npz --robot h2 --dataset samples --batch-size 6

# 2. Preview / train / play (need NPZ from step 1)
uv run wbc-mjlab-data-vis --robot h2 --dataset samples
uv run wbc-mjlab-train --task Wbc-H2 --dataset samples
uv run wbc-mjlab-play --task Wbc-H2 --dataset samples --viewer viser
```

Run from this repo root so `data/h2/<dataset>/` resolves here (via `project_root` on `WbcRobotSpec`).

Training logs go to `logs/rsl_rl/wbc_h2/` (gitignored). See [data/h2/README.md](data/h2/README.md) and [data/h2/samples/README.md](data/h2/samples/README.md) for motion layout and clip credits.

## What this repo contains

| Path | Role |
|------|------|
| [`mjlab_entry.py`](src/wbc_mjlab_h2/mjlab_entry.py) | `register_wbc_extension(...)` — entire registration |
| `robots/h2/` | MJCF + meshes, `base.py`, `actuators.py`, `tasks.py`, `rl_cfg.py` |
| `data/h2/samples/` | Bundled GMR PKL source clips (`*.npz` generated locally, not committed) |

The only registered task is **`Wbc-H2`**, built with the stock **`apply_wbc`** preset from wbc-mjlab (same MDP as `Wbc-G1` — no custom preset fork).

What you provide per robot vs what stays shared:

| You add (extension repo) | Unchanged (wbc-mjlab core) |
|--------------------------|----------------------------|
| MJCF + meshes | `apply_wbc` preset (rewards, RSI, terminations) |
| Actuator / collision config | Train / play / data CLIs |
| `base.py` body names, IMU, contacts | Motion command + multi-clip training |
| `data/<robot>/` motion clips | RL hyperparams via `rl_cfg` defaults |

The H2 MJCF follows wbc-mjlab conventions (visual/collision geom split, named foot collisions, no actuators or sim timestep in XML — those come from the env and `EntityCfg`).

## Registration (full example)

One entry point registers the robot and a single `Wbc-H2` task — no new preset module required:

```python
from wbc_mjlab.extension import WbcRobotSpec, register_wbc_extension
from wbc_mjlab.motion.robot_assets import RobotMotionSpec

register_wbc_extension(
  WbcRobotSpec(
    robot_id="h2",
    aliases=("unitree_h2",),
    project_root=Path(__file__).resolve().parents[2],  # this repo's data/h2/
    make_env_cfg=make_h2_wbc_env_cfg,
    make_rl_cfg=h2_wbc_rl_cfg,
    motion_spec=RobotMotionSpec(
      scene_cfg_fn=lambda: make_h2_wbc_env_cfg().scene,
      foot_body_names=MOTION_Z_DEBIAS_FOOT_BODY_NAMES,
      foot_sole_z=MOTION_Z_DEBIAS_FOOT_SOLE_Z,
      mjcf_path=H2_XML,
    ),
  ),
  H2_WBC_TASKS,
)
```

`pyproject.toml` exposes this via `[project.entry-points."mjlab.tasks"]` so the stock `wbc-mjlab-*` CLIs work.

## Development

```bash
make test    # registration smoke tests (no NPZ required)
make lint
```

## License

Apache-2.0
