# Google Cloud Speech to Text 인수인계

### Google Cloud Account for Pino,Able


## Env Setting : 
python2 환경에서 pip 설치 되고 있는지 확인 할 것

## Simple installation instructions
* Cloud Speech API 키 발급 받기
* Cloud SDK 설치 -> google-cloud-speech install
* ./bashrc 파일 수정

## After install google-cloud-speech library : 
src_pino 파일 안의 pino_wave와 pino_msg 코드를 가져와서 사용하면 됨
```
$ rosrun pino_wave pino_stt.py
$ rosrun pino_wave pino_think.py
```

## Installation Troubleshooting :
* pip install pyaudio 설치 에러 발생시 
  * [링크](https://blog.naver.com/PostView.nhn?blogId=chandong83&logNo=220770569956&categoryNo=65&parentCategoryNo=0&viewDate=&currentPage=1&postListTopCurrentPage=1&from=postView) 참고

* pip install google-cloud-sppech 설치 에러 발생 시
  * pyasn1 관련 에러 발생 시 [링크](https://blog.softhints.com/python-dependency-error-modules-has-requirement-which-is-incompatible/) 참고
  * permission error가 뜨면 sudo 권한으로 설치 해 줄 것 (시간 좀 걸림 - 기다리면 됨)

## References : 
> 전체 설치 방법 및 구글클라우드  키 받는 방법
* https://webnautes.tistory.com/1247
* https://cloud.google.com/sdk/docs/quickstart-linux?authuser=3
> bash 파일 수정 방법
* https://jungwoon.github.io/google%20cloud/2018/01/17/Speech-Api/
