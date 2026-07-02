.PHONY: sync sync-cpu smoke test lint

sync:
	uv sync --extra cu128 --group dev

sync-cpu:
	uv sync --extra cpu --group dev

smoke:
	MUJOCO_GL=disable uv run wbc-mjlab-list-envs | grep Wbc-H2

test:
	MUJOCO_GL=disable uv run pytest tests/

lint:
	uv run ruff check src tests
