import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

points = rs.points()
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)
profile = pipeline.start(config)

# try:
#     while True:
#         frames = pipeline.wait_for_frames()
#         nir_lf_frame = frames.get_infrared_frame(1)
#         # nir_rg_frame = frames.get_infrared_frame(2)
#         nir_rg_frame = frames.get_color_frame()
#         if not nir_lf_frame or not nir_rg_frame:
#             continue
#         nir_lf_image = np.asanyarray(nir_lf_frame.get_data())
#         nir_rg_image = np.asanyarray(nir_rg_frame.get_data())
#         # horizontal stack
#         image=np.hstack((nir_lf_image,nir_rg_image))
#         cv2.namedWindow('NIR images (left, right)', cv2.WINDOW_AUTOSIZE)
#         cv2.imshow('IR Example', image)
#         key = cv2.waitKey(1)
#         # Press esc or 'q' to close the image window
#         if key & 0xFF == ord('q') or key == 27:
#             cv2.destroyAllWindows()
#             break
# finally:
#     pipeline.stop()

for x in range(5):
    pipeline.wait_for_frames()

frameset = pipeline.wait_for_frames()
color_frame = frameset.get_color_frame()
print(np.size(color_frame))

#depth_frame = frameset.get_depth_frame()

pipeline.stop()
print('frames captures\n')
color_frame = np.asanyarray(color_frame.get_data())
cv2.imshow("color",color_frame)
