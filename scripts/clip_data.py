import ui

__all__ = ['Clip_Data_Source']

class Clip_Data_Source (object):
	def __init__(self, App):
		self.App = App
		self.cells = list()
		self.load_clip_sources()
		self.load_clip_source()
	def load_clip_sources(self):
		import os
		self.sources = os.listdir('files')
		self.sources.remove('images')
		if len(self.sources) == 0:
			self.create_file('default.json')
			self.load_clip_sources()
		else:
			self.current_source = self.sources[0]
	def set_source(self, source):
		self.current_source = source
		self.load_clip_source()
	def create_file(self, filename):
		import os
		import json
		path = os.path.join('files',filename)
		with open(path, 'w', encoding = 'utf-8') as file:
			json.dump(['this is a new file'], file)
			file.close()
			
	def load_clip_source(self):
		self.cells.clear()
		import os
		import json
		file_path = os.path.join('files',self.current_source)
		with open(file_path,'r',encoding = 'utf-8') as file:
			self.clips = json.load(file)
			file.close()
			
	def save_clips(self):
		import os
		import json
		filepath = os.path.join('files',self.current_source)
		with open(filepath, 'w', encoding = 'utf-8') as file:
			json.dump(self.clips, file)
			file.close()
			
	def save_clip(self, button):
		import os
		import clipboard
		#since there is no way to check if there is an image or text in the clipboard 
		#beforehand we will just first check for an image, and if "None" is recieved the 
		#clip is assumed to be text
		if clipboard.get_image() is None:
			clip = clipboard.get()
			self.clips.append(clip)
		else:
			clip_image = clipboard.get_image()
			cwd = os.getcwd()
			image_folder_path = os.path.join(cwd, 'files', 'images')
			#the image name will be determined by the current file count +1
			file_name = str(len(os.listdir(image_folder_path))+1)+'.jpeg'
			file_path = os.path.join(image_folder_path,file_name)
			clip_image.save(file_path)
			self.clips.append(file_path)
		self.save_clips()
		self.App.clipboard.set_items()
			
#this section deals with how the table handles the data in the clip source
	def tableview_number_of_sections(self, tableview):
		#since we are only displaying a single source at a time we will leave it as 1
		return 1
		
	def tableview_number_of_rows(self, tableview, section):
		#thia tells the tableview the number of clips in the source file, of which it will prepare that many spaces
		return len(self.clips)
		
	def tableview_cell_for_row(self, tableview, section, row):
		import ui
		import os
		clip = self.clips[row]
		cell = ui.TableViewCell()
		#this checks if the clip is a path to an image file
		#
		if os.path.isfile(clip):
			import ui
			image = ui.Image.named(clip)
			cell.image_view.image = image
			cell.height, cell.width = image.size
			
		else:
			cell.text_label.text = clip
		self.cells.append(cell)
		return cell
		
	def tableview_title_for_header(self, tableview, section):
		return self.current_source.replace('.json','')
	def tableview_can_delete(self, tableview, section, row):
		return True
	def tableview_can_move(self, tableview, section, row):
		return True
	def tableview_delete(self, tableview, section, row):
		import os
		clip = self.clips[row]
		if os.path.isfile(clip):
			os.remove(clip)
		self.clips.remove(clip)
		self.save_clips()
		tableview.delete_rows([row])
	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		pass
	
#this section deals with how the program handles the TableView's behavior
	def tableview_did_select(self, tableview, section, row):
		clip = self.clips[row]
		import os
		import keyboard
		import clipboard
		if os.path.isfile(clip):
				cell = self.cells[row]
				image = cell.image_view.image
				clipboard.set_image(image)
		else:
			if keyboard.is_keyboard():
				keyboard.insert_text(clip)
			else:
				clipboard.set(clip)
		
	def tableview_did_deselect(self, tableview, section, row):
		pass
	def tableview_title_for_delete_button(self, tableview, section, row):
		return 'Delete'
