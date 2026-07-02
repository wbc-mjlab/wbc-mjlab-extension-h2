"""Unitree H2 MJCF, scene entity, and motion metadata."""

from __future__ import annotations

from pathlib import Path

import mujoco

from mjlab.entity import EntityCfg
from mjlab.utils.spec_config import CollisionCfg

_HERE = Path(__file__).parent
H2_XML: Path = _HERE / "xmls" / "h2.xml"
assert H2_XML.exists()


def get_spec() -> mujoco.MjSpec:
  return mujoco.MjSpec.from_file(str(H2_XML))


HOME_KEYFRAME = EntityCfg.InitialStateCfg(
  pos=(0, 0, 1.2),
  joint_pos={
    ".*_hip_pitch_joint": -0.1,
    ".*_knee_joint": 0.3,
    ".*_ankle_pitch_joint": -0.2,
    ".*_shoulder_pitch_joint": 0.35,
    ".*_elbow_joint": 0.87,
    "left_shoulder_roll_joint": 0.18,
    "right_shoulder_roll_joint": -0.18,
  },
  joint_vel={".*": 0.0},
)

# Collision geoms: non-visual meshes on the asset (visual geoms use contype=0).
FULL_COLLISION = CollisionCfg(
  geom_names_expr=(".*",),
  condim={r".*ankle_pitch.*": 3, ".*": 1},
  priority={r".*ankle_pitch.*": 1},
  friction={r".*ankle_pitch.*": (0.6,)},
)


def get_h2_robot_cfg() -> EntityCfg:
  from wbc_mjlab_h2.robots.h2.actuators import H2_ARTICULATION

  return EntityCfg(
    init_state=HOME_KEYFRAME,
    collisions=(FULL_COLLISION,),
    spec_fn=get_spec,
    articulation=H2_ARTICULATION,
  )


MOTION_Z_DEBIAS_FOOT_BODY_NAMES: tuple[str, ...] = (
  "left_ankle_roll_link",
  "right_ankle_roll_link",
)
MOTION_Z_DEBIAS_FOOT_SOLE_Z: float = 0.04

H2_ANCHOR_BODY_NAME = "torso_link"

H2_MOTION_BODY_NAMES: tuple[str, ...] = (
  "pelvis",
  "left_hip_roll_link",
  "left_knee_link",
  "left_ankle_roll_link",
  "right_hip_roll_link",
  "right_knee_link",
  "right_ankle_roll_link",
  "torso_link",
  "left_shoulder_roll_link",
  "left_elbow_link",
  "left_wrist_yaw_link",
  "right_shoulder_roll_link",
  "right_elbow_link",
  "right_wrist_yaw_link",
)

H2_EE_TERMINATION_BODY_NAMES: tuple[str, ...] = (
  "left_ankle_roll_link",
  "right_ankle_roll_link",
  "left_wrist_yaw_link",
  "right_wrist_yaw_link",
)

H2_ENDEFFECTOR_BODY_NAMES: tuple[str, ...] = H2_EE_TERMINATION_BODY_NAMES

H2_FOOT_SITE_NAMES: tuple[str, ...] = ("left_foot", "right_foot")

H2_IMU_ANG_VEL_SENSOR = "robot/imu_ang_vel"
H2_IMU_LIN_VEL_SENSOR = "robot/imu_lin_vel"
