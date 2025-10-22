# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Fooocus is an offline, open-source image generation application built on Stable Diffusion XL (SDXL) and Gradio. It emphasizes simplicity and quality, requiring minimal user tweaking while producing high-quality results. The project is in Limited Long-Term Support (LTS) mode with bug fixes only—no migration to newer architectures like Flux is planned.

## Common Commands

### Running the Application

**Standard installation (Linux/Mac with venv):**
```bash
# First time setup
python3 -m venv fooocus_env
source fooocus_env/bin/activate
pip install -r requirements_versions.txt

# Run application
source fooocus_env/bin/activate
python entry_with_update.py

# Run with remote access
python entry_with_update.py --listen

# Run with different presets
python entry_with_update.py --preset anime
python entry_with_update.py --preset realistic
```

**Anaconda:**
```bash
# First time setup
conda env create -f environment.yaml
conda activate fooocus
pip install -r requirements_versions.txt

# Run application
conda activate fooocus
python entry_with_update.py
```

**Windows (from zip download):**
```bash
# Run default
run.bat

# Run anime preset
run_anime.bat

# Run realistic preset
run_realistic.bat
```

### Testing

```bash
# Run all unit tests
python -m unittest tests/

# Windows embedded python
..\python_embeded\python.exe -m unittest
```

### Key Launch Arguments

- `--listen`: Open UI to network (default: localhost only)
- `--port PORT`: Specify port (default varies)
- `--share`: Create public Gradio link
- `--preset PRESET`: Load preset (default, anime, realistic, lightning, lcm, etc.)
- `--always-high-vram`: Force high VRAM mode (recommended for Colab)
- `--disable-offload-from-vram`: Keep models in VRAM (faster on high-end GPUs)
- `--debug-mode`: Enable debug logging
- `--disable-preset-selection`: Disable preset switching in UI

## Supported Model Architectures

Fooocus now supports multiple Stable Diffusion architectures with automatic detection:

### Supported Architectures
- **SD 1.5**: Original Stable Diffusion (768px base resolution, 4-channel latent)
- **SD 2.0/2.1**: Improved Stable Diffusion (768px base resolution, OpenCLIP text encoder)
- **SDXL**: Stable Diffusion XL (1024px base resolution, dual text encoders, ADM guidance)
- **SDXL Refiner**: Specialized refiner model for SDXL

### Architecture Detection
The model architecture is automatically detected when loading a checkpoint via `get_model_architecture()` in `modules/default_pipeline.py`. Detection uses:
1. Model class type (SD15, SD20, SDXL, SDXLRefiner)
2. Latent format (SD15 vs SDXL)
3. Context dimension (768 for SD1.5, 1024 for SD2.0)

### Feature Availability by Architecture

| Feature | SD 1.5 | SD 2.0 | SDXL | Notes |
|---------|--------|--------|------|-------|
| Basic Generation | ✅ | ✅ | ✅ | All architectures supported |
| Prompt Expansion | ✅ | ✅ | ✅ | GPT-2 based, universal |
| Sharpness | ✅ | ✅ | ✅ | Sampling-level feature |
| CFG Scale | ✅ | ✅ | ✅ | Universal |
| ADM Guidance | ❌ | ❌ | ✅ | SDXL-only (automatic) |
| Refiner | ❌ | ❌ | ✅ | SDXL-only (automatic) |
| LoRA | ✅ | ✅ | ✅ | Architecture-matched |
| ControlNet | ✅ | ✅ | ✅ | Architecture-matched |
| Inpaint | ✅ | ✅ | ✅ | Custom algorithm |
| Upscale | ✅ | ✅ | ✅ | Universal |

Architecture-specific features are automatically enabled/disabled based on the loaded model.

## Architecture Overview

### High-Level Structure

Fooocus follows a layered architecture:

```
Web UI (webui.py - Gradio)
    ↓
Async Task Manager (async_worker.py)
    ↓
Generation Pipeline (default_pipeline.py, core.py)
    ↓
Patched Diffusion Engine (ldm_patched/)
```

### Entry Points & Flow

1. **entry_with_update.py** → Auto-update wrapper via git
2. **launch.py** → Environment initialization, model downloads, launches UI
3. **webui.py** → Gradio interface definition (~1100 lines)

The application starts a worker thread that continuously processes an async task queue, yielding preview updates back to the UI.

### Core Modules (`/modules/`)

- **async_worker.py** (79KB): Task queue orchestration, all generation workflows (txt2img, img2img, inpaint, upscale, enhance)
- **config.py** (36KB): Configuration loading, defaults, path management, preset system
- **default_pipeline.py** (17KB): Pipeline state, model management (base/refiner), CLIP encoding, VAE operations
- **core.py** (13KB): Model loading, LoRA application, VAE encoding/decoding, ControlNet
- **patch.py** (22KB): Fooocus-specific model patches (ADM guidance, sharpness, SAG, etc.)
- **meta_parser.py** (26KB): Metadata parsing/serialization for generated images
- **flags.py** (5.8KB): Enums and constants (performance levels, samplers, aspect ratios)
- **util.py** (18KB): Image utilities, LoRA extraction, wildcard handling

### Advanced Features (`/extras/`)

- **ip_adapter.py**: Image Prompt (IP-Adapter) integration
- **preprocessors.py**: ControlNet preprocessors (Canny, CPDS)
- **interrogate.py**: Image description via BLIP
- **wd14tagger.py**: Anime tagging
- **inpaint_mask.py**: Advanced mask generation (U2Net, SAM, cloth segmentation)
- **expansion.py**: GPT-2 based prompt expansion (Fooocus's "magic")
- **face_crop.py**: Face detection for face swap

### Key Directories

- `/modules/`: Core application logic
- `/extras/`: Optional/advanced features
- `/ldm_patched/`: Patched Stable Diffusion XL library
- `/presets/`: Configuration presets (JSON files)
- `/sdxl_styles/`: SDXL style definitions
- `/wildcards/`: Prompt randomization templates
- `/models/`: Local model cache (auto-downloaded)
- `/outputs/`: Generated images

## Architecture Deep Dive

### Async Task Pattern

Tasks are encapsulated in `AsyncTask` objects (async_worker.py) containing all generation parameters (~160 attributes). Tasks are queued in `async_tasks` list and processed by a worker thread that yields results back via the `yields` list for streaming previews.

### Model Management

- Two global model instances: `model_base` and `model_refiner` (default_pipeline.py)
- Models loaded on-demand and cached
- LoRA application happens per-task without reloading base models
- StableDiffusionModel wrapper holds unet, vae, clip, clip_vision

### Configuration System

Layered configuration priority:
1. `presets/default.json` - Base defaults
2. `config.txt` - User overrides (auto-generated after first run)
3. Command-line arguments - CLI overrides

Presets are JSON files in `/presets/` that can override defaults, specify models, and configure generation parameters.

### Generation Pipeline Flow

```
User Input → Task Creation → Prompt Processing (expansion, styles)
→ Model Loading (base/refiner/LoRAs) → CLIP Encoding
→ Image Input Processing (vary/upscale/inpaint) → ControlNet/IP-Adapter Setup
→ Diffusion Sampling → VAE Decoding → Post-processing → Save
```

**Key Pipeline Steps (default_pipeline.py::process_diffusion):**
1. Model selection (base vs refiner based on denoise strength)
2. Latent initialization (empty or from image)
3. Sigma calculation (noise schedule)
4. Sampling (joint/separate/VAE modes)
5. VAE decoding
6. Post-processing (NSFW check, enhancement)

### Fooocus-Specific Innovations

These are implemented in `patch.py` and represent Fooocus's quality advantages:

1. **GPT-2 Prompt Expansion**: Offline prompt enhancement (extras/expansion.py)
2. **Native Refiner Swap**: Seamless base→refiner transition in single k-sampler
3. **Negative ADM Guidance**: Compensates for lack of cross-attention in XL's highest resolution
4. **Self-Attention Guidance (SAG)**: Prevents overly smooth/plastic results
5. **Custom Inpaint Algorithm**: Superior to standard SDXL inpaint
6. **Custom Image Prompt**: Better than standard IP-Adapters

## Development Guidelines

### Making Changes

- **UI modifications**: Edit `webui.py` (Gradio components)
- **Generation logic**: Modify `async_worker.py` or `default_pipeline.py`
- **Model loading**: Modify `core.py` or `default_pipeline.py`
- **New features**: Create functions following AsyncTask pattern, integrate into worker
- **Model patches**: Add to `patch.py` following PatchSettings pattern
- **Configuration**: Use `modules/config.py` and preset JSON files

### Global State

Be aware of these global instances:
- `shared.gradio_root`: Gradio app instance
- `pipeline.model_base/model_refiner`: Loaded model instances
- `patch_settings`: Per-process patch configuration
- `async_tasks`: Task queue

### Code Organization

- UI layer isolated in `webui.py`
- Task processing in `async_worker.py`
- Model operations in `default_pipeline.py` and `core.py`
- Custom modifications in `patch.py`
- Configuration centralized in `modules/config.py`

### Important Notes

- Fooocus uses **Python 3.10** specifically
- Built on **PyTorch** with custom patches to diffusion models
- Models auto-download on first use (can be 5-10GB+)
- Minimal requirement: 4GB VRAM + 8GB RAM (requires swap)
- The codebase uses direct PyTorch/Diffusers with minimal abstractions
- Custom Gradio hijack in `modules/gradio_hijack.py` for enhanced components

## Model System

### Default Models by Preset

- **Default**: juggernautXL_v8Rundiffusion
- **Realistic**: realisticStockPhoto_v20
- **Anime**: animaPencilXL_v500

Models are automatically downloaded to `models/checkpoints/` on first launch.

### LoRA System

- LoRAs stored in `models/loras/`
- Applied dynamically without reloading base model
- Supports inline LoRA syntax in prompts: `<lora:filename:weight>`
- Performance LoRAs (LCM, Lightning, Hyper-SD) reduce required steps

### VAE Handling

- Default: Use VAE from checkpoint
- Custom: Load separate VAE file from `models/vae/`
- VAE approximation: Fast preview during generation

## Configuration Files

After first launch, these files are created:

- `config.txt`: Main configuration (editable JSON)
- `config_modification_tutorial.txt`: Documentation for config options
- `user_path_config.txt`: **Deprecated** (removed)

## Prompt Features

- **Wildcards**: `__color__ flower` → Random selection from `wildcards/color.txt`
- **Array Processing**: `[[red, green, blue]] flower` → 3 separate images
- **Inline LoRAs**: `flower <lora:sunflowers:1.2>` → Apply LoRA
- **Prompt Weighting**: `I am (happy:1.5)` → A1111-style emphasis
- **Embeddings**: `(embedding:filename:1.1)`
- **Multi-line Prompts**: Each line treated as separate prompt component

## Advanced Features

- **Image Prompt**: Alternative to standard IP-Adapters with better quality
- **Inpaint/Outpaint**: Custom algorithm superior to SDXL standard
- **Face Swap**: InsightFace integration
- **Describe**: BLIP-based image captioning
- **Enhance**: Multi-tab enhancement with mask generation
- **Upscale**: Multiple upscale models supported
- **ControlNet**: User-friendly integration (Canny, depth, etc.)

## Project Status

Fooocus is in **Limited Long-Term Support (LTS)** mode:
- Bug fixes only
- No migration to newer architectures (Flux, etc.)
- Built entirely on Stable Diffusion XL
- For newer models, consider WebUI Forge, ComfyUI, or Fooocus forks
