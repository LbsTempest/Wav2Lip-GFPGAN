import argparse
import os
import subprocess

import cv2
import numpy as np
from tqdm import tqdm

from GFPGAN_master.inference_gfpgan import main as g_main
from Wav2Lip_master.inference_w2l import main as w2l_main

def main(input_audio, input_video, checkpoint_path, output_path="output") -> None:
    w2l_path = "Wav2Lip_master"
    g_path = "GFPGAN_master"
    lip_synced_output_path = os.path.join(output_path, "result.mp4")
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    w2l_main(input_audio, input_video, checkpoint_path, lip_synced_output_path)
    # subprocess.call()

    unprocessed_frames_folder_path = os.path.join(output_path, "frames")

    if not os.path.exists(unprocessed_frames_folder_path):
        os.makedirs(unprocessed_frames_folder_path)

    vidcap = cv2.VideoCapture(inputVideoPath)
    number_of_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    print("FPS: ", fps, "Frames: ", number_of_frames)

    for frame_number in tqdm(range(number_of_frames)):
        _,image = vidcap.read()
        cv2.imwrite(path.join(unprocessed_frames_folder_path, str(frame_number).zfill(4)+'.jpg'), image)

    g_main(unprocessed_frames_folder_path, output_path)

    restored_frames_path = outputPath + '/restored_imgs/'

    dir_list = os.listdir(restored_frames_path)
    dir_list.sort()

    batch = 0
    batchSize = 300
    for i in tqdm(range(0, len(dir_list), batchSize)):
      img_array = []
      start, end = i, i+batchSize
      print("processing ", start, end)
      for filename in  tqdm(dir_list[start:end]):
          filename = restored_frames_path+filename
          img = cv2.imread(filename)
          if img is None:
            continue
          height, width, layers = img.shape
          size = (width,height)
          img_array.append(img)

    out = cv2.VideoWriter(output_path+'/batch_'+str(batch).zfill(4)+'.avi',cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    batch = batch + 1

    for i in range(len(img_array)):
      out.write(img_array[i])
    out.release()

    concat_text_file_path = output_path + "/concat.txt"
    concat_text_file=open(concat_text_file_path,"w")
    for ips in range(batch):
      concat_text_file.write("file batch_" + str(ips).zfill(4) + ".avi\n")
    concat_text_file.close()

    concatedVideoOutputPath = outputPath + "/concated_output.avi"
    subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', concat_text_file_path, 
        '-c', 'copy', concated_video_output_path
    ], check=True)
    finalProcessedOuputVideo = processedVideoOutputPath+'/final_with_audio.avi'
    subprocess.run([
        'ffmpeg', '-y', '-i', concated_video_path, '-i', input_audio, 
        '-map', '0', '-map', '1:a', '-c:v', 'copy', '-shortest', final_processed_output_video
    ], check=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_audio", type=str)
    parser.add_argument("--input_video", type=str)
    parser.add_argument("--ckpt", type=str)
    args = parser.parse_args()

    main(args.input_audio, args.input_video, args.ckpt)
