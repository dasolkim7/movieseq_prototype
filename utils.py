import os
from openai import OpenAI
from typing import List
import base64

# OpenAI API 키 설정
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def save_uploaded_video(uploaded_file) -> str:
    """업로드된 비디오 파일을 저장하고 경로를 반환"""
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

def get_extracted_images(output_folder: str) -> List[str]:
    """출력 폴더에서 추출된 씬 이미지를 정렬하여 반환"""
    return sorted(
        [os.path.join(output_folder, img) for img in os.listdir(output_folder) if img.endswith(".png")]
    )

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def send_query_to_chatgpt(query: str, images: List[str]) -> str:
    """ChatGPT-4 Vision API에 쿼리를 전달하고 응답을 반환"""
    try:
        messages = [
            {"role": "system", "content": "당신은 유능한 비디오 분석 전문가입니다."},
            {"role": "user", "content": [{"type": "text", "text": query}]}
        ]
        
        for img_path in images:
            base64_image = encode_image(img_path)
            messages[1]["content"].append({
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"}
            })

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error sending query to ChatGPT: {e}")
        return None