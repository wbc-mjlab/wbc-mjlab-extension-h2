"""H2 WBC task builders and task table."""

from __future__ import annotations

from mjlab.envs import ManagerBasedRlEnvCfg

from wbc_mjlab.env.mdp.commands import MotionCommandCfg
from wbc_mjlab.presets.wbc import apply_wbc
from wbc_mjlab.tasks.config import WbcTaskConfig
from wbc_mjlab_h2.robots.h2.base import h2_base_cfg
from wbc_mjlab_h2.robots.h2.constants import (
  H2_EE_TERMINATION_BODY_NAMES,
  H2_MOTION_BODY_NAMES,
)

DEFAULT_H2_TASK_ID = "Wbc-H2"


def h2_wbc_env_cfg() -> ManagerBasedRlEnvCfg:
  cfg = h2_base_cfg()
  apply_wbc(
    cfg,
    motion_body_names=H2_MOTION_BODY_NAMES,
    ee_termination_bodies=H2_EE_TERMINATION_BODY_NAMES,
  )
  return cfg


H2_WBC_TASKS: tuple[WbcTaskConfig, ...] = (
  WbcTaskConfig(
    task_id="Wbc-H2",
    robot_id="h2",
    description="Default WBC tracking + RSI (wbc-mjlab apply_wbc preset).",
    experiment_name="wbc_h2",
    build_env_cfg=h2_wbc_env_cfg,
  ),
)

H2_TASK_BY_ID: dict[str, WbcTaskConfig] = {t.task_id: t for t in H2_WBC_TASKS}


def get_h2_task_config(task_id: str = DEFAULT_H2_TASK_ID) -> WbcTaskConfig:
  try:
    return H2_TASK_BY_ID[task_id]
  except KeyError as exc:
    known = ", ".join(sorted(H2_TASK_BY_ID))
    raise KeyError(f"Unknown H2 task {task_id!r}. Known: {known}") from exc


def make_h2_wbc_env_cfg(
  *,
  play: bool = False,
  task_id: str = DEFAULT_H2_TASK_ID,
  **kwargs,
) -> ManagerBasedRlEnvCfg:
  if kwargs:
    unknown = ", ".join(sorted(kwargs))
    raise TypeError(
      f"Unknown env cfg kwargs for H2: {unknown}. Pass task_id=Wbc-H2."
    )
  cfg = get_h2_task_config(task_id).build_env_cfg()

  if play:
    cfg.episode_length_s = int(1e9)
    cfg.observations["actor"].enable_corruption = False
    cfg.curriculum = {}
    cfg.events.pop("push_robot", None)
    motion_cmd = cfg.commands["motion"]
    assert isinstance(motion_cmd, MotionCommandCfg)
    motion_cmd.pose_range = {}
    motion_cmd.velocity_range = {}
    motion_cmd.assistive_wrench_enabled = False
    if "assistive_wrench" in cfg.events:
      cfg.events["assistive_wrench"].params["enabled"] = False

  return cfg
