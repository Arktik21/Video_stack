from threading import Thread
import cv2, time
import numpy as np
import sounddevice as sd, soundfile as sf
import subprocess
import os

class AudioStreamWidget(object):
	def __init__(self, src=0, path_to_save=''):
		self.sps = 16000
		sd.default.device = src
		# Start the thread to read frames from the video stream
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()
		self.full_record = np.zeros((1, 1))
		self.path = path_to_save

	def update(self):
		# Read the next frame from the stream in a different thread
		while True:
			record_voice = sd.rec(int(self.sps * 1), self.sps, channels=1)
			sd.wait()
			self.full_record = np.append(self.full_record, record_voice)

	def save_audio(self):
		sf.write(self.path + 'audio.wav', self.full_record, self.sps)


class VideoStreamWidget(object):
	def __init__(self, src, path_to_save, file_name):
		self.fps = 25.0
		self.path = path_to_save
		self.capture = cv2.VideoCapture(src)
		self.thread = Thread(target=self.update, args=())
		self.thread.daemon = True
		self.thread.start()
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		self.out = cv2.VideoWriter(self.path + file_name + '.mp4', fourcc, 25.0, (640, 480))


	def update(self):
		while True:
			if self.capture.isOpened():
				(self.status, self.frame) = self.capture.read()
				self.out.write(self.frame)
			#time.sleep(1/self.fps)

	def save_video(self):
		self.capture.release()
		self.out.release()


def show_frame(video_stream_widget):
	frames = []
	for device in video_stream_widget:
		frames.append(device.frame)
	cv2.imshow('frame',  np.concatenate(frames, axis=1))


if __name__ == '__main__':
	path = './test_samples/'
	path = ''
	#print(sd.query_devices())
	audio_dev = len(sd.query_devices())-1#int(input('select dev'))
	devises = [0,2,4]
	video_stream_widget = []

	for devise in devises:
		video_stream_widget.append(VideoStreamWidget(src=devise, path_to_save=path, file_name=str(devise)))

	#audio_dev = 25
#	video_stream_widget1 = VideoStreamWidget(src=0,  path_to_save=path, file_name='customer')
#	video_stream_widget2 = VideoStreamWidget(src=2,  path_to_save=path, file_name='manager')

	while True:
		try:
			show_frame(video_stream_widget)
		except AttributeError:
			pass
		key = cv2.waitKey(1)
		if key == ord('q'):
			for devise in video_stream_widget:
				devise.save_video()
			cv2.destroyAllWindows()
			break







