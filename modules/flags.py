from enum import IntEnum, Enum

disabled = 'Disabled'
enabled = 'Enabled'
subtle_variation = 'Vary (Subtle)'
strong_variation = 'Vary (Strong)'
upscale_15 = 'Upscale (1.5x)'
upscale_2 = 'Upscale (2x)'
upscale_fast = 'Upscale (Fast 2x)'

uov_list = [disabled, subtle_variation, strong_variation, upscale_15, upscale_2, upscale_fast]

enhancement_uov_before = "Before First Enhancement"
enhancement_uov_after = "After Last Enhancement"
enhancement_uov_processing_order = [enhancement_uov_before, enhancement_uov_after]

enhancement_uov_prompt_type_original = 'Original Prompts'
enhancement_uov_prompt_type_last_filled = 'Last Filled Enhancement Prompts'
enhancement_uov_prompt_types = [enhancement_uov_prompt_type_original, enhancement_uov_prompt_type_last_filled]

CIVITAI_NO_KARRAS = ["euler", "euler_ancestral", "heun", "dpm_fast", "dpm_adaptive", "ddim", "uni_pc"]

# fooocus: a1111 (Civitai)
KSAMPLER = {
    "euler": "Euler",
    "euler_ancestral": "Euler a",
    "heun": "Heun",
    "heunpp2": "",
    "dpm_2": "DPM2",
    "dpm_2_ancestral": "DPM2 a",
    "lms": "LMS",
    "dpm_fast": "DPM fast",
    "dpm_adaptive": "DPM adaptive",
    "dpmpp_2s_ancestral": "DPM++ 2S a",
    "dpmpp_sde": "DPM++ SDE",
    "dpmpp_sde_gpu": "DPM++ SDE",
    "dpmpp_2m": "DPM++ 2M",
    "dpmpp_2m_sde": "DPM++ 2M SDE",
    "dpmpp_2m_sde_gpu": "DPM++ 2M SDE",
    "dpmpp_3m_sde": "",
    "dpmpp_3m_sde_gpu": "",
    "ddpm": "",
    "lcm": "LCM",
    "tcd": "TCD",
    "restart": "Restart"
}

SAMPLER_EXTRA = {
    "ddim": "DDIM",
    "uni_pc": "UniPC",
    "uni_pc_bh2": ""
}

SAMPLERS = KSAMPLER | SAMPLER_EXTRA

KSAMPLER_NAMES = list(KSAMPLER.keys())

SCHEDULER_NAMES = ["normal", "karras", "exponential", "sgm_uniform", "simple", "ddim_uniform", "lcm", "turbo", "align_your_steps", "tcd", "edm_playground_v2.5"]
SAMPLER_NAMES = KSAMPLER_NAMES + list(SAMPLER_EXTRA.keys())

sampler_list = SAMPLER_NAMES
scheduler_list = SCHEDULER_NAMES

clip_skip_max = 12

default_vae = 'Default (model)'

refiner_swap_method = 'joint'

default_input_image_tab = 'uov_tab'
input_image_tab_ids = ['uov_tab', 'ip_tab', 'inpaint_tab', 'describe_tab', 'enhance_tab', 'metadata_tab']

cn_ip = "ImagePrompt"
cn_ip_face = "FaceSwap"
cn_canny = "PyraCanny"
cn_cpds = "CPDS"

ip_list = [cn_ip, cn_canny, cn_cpds, cn_ip_face]
default_ip = cn_ip

default_parameters = {
    cn_ip: (0.5, 0.6), cn_ip_face: (0.9, 0.75), cn_canny: (0.5, 1.0), cn_cpds: (0.5, 1.0)
}  # stop, weight

output_formats = ['png', 'jpeg', 'webp']

inpaint_mask_models = ['u2net', 'u2netp', 'u2net_human_seg', 'u2net_cloth_seg', 'silueta', 'isnet-general-use', 'isnet-anime', 'sam']
inpaint_mask_cloth_category = ['full', 'upper', 'lower']
inpaint_mask_sam_model = ['vit_b', 'vit_l', 'vit_h']

inpaint_engine_versions = ['None', 'v1', 'v2.5', 'v2.6']
inpaint_option_default = 'Inpaint or Outpaint (default)'
inpaint_option_detail = 'Improve Detail (face, hand, eyes, etc.)'
inpaint_option_modify = 'Modify Content (add objects, change background, etc.)'
inpaint_options = [inpaint_option_default, inpaint_option_detail, inpaint_option_modify]

describe_type_photo = 'Photograph'
describe_type_anime = 'Art/Anime'
describe_types = [describe_type_photo, describe_type_anime]

sdxl_aspect_ratios = [
    '704*1408', '704*1344', '768*1344', '768*1280', '832*1216', '832*1152',
    '896*1152', '896*1088', '960*1088', '960*1024', '1024*1024', '1024*960',
    '1088*960', '1088*896', '1152*896', '1152*832', '1216*832', '1280*768',
    '1344*768', '1344*704', '1408*704', '1472*704', '1536*640', '1600*640',
    '1664*576', '1728*576'
]


class MetadataScheme(Enum):
    FOOOCUS = 'fooocus'
    A1111 = 'a1111'


metadata_scheme = [
    (f'{MetadataScheme.FOOOCUS.value} (json)', MetadataScheme.FOOOCUS.value),
    (f'{MetadataScheme.A1111.value} (plain text)', MetadataScheme.A1111.value),
]


class OutputFormat(Enum):
    PNG = 'png'
    JPEG = 'jpeg'
    WEBP = 'webp'

    @classmethod
    def list(cls) -> list:
        return list(map(lambda c: c.value, cls))


class PerformanceLoRA(Enum):
    QUALITY = None
    SPEED = None
    EXTREME_SPEED = 'sdxl_lcm_lora.safetensors'
    LIGHTNING = 'sdxl_lightning_4step_lora.safetensors'
    HYPER_SD = 'sdxl_hyper_sd_4step_lora.safetensors'


class Steps(IntEnum):
    QUALITY = 60
    SPEED = 30
    EXTREME_SPEED = 8
    LIGHTNING = 4
    HYPER_SD = 4

    @classmethod
    def keys(cls) -> list:
        return list(map(lambda c: c, Steps.__members__))


class StepsUOV(IntEnum):
    QUALITY = 36
    SPEED = 18
    EXTREME_SPEED = 8
    LIGHTNING = 4
    HYPER_SD = 4


class Performance(Enum):
    QUALITY = 'Quality'
    SPEED = 'Speed'
    EXTREME_SPEED = 'Extreme Speed'
    LIGHTNING = 'Lightning'
    HYPER_SD = 'Hyper-SD'

    @classmethod
    def list(cls) -> list:
        return list(map(lambda c: (c.name, c.value), cls))

    @classmethod
    def values(cls) -> list:
        return list(map(lambda c: c.value, cls))

    @classmethod
    def by_steps(cls, steps: int | str):
        return cls[Steps(int(steps)).name]

    @classmethod
    def has_restricted_features(cls, x) -> bool:
        if isinstance(x, Performance):
            x = x.value
        return x in [cls.EXTREME_SPEED.value, cls.LIGHTNING.value, cls.HYPER_SD.value]

    def steps(self) -> int | None:
        return Steps[self.name].value if self.name in Steps.__members__ else None

    def steps_uov(self) -> int | None:
        return StepsUOV[self.name].value if self.name in StepsUOV.__members__ else None

    def lora_filename(self) -> str | None:
        return PerformanceLoRA[self.name].value if self.name in PerformanceLoRA.__members__ else None

    def get_preset_config(self) -> dict:
        """Returns dictionary of all settings for this performance preset"""
        is_fast_mode = self.has_restricted_features(self)

        config = {
            'steps': self.steps(),
            'uov_steps': self.steps_uov(),
            'performance_lora_enabled': self.lora_filename() is not None,
            'performance_lora_type': 'None',
            'performance_lora_weight': 1.0,
            'sampler_name': 'dpmpp_2m_sde_gpu',
            'scheduler_name': 'karras',
            'cfg_scale': 7.0,
            'sharpness': 2.0,
            'adaptive_cfg': 7.0,
            'refiner_switch': 0.8,
            'adm_scaler_positive': 1.5,
            'adm_scaler_negative': 0.8,
            'adm_scaler_end': 0.3,
            'refiner_swap_method': 'joint',
            'disable_intermediate_results': is_fast_mode
        }

        # Set performance LoRA type and weight
        if self == Performance.EXTREME_SPEED:
            config['performance_lora_type'] = 'LCM'
            config['performance_lora_weight'] = 1.0
        elif self == Performance.LIGHTNING:
            config['performance_lora_type'] = 'Lightning'
            config['performance_lora_weight'] = 1.0
        elif self == Performance.HYPER_SD:
            config['performance_lora_type'] = 'Hyper-SD'
            config['performance_lora_weight'] = 0.8

        # Override settings for fast modes
        if is_fast_mode:
            config['cfg_scale'] = 1.0
            config['sharpness'] = 0.0
            config['adaptive_cfg'] = 1.0
            config['refiner_switch'] = 1.0
            config['adm_scaler_positive'] = 1.0
            config['adm_scaler_negative'] = 1.0
            config['adm_scaler_end'] = 0.0

            # Set specific sampler/scheduler for each fast mode
            if self == Performance.EXTREME_SPEED:
                config['sampler_name'] = 'lcm'
                config['scheduler_name'] = 'lcm'
            elif self == Performance.LIGHTNING:
                config['sampler_name'] = 'euler'
                config['scheduler_name'] = 'sgm_uniform'
            elif self == Performance.HYPER_SD:
                config['sampler_name'] = 'dpmpp_sde_gpu'
                config['scheduler_name'] = 'karras'

        return config
