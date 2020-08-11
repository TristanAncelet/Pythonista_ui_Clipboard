__all__ = ['get_clips','save_clip','save_clips','delete_clip_file','create_clip_file','get_clip_filenames']

def delete_clip_file(filename):
	import os
	file_dir = 'files'
	cwd = os.getcwd()
	file_path = os.path.join(cwd, file_dir, filename)
	os.remove(file_path)

def create_clip_file(filename, dir = 'files'):
	import os
	import json
	file_path = os.path.join(dir,filename)
	
	with open(file_path, 'w', encoding = 'utf-8') as file:
		json.dump(['this is a new file'],file)
		file.close()

def get_clips(filename):
	import os
	import json
	
	current_dir = os.getcwd()
	files_dir_name = 'files'
	clip_dir = os.path.join(current_dir,files_dir_name,filename)
	
	try:
		with open(clip_dir,'r') as file:
			clips = json.load(file)
			file.close()
		return clips
	except:
		create_clip_file(filename)
		clips = get_clips(filename)

def save_clips(filename,clips):
	import os,json
	current_dir = os.getcwd()
	files_dir_name = 'files'
	
	clip_dir = os.path.join(current_dir,files_dir_name,filename)
	
	with open(clip_dir,'w',encoding = 'utf-8') as file:
		json.dump(clips,file)
		file.close()

def save_clip(filename,clip):
	clips = get_clips(filename)
	if clip in clips:
		pass
	else:
		clips.append(clip)
	save_clips(filename,clips)
	
def get_clip_filenames():
	import os
	current_dir = os.getcwd()
	path = os.path.join(current_dir, 'files')
	file_list = os.listdir(path)
	
	if len(file_list) == 0:
		create_clip_file('default.json')
		file_list = get_clip_filenames()
	return file_list
