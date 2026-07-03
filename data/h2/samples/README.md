# H2 sample motions

A small, **version-controlled** subset of retargeted H2 clips for smoke-testing
convert, train, play, and `wbc-mjlab-data-vis` without downloading full datasets.

**Retargeting quality.** These clips are early H2 retargets from LAFAN1 / BONES-SEED source mocap. Known artifacts include standing on toes, foot slip, and other contact quirks visible in `wbc-mjlab-data-vis`. Better retargeting and foot placement would likely improve trained policies; for now the dataset exists to **demonstrate plugging an external robot into wbc-mjlab**, not as a curated motion library.

**13 clips** ship as GMR PKL in this folder (8 from LAFAN1 retargeting, 5 from
BONES-SEED). **NPZ is not committed** — run conversion once after clone to populate
`npz/`, then train or visualize:

```bash
uv run wbc-mjlab-data-to-npz --robot h2 --dataset samples
uv run wbc-mjlab-data-to-npz --robot h2 --dataset samples --batch-size 6   # parallel FK workers
uv run wbc-mjlab-data-vis --robot h2 --dataset samples
uv run wbc-mjlab-train --task Wbc-H2 --dataset samples
uv run wbc-mjlab-play --task Wbc-H2 --dataset samples
```

## Layout

```
data/h2/samples/
  README.md
  *.pkl              # source clips (bundled, GMR format)
  npz/               # placeholder dir only in git — run data-to-npz locally
  npz/<clip>.npz     # never committed (*.npz is gitignored)
```

## Bundled clips

### LAFAN1 retarget (8 clips)

From [lvhaidong/LAFAN1_Retargeting_Dataset](https://huggingface.co/datasets/lvhaidong/LAFAN1_Retargeting_Dataset)
— LAFAN1 mocap retargeted to Unitree H2, GMR PKL.

| File | Motion |
|------|--------|
| `walk1_subject1.pkl` | Walking |
| `run1_subject2.pkl` | Running |
| `sprint1_subject2.pkl` | Sprinting |
| `dance1_subject1.pkl` | Dance |
| `fallAndGetUp1_subject1.pkl` | Fall and get up |
| `fight1_subject2.pkl` | Fight / kick |
| `fightAndSports1_subject1.pkl` | Fight and sports combo |

### BONES-SEED (5 clips)

From [bones-studio/seed](https://huggingface.co/datasets/bones-studio/seed) — acrobatic
flips retargeted to H2, GMR PKL.

| File | Motion |
|------|--------|
| `flip_090_001__A304.pkl` | 90° flip |
| `flip_090_002__A304_M.pkl` | 90° flip (mirrored) |
| `flip_090_003__A304.pkl` | 90° flip (variant) |
| `flip_360_009__A416.pkl` | 360° flip |
| `flip_360_011__A416_M.pkl` | 360° flip (mirrored) |

## Credits and licenses

### LAFAN1 retargeting (8 clips)

| | |
|---|---|
| **Mocap** | [Ubisoft LAFAN1](https://github.com/ubisoft/ubisoft-laforge-animation-dataset) (CC BY-NC-ND 4.0) |
| **H2 retarget** | GMR / custom retarget to this repo's H2 MJCF |
| **Format** | GMR PKL (`fps`, `root_pos`, `root_rot`, `dof_pos`) |

LAFAN1 motion content is licensed under
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) (non-commercial,
no derivatives). The bundled clips are **unmodified subsets** for tutorial and
reproducibility; for the full set or commercial use, download from Hugging Face and
follow the dataset card.

### BONES-SEED (5 clips)

| | |
|---|---|
| **Dataset** | [bones-studio/seed](https://huggingface.co/datasets/bones-studio/seed) on Hugging Face |
| **Publisher** | [Bones Studio](https://bones.studio/datasets/seed) |
| **Format** | GMR PKL retargeted to H2 |

BONES-SEED requires accepting the
[dataset license](https://huggingface.co/datasets/bones-studio/seed) on Hugging Face
before download. The samples here are a small excerpt; see `LICENSE.md` in the full
dataset for terms.

### This repository

Sample motion **files** remain under their respective dataset licenses above.
The `wbc-mjlab-extension-h2` **code** is Apache-2.0 (see repo root `LICENSE`).

When you publish results trained on these clips, cite the original datasets in addition to
`wbc-mjlab`, [wbc-mjlab-extension-h2](https://github.com/wbc-mjlab/wbc-mjlab-extension-h2), and
[mjlab](https://github.com/mujocolab/mjlab).
