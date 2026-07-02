"""Registration smoke tests for the H2 extension."""

from __future__ import annotations


def test_h2_task_registered() -> None:
  import mjlab  # noqa: F401
  import wbc_mjlab_h2.mjlab_entry  # noqa: F401
  from wbc_mjlab.tasks import get_task_config, list_wbc_task_ids, register_all_wbc_tasks

  register_all_wbc_tasks()

  assert "Wbc-H2" in list_wbc_task_ids()
  task = get_task_config("Wbc-H2")
  assert task.robot_id == "h2"


def test_h2_env_cfg_builds() -> None:
  from wbc_mjlab_h2.robots.h2.tasks import make_h2_wbc_env_cfg

  cfg = make_h2_wbc_env_cfg()
  assert cfg.scene.entities["robot"] is not None
  assert cfg.commands["motion"].anchor_body_name == "torso_link"
