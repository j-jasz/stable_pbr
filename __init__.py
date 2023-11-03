# ~ from .lch import NODE_CLASS_MAPPINGS
# ~ from .lch import NODE_CLASS_MAPPINGS as lch_NODE_CLASS_MAPPINGS
from .lch_convert import NODE_CLASS_MAPPINGS as lch_convert_NODE_CLASS_MAPPINGS
from .lch_lightness_blend import NODE_CLASS_MAPPINGS as lch_lightness_blend_NODE_CLASS_MAPPINGS
from .highpass import NODE_CLASS_MAPPINGS as highpass_NODE_CLASS_MAPPINGS
from .normal import NODE_CLASS_MAPPINGS as normal_NODE_CLASS_MAPPINGS

NODE_CLASS_MAPPINGS = {}
# ~ NODE_CLASS_MAPPINGS.update(lch_NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(lch_convert_NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(lch_lightness_blend_NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(highpass_NODE_CLASS_MAPPINGS)
NODE_CLASS_MAPPINGS.update(normal_NODE_CLASS_MAPPINGS)
__all__ = ["NODE_CLASS_MAPPINGS"]
