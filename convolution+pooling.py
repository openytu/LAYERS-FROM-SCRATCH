import cv2
import imutils
import numpy as np 

img_path = "gorseller/barkan.jpg"


img = cv2.imread(img_path, cv2.IMREAD_COLOR)
img = imutils.resize(img, height=450)

height = len(img)
width = len(img[0])
channels = len(img[0][0])



conv_tensor = [
    [[1, 1, 1], [1, 0, 5], [-1, -1, -1]],
    [[1, 1, 1], [0, -1, 0], [-1, -1, -1]],
    [[1, 1, 1], [8, 2, 3], [-1, -1, -1]]
]


pad = 1


def ortalama(girdi_vektoru: list):
    return sum(girdi_vektoru) / len(girdi_vektoru)



def evrisim(pad, stride, goruntu, conv_tensor):
    height = len(goruntu)
    width = len(goruntu[0])
    channels = len(goruntu[0][0])

    kernel_size = 3


    padded_height = height + 2 * pad
    padded_width = width + 2 * pad
    padded_img = [[[0, 0, 0] for _ in range(padded_width)] for _ in range(padded_height)]


    for i in range(height):
        for j in range(width):
            padded_img[i + pad][j + pad] = list(goruntu[i][j])



    out_height = ((padded_height - kernel_size) // stride) + 1
    out_width = ((padded_width - kernel_size) // stride) + 1
    output = [[[0, 0, 0] for _ in range(out_width)] for _ in range(out_height)]

 
    for i in range(out_height):
        for j in range(out_width):
            toplam_B = toplam_G = toplam_R = 0
            for a in range(kernel_size):
                for b in range(kernel_size):
                    toplam_B += conv_tensor[a][b][0] * padded_img[i * stride + a][j * stride + b][0]
                    toplam_G += conv_tensor[a][b][1] * padded_img[i * stride + a][j * stride + b][1]
                    toplam_R += conv_tensor[a][b][2] * padded_img[i * stride + a][j * stride + b][2]
            output[i][j] = [int(toplam_B), int(toplam_G), int(toplam_R)]


    for c in range(3):
        min_val = min(output[i][j][c] for i in range(out_height) for j in range(out_width))
        max_val = max(output[i][j][c] for i in range(out_height) for j in range(out_width))
        range_val = max_val - min_val if max_val != min_val else 1
        for i in range(out_height):
            for j in range(out_width):
                output[i][j][c] = int((output[i][j][c] - min_val) * 255 / range_val)

    return np.array(output, dtype=np.uint8)



def havuzlama(tipi="maksimum", pad=1, stride=2, goruntu=None):

    if goruntu is None:
        print("Görüntü verilmedi!")
        return None

    height = len(goruntu)
    width = len(goruntu[0])
    channels = len(goruntu[0][0])

    kernel_size = 3
    padded_height = height + 2 * pad
    padded_width = width + 2 * pad

    padded_img = [[[0,0,0] for _ in range(padded_width)] for _ in range(padded_height)]
    for i in range(height):
        for j in range(width):
            padded_img[i+pad][j+pad] = list(goruntu[i][j])

    out_height = ((padded_height - kernel_size) // stride) + 1
    out_width  = ((padded_width  - kernel_size) // stride) + 1
    if out_height <= 0 or out_width <= 0:
        print("Havuzlama sonrası çıktı boyutu 0! Kernel/Stride/Pad ayarlarını kontrol et.")
        return None

    output = [[[0,0,0] for _ in range(out_width)] for _ in range(out_height)]

    for i in range(out_height):
        for j in range(out_width):
            window = [padded_img[i*stride + m][j*stride + n] for m in range(kernel_size) for n in range(kernel_size)]
            if tipi=="maksimum":
                output[i][j] = [max([p[0] for p in window]), max([p[1] for p in window]), max([p[2] for p in window])]
            elif tipi=="ortalama":
                output[i][j] = [int(ortalama([p[0] for p in window])),
                                int(ortalama([p[1] for p in window])),
                                int(ortalama([p[2] for p in window]))]
            else:
                print("Hatalı havuzlama tipi!")

    return np.array(output, dtype=np.uint8)




output_img = evrisim(pad = pad, stride=1,  goruntu=img, conv_tensor=conv_tensor)

output_img_2 = havuzlama(tipi = "ortalama", pad=1, stride=1, goruntu=output_img)

output_img_3 = evrisim(pad = pad, stride=1,  goruntu=output_img_2, conv_tensor=conv_tensor)

output_img_4 = havuzlama(tipi = "maksimum", pad=1, stride=1, goruntu=output_img_3)

cv2.imshow("Orijinal", img)
cv2.imshow("Evrisim Sonucu", output_img)
cv2.imshow("Evrisim + Maksimum Havuzlama Sonucu", output_img_2)
cv2.imshow("Evrisim + Maksimum Havuzlama + Evrisim Sonucu", output_img_3)
cv2.imshow("Evrisim + Maksimum Havuzlama + Evrisim Sonucu + Maksimum Havuzlama", output_img_4)
cv2.waitKey(0)
cv2.destroyAllWindows()
