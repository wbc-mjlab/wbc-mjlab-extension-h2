"""H2 PD actuators (simplified; tune armature/limits from Unitree specs)."""

from __future__ import annotations

import math

from mjlab.actuator.pd_actuator import IdealPdActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg

_NATURAL_FREQ = 10.0 * 2.0 * math.pi
_DAMPING_RATIO = 2.0
_DEFAULT_ARMATURE = 0.01


def _pd_cfg(
  *,
  target_names_expr: tuple[str, ...],
  effort_limit: float,
  armature: float = _DEFAULT_ARMATURE,
) -> IdealPdActuatorCfg:
  stiffness = armature * _NATURAL_FREQ**2
  damping = 2.0 * _DAMPING_RATIO * armature * _NATURAL_FREQ
  return IdealPdActuatorCfg(
    target_names_expr=target_names_expr,
    stiffness=stiffness,
    damping=damping,
    effort_limit=effort_limit,
    armature=armature,
  )


H2_ACTUATOR_LEG = _pd_cfg(
  target_names_expr=(
    ".*_hip_pitch_joint",
    ".*_hip_roll_joint",
    ".*_hip_yaw_joint",
    ".*_knee_joint",
  ),
  effort_limit=360.0,
)
H2_ACTUATOR_ANKLE = _pd_cfg(
  target_names_expr=(".*_ankle_roll_joint", ".*_ankle_pitch_joint"),
  effort_limit=67.0,
)
H2_ACTUATOR_WAIST = _pd_cfg(
  target_names_expr=(
    "waist_yaw_joint",
    "waist_roll_joint",
    "waist_pitch_joint",
  ),
  effort_limit=180.0,
)
H2_ACTUATOR_SHOULDER = _pd_cfg(
  target_names_expr=(
    ".*_shoulder_pitch_joint",
    ".*_shoulder_roll_joint",
    ".*_shoulder_yaw_joint",
  ),
  effort_limit=130.0,
)
H2_ACTUATOR_ARM = _pd_cfg(
  target_names_expr=(
    ".*_elbow_joint",
    ".*_wrist_roll_joint",
  ),
  effort_limit=60.0,
)
H2_ACTUATOR_WRIST = _pd_cfg(
  target_names_expr=(".*_wrist_pitch_joint", ".*_wrist_yaw_joint"),
  effort_limit=10.0,
)
H2_ACTUATOR_HEAD = _pd_cfg(
  target_names_expr=("head_pitch_joint", "head_yaw_joint"),
  effort_limit=50.0,
)

H2_ARTICULATION = EntityArticulationInfoCfg(
  actuators=(
    H2_ACTUATOR_LEG,
    H2_ACTUATOR_ANKLE,
    H2_ACTUATOR_WAIST,
    H2_ACTUATOR_SHOULDER,
    H2_ACTUATOR_ARM,
    H2_ACTUATOR_WRIST,
    H2_ACTUATOR_HEAD,
  ),
  soft_joint_pos_limit_factor=0.9,
)

H2_ACTION_SCALE: dict[str, float] = {}
for _actuator in H2_ARTICULATION.actuators:
  effort = _actuator.effort_limit
  stiffness = _actuator.stiffness
  for name in _actuator.target_names_expr:
    H2_ACTION_SCALE[name] = 0.25 * effort / stiffness
