import torch
import torch.nn.functional as F

class HighPass:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "blur_radius": ("INT", {
                    "default": 5,
                    "min": 1,
                    "max": 199,
                    "step": 1
                }),
                "sigma": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.1
                }),
                "contrast": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.01,
                    "max": 5.0,
                    "step": 0.01
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "highpass"
    CATEGORY = "pbr"

    def highpass(self, image: torch.Tensor, blur_radius: int, sigma: float, contrast: float):
        if blur_radius == 0:
            return (image,)

        batch_size, height, width, channels = image.shape

        kernel_size = blur_radius * 2 + 1
        # ~ TODO: INVERT GAMMA HERE
        kernel = gaussian_kernel(kernel_size, sigma).repeat(channels, 1, 1).unsqueeze(1)
        image_permuted = image.permute(0, 3, 1, 2) # Torch wants (B, C, H, W) we use (B, H, W, C)
        blurred = F.conv2d(image_permuted, kernel, padding=kernel_size // 2, groups=channels)
        blurred = blurred.permute(0, 2, 3, 1)

        highpass_image = image - blurred

        # Adjust high-pass contrast
        highpass_contrast_adj = torch.tanh(highpass_image * contrast)

        # Normalize the high-pass image
        highpass_normalized = (highpass_contrast_adj - highpass_contrast_adj.min()) / (highpass_contrast_adj.max() - highpass_contrast_adj.min())

        return (highpass_normalized,)

def gaussian_kernel(kernel_size: int, sigma: float):
    x, y = torch.meshgrid(torch.linspace(-1, 1, kernel_size), torch.linspace(-1, 1, kernel_size), indexing="ij")
    d = torch.sqrt(x * x + y * y)
    g = torch.exp(-(d * d) / (2.0 * sigma * sigma))
    return g / g.sum()

NODE_CLASS_MAPPINGS = {
    "HighPass": HighPass,
}
