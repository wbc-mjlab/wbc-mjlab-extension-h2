# wbc-mjlab-h2

Minimal standalone example: register **Unitree H2** with [wbc-mjlab](https://github.com/wbc-mjlab/wbc-mjlab) via the public extension API (`register_wbc_extension`).

## Quick start

```bash
make sync          # or make sync-cpu
make smoke         # Wbc-H2 appears in wbc-mjlab-list-envs
```

Add retargeted motion under `data/h2/<dataset>/`, then:

```bash
uv run wbc-mjlab-data-to-npz --robot h2 --dataset my_clips
uv run wbc-mjlab-train --task Wbc-H2 --dataset my_clips
uv run wbc-mjlab-play --task Wbc-H2 --dataset-path ./data/h2/my_clips --viewer viser
```

See [data/h2/README.md](data/h2/README.md) for motion layout.

## What this repo contains

| File | Role |
|------|------|
| [`mjlab_entry.py`](src/wbc_mjlab_h2/mjlab_entry.py) | `register_wbc_extension(...)` — entire registration |
| `robots/h2/` | MJCF + meshes, `base.py`, `actuators.py`, `tasks.py`, `rl_cfg.py` |
| `data/h2/` | Motion clips for `--robot h2` |

The only registered task is **`Wbc-H2`** (`wbc_mjlab.presets.wbc.apply_wbc`).

## Registration (full example)

```python
from wbc_mjlab.extension import WbcRobotSpec, register_wbc_extension
from wbc_mjlab.motion.robot_assets import RobotMotionSpec

register_wbc_extension(
  WbcRobotSpec(
    robot_id="h2",
    aliases=("unitree_h2",),
    make_env_cfg=make_h2_wbc_env_cfg,
    make_rl_cfg=h2_wbc_rl_cfg,
    motion_spec=RobotMotionSpec(
      scene_cfg_fn=lambda: make_h2_wbc_env_cfg().scene,
      foot_body_names=MOTION_Z_DEBIAS_FOOT_BODY_NAMES,
      foot_sole_z=MOTION_Z_DEBIAS_FOOT_SOLE_Z,
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
