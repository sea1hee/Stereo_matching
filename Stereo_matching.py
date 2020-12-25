import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Image read as grayscale
left_img_origin = Image.open('left.png')
img_L = left_img_origin.convert('L')  # grayscale
img_L = np.asarray(img_L)

right_img_origin = Image.open('right.png')
img_R = right_img_origin.convert('L')  # grayscale
img_R = np.asarray(img_R)


# Image zero padding
img_L = np.pad(img_L, ((3, 3), (3, 3)), 'constant', constant_values=0)
img_R = np.pad(img_R, ((3, 3), (3, 3)), 'constant', constant_values=0)


# Height and Width
H, W = img_L.shape


# Patch size
patch_size = 7
half_size = patch_size // 2


# Declare depth map
depth = np.zeros(img_L.shape)

for i in range(half_size, H - half_size):
    print(".", end="", flush=True)  # let the user know that computation is on going
    
    '''
        Image의 Height에 해당하는 픽셀마다 Disparity Space Image 구하기
    '''

    # Disparity Space Image 값을 저장할 zero 배열 선언
    dsi = np.zeros((W,W))
    for j in range(half_size, W - half_size):
        mask_R = img_R[i-half_size:i+half_size + 1, j-half_size:j+half_size + 1]  # Patch from right image
        for k in range(half_size, W-half_size):
            mask_L = img_L[i-half_size:i+half_size + 1, k-half_size:k+half_size + 1]  # Patch from left image
            # 배열의 값은 Right patch 값과 Left patch 값의 차이
            dsi[j,k] = np.sum(abs(mask_R - mask_L))

    
    '''
        구해진 DSI로 Dynamic Programming
    '''
    # occlusionCost는 각 픽셀별로 100으로 둔다
    occlusionCost = 100*patch_size*patch_size

    # 해당 픽셀까지의 최저 코스트를 저장할 2차원 배열, 각 픽셀에서 어디로 가는지 방향을 저장할 2차원 배열 선언
    C = np.zeros((W,W))
    M = np.zeros((W,W))
    
    # C의 초기값을 저장해줌, dsi patch로 계산했기 때문에 [0,0]부터 값이 저장되어 있는 게 아니라, [half_size, half_size]부터 값이 저장되어 있다.
    for x in range(W):
         C[x,half_size] = x*occlusionCost
         C[half_size,x] = x*occlusionCost
         
    # DSI 첫 값 [half_size+1, half_size+1]부터 M 배열 채우기
    for x in range(half_size+1,W):
        for y in range(half_size+1,W):
            min1=C[x-1,y-1]+abs(dsi[x,y])
            min2=C[x-1,y]+occlusionCost
            min3=C[x,y-1]+occlusionCost
            C[x,y]=cmin=min([min1,min2,min3])
            if(min1==cmin):
                M[x,y]=1
            if(min2==cmin):
                M[x,y]=2
            if(min3==cmin):
                M[x,y]=3
    
    # M 배열을 통해 우측하단에서 좌측상단으로 올라가는 과정
    # 시작점은 [W-half_size, W-half_size]
    x=W-half_size-1
    y=W-half_size-1
    
    # 종료점은 x 값이나 y 값이 올라가면서 왼쪽 끝이나 위쪽 끝에 닿았을 경우
    while(x!=half_size and y!=half_size):
        if M[x,y]==1:
            depth[i,x]=abs(x-y)
            x-=1
            y-=1
        elif M[x,y]==2:
            x-=1
        elif M[x,y]==3:
            y-=1
            

'''
    Occlusion 최대한 없애보기
'''
for x in range(depth.shape[0]):
    for y in range(depth.shape[1]):
        # Occlusion 발견
        if depth[x,y] == 0:
            # 같은 선상에서 값을 가진 것 찾기
            for z in range(y, depth.shape[1]):
                if depth[x,z] != 0:
                    # Occlusion 좌측 값과 찾은 값의 평균을 해당 Occlusion에 넣기
                    depth[x,y] = (depth[x,y-1] + depth[x,z])//2
                    break
                # 만약 같은 선상에서 값을 찾지 못한 경우, Occlusion의 좌측 값 넣기
                depth[x,y] = depth[x,y-1]

'''
    결과 이미지 출력
'''
# Plot
plt.subplot(131); plt.imshow(np.asarray(left_img_origin)); plt.axis('off')
plt.subplot(132); plt.imshow(np.asarray(right_img_origin)); plt.axis('off')
plt.subplot(133); plt.imshow(depth, cmap='gray'); plt.axis('off')
plt.show()
