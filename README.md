Stereo matching using Dynamic Programming and DSI
===============
Computer Vision Project   

Description
-----------
Stero System에서 두 이미지 사이의 Matching Point를 찾는 것을 Stero matching이라고 한다. 좌, 우 이미지 간 이미지 속 물체가 얼마나 움직였는지를 찾아낸다. 카메라와 가까이 있는 물체라면 많이 움직였을 것이고, 멀리 있는 물체라면 상대적으로 적게 움직였을 것이다. 이러한 성질을 이용해 depth map을 결과물로 도출한다.   



Stereo mathcing
---------------

<img width="500" src="https://user-images.githubusercontent.com/22738293/103155765-fba66100-47e5-11eb-9304-30ed8437bbb4.png">


Left Image를 기준으로 Left Image의 Height 픽셀 마다 일정 크기의 패치를 만들어 Right Image에서 같은 선상에서 찾는다. 해당  차이 값을 저장해 놓은 것이 Disparity Space Image(DSI)이다. DSI는 기준이 되는 Image의 Height 픽셀 개수 만큼 생성된다.     

<img width="200" src="https://user-images.githubusercontent.com/22738293/103155795-298ba580-47e6-11eb-992c-f3610000746d.png">


DSI 는 위 사진을 기준으로, Height 픽셀의 n 번째에 해당하는 Left Image의 n번째 scanline과 Right 이미지의 n번째에 해당하는 scanline의 차이 값을 담은 이미지이다. 여기서 가장 어두운 값들을 찾아내는 것이 Corresponding point를 찾는 것이다.   


Dynamic Programming은 두 가지 단계로 구성된다. 로컬 위치마다 그 위치에서의 가장 작은 cost와 direction을 저장해 놓는다. End point에서 start point로 거꾸로 optimal한 direction을 따라가며 최종 path를 찾는다. Dynamic Programming은 모든 path의 값을 계산하지 않으면서 적절한 global solution을 얻을 수 있다.   

이 후, 값에 대해 Occlusion을 채워줄 수 있는 간단하 알고리즘을 수행한다.

Result
------
<img width="800" src="https://user-images.githubusercontent.com/22738293/103155851-8c7d3c80-47e6-11eb-8b16-f41a41b66179.png">

