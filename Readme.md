# AfterTrip
> 현재 서버 종료된 상태입니다.

## 개발환경
![image](https://img.shields.io/badge/django-092E20?style=flat&logo=Django&logoColor=white)
![image](https://img.shields.io/badge/nginx-009639?style=flat&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/docker-2496ED?style=flat&logo=docker&logoColor=white)
![image](https://img.shields.io/badge/mysql-4479A1?style=flat&logo=mysql&logoColor=white)
<br>
![image](https://img.shields.io/badge/aws-232F3E?style=flat&logo=amazonaws&logoColor=white)
![image](https://img.shields.io/badge/amazonec2-FF9900?style=flat&logo=amazonec2&logoColor=white)
![image](https://img.shields.io/badge/amazonrds-527FFF?style=flat&logo=amazonrds&logoColor=white)
![image](https://img.shields.io/badge/amazons3-569A31?style=flat&logo=amazons3&logoColor=white)
<br>
![image](https://img.shields.io/badge/githubactions-2088FF?style=flat&logo=githubactions&logoColor=white)

## 기능 소개
(organization readme 바로가기 링크?)

## ERD
![image](https://user-images.githubusercontent.com/86969518/236693791-f41020d2-c179-4852-a5f7-3dadd0ea4bb7.png)

## API 문서
프론트엔드 개발자와의 협업을 위한 API 문서를 작성하기 위해 노션을 이용했다.  
노션을 이용한 API 문서는 생성, 수정이 간편하다는 장점이 있다.

![image](https://github.com/JeongHyoYeon/Capstone-BE/assets/86969518/380261fa-32a2-4e5c-b768-7d9f3c7bbf1d)
![image](https://github.com/JeongHyoYeon/Capstone-BE/assets/86969518/eb5573a1-28ce-40e3-9dda-6f3f6fd17314)
![image](https://github.com/JeongHyoYeon/Capstone-BE/assets/86969518/176a2ce0-e04b-4d3e-8c16-4b110ed5a55e)

## Directory 구조
```
tripfriend
├── accounts
│   ├── migrations
│   └── views
├── base
│   └── migrations
├── config
│   ├── docker
│   ├── nginx
│   └── scripts
├── photos
│   ├── migrations
│   └── views
│       └── photo_views
├── tripfriend
│   └── settings
└── trips
    └── migrations
```

**Django project name**: tripfriend (변경 전 이름)  
**Django apps**: base, accounts, trips, photos



### 참고: 개발 블로그
[AfterTrip: 개발 최종 정리 \[백엔드\]](https://velog.io/@jeonghyun/AfterTrip-개발-최종-정리-백엔드)