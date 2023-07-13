import os
import cv2
import mutagen
import pandas as pd
from moviepy.editor import AudioFileClip, VideoFileClip
#paste here your video paths
#from get_video_points import get_video_points
path_video = 'C:/Users/79778/OneDrive/Рабочий стол/Учеба. Бауманка/нирс/videos/Патология/'
path_points = 'C:/Users/79778/OneDrive/Рабочий стол/Учеба. Бауманка/нирс/points/Патология/'
k = 0
while k != len(os.listdir(path_video)): #преобразование в список
    name = os.listdir(path_video)[k]

    video_full_file_name = path_video + name # путь видео, выбираем видео по названию из директории

    cap = cv2.VideoCapture(video_full_file_name) # захват видео из пакета cv2(класс с методами)
    reader = pd.read_csv(path_points + os.listdir(path_points)[k]) #путь к файлу с точками

    video = mutagen.File(video_full_file_name) #плагин для работы с аудио
    clip = VideoFileClip(video_full_file_name) #делаем переменную клип с видео
    clip.audio.write_audiofile('output_audio.mp3') #создаем файл, где записываем аудио из видео
    audio = AudioFileClip('output_audio.mp3') #переменная с аудио из видео

    audio.write_audiofile('output_audio1.mp3', fps=44100, bitrate=str(video.info.bitrate)) #Битре́йт — количество бит, используемых для передачи/обработки данных в единицу времени.
    #audio = AudioFileClip('output_audio1.mp3')

    success, img0 = cap.read() #считывание кадра
    height = img0.shape[0] #высота
    width = img0.shape[1] #ширина
    FPS = cap.get(cv2.CAP_PROP_FPS) #кадры в секунду
    out = cv2.VideoWriter("output.mp4", -1, FPS, (width, height)) #запись нового видео в файл
    i = -1

    while True:
        success, img = cap.read()

        if success == True: #проходим кадры по одному
            i = i + 1


            if reader['frame_validity'][i] == 'valid': #если файл доступен

                for j in range(19, 59, 38): #проход по средним х в csv файле (верхней и нижней точкам оси)

                    cv2.circle(img, (int(reader.loc[i][j]), int(reader.loc[i][j + 1])), 3, (0, 0, 255), thickness=cv2.FILLED) #рисуем точки cv2.circle(image, center_coordinates, radius, color, thickness)

                    cv2.line(img, (int(reader.loc[i][19]),int(reader.loc[i][20])), (int(reader.loc[i][57]),int(reader.loc[i][58]-50)), (0, 0, 255), 1)
            out.write(img) #оптимизация кода, фиксим баг
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif i == len(reader.loc[:]) - 1:
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    video = VideoFileClip("output.mp4")
    clip = video.set_audio(audio)
    clip.write_videofile('C:/Users/79778/OneDrive/Рабочий стол/Учеба. Бауманка/нирс/videos/РезультатПатология/' + 'new_' + str(name), fps=FPS, codec='libx264')
    k += 1
os.remove("output.mp4")
os.remove("output_audio.mp3")
os.remove("output_audio1.mp3")