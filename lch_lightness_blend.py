import torch
import colorspacious

class LCh_Lightness_Blend:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image1": ("IMAGE",),
                "image2": ("IMAGE",),
                "L_component": (["image1", "image2"],),
                "Ch_components": (["image1", "image2"],),
                "image_source": (["image1", "image2"],),
                "blend_factor": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "lch_lightness_blend"
    CATEGORY = "pbr"

    def lch_lightness_blend(self, image1, image2, L_component: str, Ch_components: str, image_source: str, blend_factor: float):
        # Convert RGB to LCh using colorspacious
        lch_image1 = colorspacious.cspace_convert(image1.numpy(), "sRGB1", "JCh")
        lch_image2 = colorspacious.cspace_convert(image2.numpy(), "sRGB1", "JCh")

        # Extract LCh channels
        L1, C1, h1 = lch_image1[..., 0], lch_image1[..., 1], lch_image1[..., 2]
        L2, C2, h2 = lch_image2[..., 0], lch_image2[..., 1], lch_image2[..., 2]

        # Convert L, C and h to PyTorch tensor
        L1 = torch.from_numpy(L1)
        C1 = torch.from_numpy(C1)
        h1 = torch.from_numpy(h1)
        L2 = torch.from_numpy(L2)
        C2 = torch.from_numpy(C2)
        h2 = torch.from_numpy(h2)

        if L_component == "image1":
            L = L1
        elif L_component == "image2":
            L = L2
        else:
            raise ValueError(f"Unsupported arithmetic blend mode: {blend_mode}")

        if Ch_components == "image1":
            C = C1
            h = h1
        elif Ch_components == "image2":
            C = C2
            h = h2
        else:
            raise ValueError(f"Unsupported arithmetic blend mode: {blend_mode}")

        if image_source == "image1":
            image = lch_image1
        elif image_source == "image2":
            image = lch_image2
        else:
            raise ValueError(f"Unsupported arithmetic blend mode: {blend_mode}")

        # Blend LCh lightness with the original image
        L_blend = blend_factor * L + (1 - blend_factor) * image[..., 0]
        # Combine blended L channel with original C and h channels
        blended_image = torch.stack((L_blend, C, h), dim=-1)

        # Convert LCh back to RGB
        rgb_image = colorspacious.cspace_convert(blended_image, "JCh", "sRGB1")

        return (torch.from_numpy(rgb_image),)

NODE_CLASS_MAPPINGS = {
    "LCh_Lightness_Blend": LCh_Lightness_Blend,
}
