"""H2 PD actuators — standalone example for custom robot extensions.

When you add a new robot to wbc-mjlab, this file is the pattern to copy:

1. Look up per-joint peak torque (URDF ``effort`` limits, vendor MJCF
   ``actuatorfrcrange``, or datasheet).
2. Estimate reflected rotor inertia (``armature``) per motor / gear stage.
3. Derive simulation PD gains from a target natural frequency (here 10 Hz).
4. Group joints that share the same motor into one ``IdealPdActuatorCfg``.
5. Build ``<ROBOT>_ACTION_SCALE`` so policy deltas map to reasonable torques.

H2 numbers below come from:
- Peak torque: Unitree ``unitree_mujoco/unitree_robots/h2/h2_mujoco.xml``
- Armature / motor SKUs: Unitree ``unitree_rl_lab`` actuator tables (N7520,
  N5020, W4010 family — same formulas used across Unitree humanoids)
- Real-robot Kp/Kd (deploy only): ``unitree_sdk2/.../h2_ankle_swing_example.cpp``
  (legs 200/3, waist 300/5) — not used directly in sim.
"""

from __future__ import annotations

import math

from mjlab.actuator.pd_actuator import IdealPdActuatorCfg
from mjlab.entity import EntityArticulationInfoCfg
from mjlab.utils.actuator import reflected_inertia_from_two_stage_planetary

# --- PD gain design (critical damping ratio ζ = 2) --------------------------------

_NATURAL_FREQ_HZ = 10.0
_NATURAL_FREQ = _NATURAL_FREQ_HZ * 2.0 * math.pi  # rad/s
_DAMPING_RATIO = 2.0


def _reflected_armature(rotor_inertias: tuple[float, ...], gears: tuple[float, ...]) -> float:
  """Reflected inertia at the joint (kg·m²) for a multi-stage planetary gearbox."""
  return reflected_inertia_from_two_stage_planetary(rotor_inertias, gears)


def _pd_from_armature(armature: float) -> tuple[float, float]:
  """Return (stiffness, damping) for an ideal PD actuator."""
  stiffness = armature * _NATURAL_FREQ**2
  damping = 2.0 * _DAMPING_RATIO * armature * _NATURAL_FREQ
  return stiffness, damping


def _actuator(
  *,
  target_names_expr: tuple[str, ...],
  effort_limit: float,
  armature: float,
) -> IdealPdActuatorCfg:
  stiffness, damping = _pd_from_armature(armature)
  return IdealPdActuatorCfg(
    target_names_expr=target_names_expr,
    stiffness=stiffness,
    damping=damping,
    effort_limit=effort_limit,
    armature=armature,
  )


# --- Reflected armature per motor SKU (Unitree rl_lab rotor + gear tables) ---------

# N5020-16 (shoulder, elbow, small joints)
_ARMATURE_N5020 = _reflected_armature(
  (0.139e-4, 0.017e-4, 0.169e-4),
  (1, 1 + 46 / 18, 1 + 56 / 16),
)
# N7520-14 (hip yaw, waist yaw)
_ARMATURE_N7520_14 = _reflected_armature(
  (0.489e-4, 0.098e-4, 0.533e-4),
  (1, 4.5, 1 + 48 / 22),
)
# N7520-22 (hip pitch/roll, knee)
_ARMATURE_N7520_22 = _reflected_armature(
  (0.489e-4, 0.109e-4, 0.738e-4),
  (1, 4.5, 5),
)
# W4010-25 (wrist pitch/yaw)
_ARMATURE_W4010 = _reflected_armature((0.068e-4, 0.0, 0.0), (1, 5, 5))
# Two N5020 motors driving one serial joint (ankle pitch, waist roll/pitch)
_ARMATURE_DUAL_N5020 = _ARMATURE_N5020 * 2

# --- Peak |torque| per joint (N·m) from unitree_mujoco h2_mujoco.xml --------------

_TORQUE_LEG = 360.0
_TORQUE_ANKLE_ROLL = 19.0
_TORQUE_ANKLE_PITCH = 66.88
_TORQUE_WAIST_YAW = 120.0
_TORQUE_WAIST_PR = 180.0
_TORQUE_SHOULDER_PITCH = 130.0
_TORQUE_ARM = 60.0
_TORQUE_WRIST = 10.0
_TORQUE_HEAD = 50.0

# --- Actuator groups (one cfg per motor type × joint set) --------------------------

H2_ACTUATOR_HIP_ROLL = _actuator(
  target_names_expr=(".*_hip_roll_joint",),
  effort_limit=_TORQUE_LEG,
  armature=_ARMATURE_N7520_22,
)
H2_ACTUATOR_HIP_PITCH = _actuator(
  target_names_expr=(".*_hip_pitch_joint",),
  effort_limit=_TORQUE_LEG,
  armature=_ARMATURE_N7520_22,
)
H2_ACTUATOR_HIP_YAW = _actuator(
  target_names_expr=(".*_hip_yaw_joint",),
  effort_limit=_TORQUE_LEG,
  armature=_ARMATURE_N7520_14,
)
H2_ACTUATOR_KNEE = _actuator(
  target_names_expr=(".*_knee_joint",),
  effort_limit=_TORQUE_LEG,
  armature=_ARMATURE_N7520_22,
)
H2_ACTUATOR_ANKLE_ROLL = _actuator(
  target_names_expr=(".*_ankle_roll_joint",),
  effort_limit=_TORQUE_ANKLE_ROLL,
  armature=_ARMATURE_N5020,
)
H2_ACTUATOR_ANKLE_PITCH = _actuator(
  target_names_expr=(".*_ankle_pitch_joint",),
  effort_limit=_TORQUE_ANKLE_PITCH,
  armature=_ARMATURE_DUAL_N5020,
)
H2_ACTUATOR_WAIST_YAW = _actuator(
  target_names_expr=("waist_yaw_joint",),
  effort_limit=_TORQUE_WAIST_YAW,
  armature=_ARMATURE_N7520_14,
)
H2_ACTUATOR_WAIST = _actuator(
  target_names_expr=("waist_roll_joint", "waist_pitch_joint"),
  effort_limit=_TORQUE_WAIST_PR,
  armature=_ARMATURE_DUAL_N5020,
)
H2_ACTUATOR_SHOULDER_PITCH = _actuator(
  target_names_expr=(".*_shoulder_pitch_joint",),
  effort_limit=_TORQUE_SHOULDER_PITCH,
  armature=_ARMATURE_N5020,
)
H2_ACTUATOR_ARM = _actuator(
  target_names_expr=(
    ".*_shoulder_roll_joint",
    ".*_shoulder_yaw_joint",
    ".*_elbow_joint",
    ".*_wrist_roll_joint",
  ),
  effort_limit=_TORQUE_ARM,
  armature=_ARMATURE_N5020,
)
H2_ACTUATOR_WRIST = _actuator(
  target_names_expr=(".*_wrist_pitch_joint", ".*_wrist_yaw_joint"),
  effort_limit=_TORQUE_WRIST,
  armature=_ARMATURE_W4010,
)
H2_ACTUATOR_HEAD = _actuator(
  target_names_expr=("head_pitch_joint", "head_yaw_joint"),
  effort_limit=_TORQUE_HEAD,
  armature=_ARMATURE_N5020,
)

H2_ARTICULATION = EntityArticulationInfoCfg(
  actuators=(
    H2_ACTUATOR_HIP_ROLL,
    H2_ACTUATOR_HIP_PITCH,
    H2_ACTUATOR_HIP_YAW,
    H2_ACTUATOR_KNEE,
    H2_ACTUATOR_ANKLE_ROLL,
    H2_ACTUATOR_ANKLE_PITCH,
    H2_ACTUATOR_WAIST_YAW,
    H2_ACTUATOR_WAIST,
    H2_ACTUATOR_SHOULDER_PITCH,
    H2_ACTUATOR_ARM,
    H2_ACTUATOR_WRIST,
    H2_ACTUATOR_HEAD,
  ),
  soft_joint_pos_limit_factor=0.9,
)

# Policy action scale: 0.25 × (effort / stiffness) per joint name regex.
H2_ACTION_SCALE: dict[str, float] = {}
for _cfg in H2_ARTICULATION.actuators:
  for _name in _cfg.target_names_expr:
    H2_ACTION_SCALE[_name] = 0.25 * _cfg.effort_limit / _cfg.stiffness
