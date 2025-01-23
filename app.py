import os
import random
import streamlit as st
from dotenv import load_dotenv
from utils import save_uploaded_video, get_extracted_images, send_query_to_chatgpt
from scene_extractor import split_video_to_one_image_per_scene

# .env 파일에서 환경 변수 로드
load_dotenv()

st.title("MovieSeq - Video Scene Analyzer")

# 동영상 업로드 및 쿼리 입력
uploaded_video = st.file_uploader("동영상을 업로드하세요", type=["mp4", "mov", "avi", "mkv", "webm"])
query = st.text_area("ChatGPT에 전달할 질문을 입력하세요 (예: 이 씬은 어떤 느낌인가요?)")
output_folder = "output_scenes"

# 텍스트 파일 로드
def load_texts(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    else:
        return []

texts = load_texts("texts.txt")  # Load the texts from texts.txt


if uploaded_video is not None:
    # 동영상 미리보기
    st.video(uploaded_video)

    if st.button("씬 추출 및 분석"):
        if not query.strip():
            st.warning("쿼리를 입력하세요.")
        else:
            # 진행 상태 표시를 위한 progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # 1단계: 동영상 저장
            status_text.text("1단계: 동영상을 저장 중입니다...")
            video_path = save_uploaded_video(uploaded_video)
            progress_bar.progress(20)

            # 2단계: 씬 추출
            status_text.text("2단계: 씬을 추출 중입니다...")
            split_video_to_one_image_per_scene(video_path, output_folder, threshold=27.0)
            progress_bar.progress(50)

            # 3단계: 추출된 이미지 가져오기
            status_text.text("3단계: 추출된 이미지를 가져오는 중입니다...")
            image_files = get_extracted_images(output_folder)
            progress_bar.progress(70)

            if len(image_files) > 0:
                # 여기에 검색된 유사한 이미지를 출력하시면 됩니다~!
                status_text.text("4단계: 검색된 이미지를 보여줍니다...")
                selected_images = random.sample(image_files, min(5, len(image_files)))
                st.write("추출된 장면 중 쿼리와 가장 유사한 2개의 이미지를 보여줍니다:")

                for img_path in selected_images:
                    st.image(img_path, caption=os.path.basename(img_path), use_container_width=True)
                
                #여기에 검색된 유사한 synopsis를 출력하시면 됩니다!
                if texts:
                    random_text = random.choice(texts).strip()
                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #ddd; 
                            border-radius: 10px; 
                            padding: 10px; 
                            margin: 10px 0; 
                            background-color: #f9f9f9; 
                            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);">
                            <p style="font-size: 16px; font-weight: bold; color: #333; text-align: center;">
                            {random_text}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                progress_bar.progress(85)

                # 5단계: ChatGPT로 쿼리 전달
                status_text.text("5단계: ChatGPT로 쿼리를 전달하고 있습니다...")
                with st.spinner("ChatGPT가 응답을 생성 중입니다..."):
                    response = send_query_to_chatgpt(query, selected_images)
                
                if response:
                    st.write("ChatGPT의 답변:")
                    st.success(response)
                else:
                    st.error("ChatGPT 요청 중 오류가 발생했습니다.")

                progress_bar.progress(100)
                status_text.text("작업 완료!")
            else:
                st.warning("장면이 감지되지 않았습니다.")
                progress_bar.progress(100)
                status_text.text("작업 실패!")