# movieseq_prototype
DSLAB streamlit을 이용한 movieseq 프로토타입 개발

```
streamlit run app.py
```

### 파일 구성
<b>app.py</b>  
프로젝트의 메인 코드로, Streamlit 기반의 UI와 주요 실행 흐름을 담당합니다.

<b>utils.py</b>  
다양한 보조 함수들이 모여 있는 파일로, 비디오 저장, 이미지 파일 관리, ChatGPT 쿼리 전송 등의 기능을 포함합니다.

<b>scene_extractor.py</b>  
비디오에서 씬 전환을 감지하고, 각 씬의 이미지를 추출하는 기능이 구현되어 있습니다.

<b>video_upgrade.py</b>  
Streamlit의 기본 비디오 입력 용량(200MB)을 확장하기 위해 일회성으로 실행하는 코드입니다. 현재 프로젝트에서는 비디오 입력 용량을 500MB로 설정했습니다.

### 폴더 구조
<b>temp/</b>  
업로드된 비디오 파일이 임시로 저장되는 디렉터리입니다.

<b>output_scenes/</b>  
씬 전환 감지를 통해 추출된 이미지가 저장되는 디렉터리입니다.