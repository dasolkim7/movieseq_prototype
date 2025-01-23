import os

# .streamlit 디렉토리 생성
streamlit_dir = os.path.expanduser("~/.streamlit")
os.makedirs(streamlit_dir, exist_ok=True)

# config.toml 파일 생성
config_file_path = os.path.join(streamlit_dir, "config.toml")

# 올바른 내용 작성
config_content = """
[server]
maxUploadSize = 500
"""

# 파일 쓰기
with open(config_file_path, "w", encoding="utf-8") as f:
    f.write(config_content)

print(f"Streamlit 설정 파일이 생성되었습니다: {config_file_path}")
