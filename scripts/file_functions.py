__all__ = ['save_clip','delete_clip_file','create_clip_file']

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

def save_clip(filename,clip):
	clips = get_clips(filename)
	if clip in clips:
		pass
	else:
		clips.append(clip)
	save_clips(filename,clips)

