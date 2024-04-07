from flask import Flask, request, jsonify, Blueprint
from transformers import AutoProcessor, LlavaForConditionalGeneration
import torch
from PIL import Image
import numpy as np

ocr_api = Blueprint('ocr', __name__)

# model_id = "llava-hf/llava-1.5-7b-hf"

# # Définir un prompt qui guide le modèle pour extraire les informations souhaitées de l'image
# prompt = "USER: <image>\nPlease extract all available information from this French passport, including name, first name, date of birth, passport number, and expiration date.\nASSISTANT:"

# # Charger le modèle et le processeur
# model = LlavaForConditionalGeneration.from_pretrained(
#     model_id, 
#     torch_dtype=torch.float16, 
#     low_cpu_mem_usage=True, 
# ).to("cuda" if torch.cuda.is_available() else "cpu")  # Assurez-vous d'utiliser le GPU si disponible

# processor = AutoProcessor.from_pretrained(model_id)

@ocr_api.route('/ocr_upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['image']
    # if file.filename == '':
    #     return jsonify({'error': 'No selected file'}), 400
    # if file:
    #     # Convertir le fichier en image PIL
    #     raw_image = Image.open(file.stream).convert("RGB")
    #     # Préparer les entrées pour le modèle
    #     inputs = processor(prompt, images=raw_image, return_tensors='pt').to("cuda" if torch.cuda.is_available() else "cpu", torch.float16)
    #     # Générer une sortie à partir du modèle
    #     output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
    #     # Décoder la sortie pour obtenir le texte généré
    #     generated_text = processor.decode(output[0][2:], skip_special_tokens=True)
        
    #     print('Extracted text: ', generated_text)
        
    return jsonify({'message': 'Success', 'extracted_text': file})

