import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector
from PIL import Image

def split_video_to_one_image_per_scene(video_path, output_folder, threshold=30.0):
    """
    PySceneDetect를 이용하여 콘텐츠 기반으로 씬 전환을 감지한 뒤,
    각 씬에서 대표 이미지를 하나만 추출하여 저장합니다.
    """
    os.makedirs(output_folder, exist_ok=True)

    # 비디오 불러오기 (PySceneDetect)
    video = open_video(video_path)

    # SceneManager 생성 및 ContentDetector 추가
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))

    # 장면(씬) 감지
    scene_manager.detect_scenes(video=video)
    scene_list = scene_manager.get_scene_list()

    print(f"감지된 씬 개수: {len(scene_list)}")

    # 각 씬 구간별로 대표 이미지 저장
    for i, (start_time, end_time) in enumerate(scene_list):
        # MoviePy VideoFileClip으로 서브클립 생성
        clip = VideoFileClip(video_path)

        # 씬의 중앙 프레임 추출
        mid_time = (start_time.get_seconds() + end_time.get_seconds()) / 2
        frame = clip.get_frame(mid_time)  # 중앙 프레임 추출 (numpy 배열)

        # 초 단위 시작/종료 시간 포함된 파일 이름 생성
        start_sec = start_time.get_seconds()
        end_sec = end_time.get_seconds()
        scene_image_path = os.path.join(output_folder, f"scene_{i+1:03d}_{start_sec:.2f}-{end_sec:.2f}.png")

        # 이미지 저장
        Image.fromarray(frame).save(scene_image_path)

        # 리소스 해제
        clip.close()

    print("씬 분할 및 이미지 저장이 완료되었습니다!")
