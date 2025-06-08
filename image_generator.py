from diffusers import DiffusionPipeline
import torch

class AIImageGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32

        # Load the pipeline once during initialization
        self.pipe = DiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=self.dtype
        )
        self.pipe = self.pipe.to(self.device)

    def generate_image(self, prompt, save_path="image.png"):
        # Generate image with 16:9 aspect ratio
        image = self.pipe(prompt, height=512, width=896).images[0]
        image.save(save_path)
if __name__ == "__main__":
    gen = AIImageGenerator()
    gen.generate_image(
        prompt="Cybersecurity expert monitoring multiple threat dashboards in a dark room.",
        save_path="test.png"
    )
    print("✅ Image generated!")