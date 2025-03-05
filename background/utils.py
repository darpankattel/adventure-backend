from diffusers import StableDiffusionPipeline
import torch

pipeline = StableDiffusionPipeline.from_pretrained(
    "./models/background_model", torch_dtype=torch.float16,  use_safetensors=True, requires_safety_checker=False, safety_checker=None)
# .to("cuda")


def intitate_generation(serializer_data):
    prompt = serializer_data["prompt"]
    image = pipeline(prompt=prompt).images[0]
    image_path = f"{serializer_data['id']}_{serializer_data['campaign']}.jpg"
    image.save(image_path)

    return image_path
