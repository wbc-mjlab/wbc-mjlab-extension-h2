"""Mjlab entry point: register Unitree H2 with wbc-mjlab."""

from __future__ import annotations

from wbc_mjlab.extension import WbcRobotSpec, register_wbc_extension
from wbc_mjlab.motion.robot_assets import RobotMotionSpec

from wbc_mjlab_h2.robots.h2.constants import (
  MOTION_Z_DEBIAS_FOOT_BODY_NAMES,
  MOTION_Z_DEBIAS_FOOT_SOLE_Z,
)
from wbc_mjlab_h2.robots.h2.rl_cfg import h2_wbc_rl_cfg
from wbc_mjlab_h2.robots.h2.tasks import H2_WBC_TASKS, make_h2_wbc_env_cfg

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
