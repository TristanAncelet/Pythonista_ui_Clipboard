__all__ = ['get_clips','save_clip','save_clips','load_file','save_sources','delete_clip_file','create_file']

def delete_clip_file(filename):
	import os
	file_dir = 'files'
	cwd = os.getcwd()
	file_path = os.path.join(cwd, file_dir, filename)
	os.remove(file_path)

def create_file(filename, dir = 'files'):
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
		create_file(filename)
		clips = get_clips(filename)

def save_clips(filename,clips):
	import os,json
	current_dir = os.getcwd()
	files_dir_name = 'files'
	
	clip_dir = os.path.join(current_dir,files_dir_name,filename)
	
	with open(clip_dir,'w',encoding = 'utf-8') as file:
		json.dump(clips,file)
		file.close()

def load_file(filename,dir = 'files',json = True):
	import os
	import json
	
	if json is True and '.json' not in filename:
		filename = filename + '.json'
	else:
		pass
		
	cwd = os.getcwd()
	file_path = os.path.join(cwd,dir,filename)
	with open(file_path, 'r', encoding = 'utf-8') as file:
		sources = json.load(file)
		file.close()
	return sources

def save_sources(sources,filename = 'sources.json',dir = 'files',json = True):
	import os
	import json
	
	if json is True and '.json' not in filename:
		filename = filename + '.json'
	else:
		pass
		
	cwd = os.getcwd()
	file_path = os.path.join(cwd,dir,filename)
	with open(file_path, 'w', encoding = 'utf-8') as file:
		sources = json.dump(sources,file)
		file.close()
	return sources
	
	
def save_clip(filename,clip):
	clips = get_clips(filename)
	if clip in clips:
		pass
	else:
		clips.append(clip)
	save_clips(filename,clips)
