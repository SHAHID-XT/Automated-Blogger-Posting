from diffusers import DiffusionPipeline
import torch

# Load model (Kaggle GPU works fine)
pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipe = pipe.to("cuda")

prompt = "A person wearing a headset, looking at multiple computer screens displaying code and security alerts, with a concerned but determined expression. The background is a blurred office environment."

# Generate image with 16:9 aspect ratio, e.g. 896x512
image = pipe(prompt, height=512, width=896).images[0]


# Save the generated image to disk
image.save("generated.png")

class AIImageGenerator:

    def generate_image(self,prompt,save_path="image.png"):
        
        pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
        pipe = pipe.to("cuda")

        # Generate image with 16:9 aspect ratio, e.g. 896x512
        image = pipe(prompt, height=512, width=896).images[0]

        # Save the generated image to disk
        image.save(save_path)
