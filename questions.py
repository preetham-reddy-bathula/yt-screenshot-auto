import cv2
import numpy as np
import os
import glob

input_folder = '<VIDEOS PATH>'  

output_folder = '<output for imgs>'  

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

video_files = glob.glob(os.path.join(input_folder, '*.mp4'))  

lower_green = np.array([35, 50, 50])
upper_green = np.array([75, 255, 255])

def has_green_text(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    green_area = cv2.countNonZero(green_mask)
    return green_area > 0

for video_file in video_files:
    video = cv2.VideoCapture(video_file)

    if not video.isOpened():
        print(f"Error: Could not open the video file {video_file}")
        continue

    frame_rate = int(video.get(cv2.CAP_PROP_FPS))
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count // frame_rate

    output_count = 0
    ret, prev_frame = video.read()
    green_detected = False

    for time in range(10, duration, 10):
        frame_idx = time * frame_rate
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, current_frame = video.read()

        if ret:
            if not green_detected and has_green_text(current_frame):
                output_filename = f'output_{os.path.basename(video_file).split(".")[0]}_{output_count:03d}.png'
                output_filepath = os.path.join(output_folder, output_filename)
                cv2.imwrite(output_filepath, prev_frame)
                output_count += 1
                print(f"Saved frame {frame_idx - frame_rate} from {video_file} as {output_filename}")
                green_detected = True
            elif not has_green_text(current_frame):
                green_detected = False

            prev_frame = current_frame
        else:
            print(f"Error: Could not read frame at {time} seconds in {video_file}")

    video.release()