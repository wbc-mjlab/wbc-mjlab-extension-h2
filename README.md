# Whole-body control for Unitree H2 (standalone wbc-mjlab example) 

Minimal standalone example: register **Unitree H2** with [wbc-mjlab](https://github.com/wbc-mjlab/wbc-mjlab) via the public extension API (`register_wbc_extension`).

**This is not a production-ready.** The H2 asset, actuators, and training setup are a **reference layout** for building whole-body control on your own robot in a **separate repo** — without forking wbc-mjlab. Several details still need validation against hardware and vendor data, including:

- **Motor armature and PD gains** — reflected inertias are inferred from public Unitree motor tables, not H2-specific datasheets
- **MJCF fidelity** — collision primitives, link inertias, and foot geometry are approximate
- **Sim-to-real** — no deploy pipeline or tuned policies are bundled here

Use this repo as a **guideline**: copy the structure (`mjlab_entry.py`, `robots/<id>/`, `data/<id>/`), swap in your MJCF and actuator tables, and register via `register_wbc_extension`. Expect to iterate on model accuracy as you compare sim against your platform.

## Quick start

```bash
make sync          # or make sync-cpu
 uv run wbc-mjlab-list-envs # Wbc-H2 should appears in wbc-mjlab-list-envs
```

This repo ships **13 sample mocap clips** under `data/h2/samples/` (GMR PKL, retargeted to H2). From the repo root:

```bash
# FK export → data/h2/samples/npz/ (gitignored; regenerate after pull)
uv run wbc-mjlab-data-to-npz --robot h2 --dataset samples --batch-size 6

# Preview clips in the browser
uv run wbc-mjlab-data-vis --robot h2 --dataset samples

# Train and play
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
| `data/h2/samples/` | Bundled GMR PKL clips + generated `npz/` for smoke tests |

The only registered task is **`Wbc-H2`** (`wbc_mjlab.presets.wbc.apply_wbc`).

The H2 MJCF follows wbc-mjlab conventions (visual/collision geom split, named foot collisions, no actuators or sim timestep in XML — those come from the env and `EntityCfg`).

## Registration (full example)

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
make test
make lint
```

## License

Apache-2.0
