from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# load model once
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def recognize_objects(image_path,query):
    image = Image.open(image_path)

    # these are the labels you're comparing against
    labels = [f"photo of {query}",f"photo of something else "]

    inputs = processor(
        text=labels,
        images=image,
        return_tensors="pt",
        padding=True
    )

    outputs = model(**inputs)
    
    # this gives you a probability score for each label
    probs = outputs.logits_per_image.softmax(dim=1)
    query_score = probs[0][0].item()
    print(f"{image_path} -> {query_score}") 
    # pair each label with its score
    results = dict(zip(labels, probs[0].tolist()))
    return results
