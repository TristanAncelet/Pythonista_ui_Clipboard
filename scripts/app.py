import ui
import app_ui
import scripts
import gestures
 
__all__ = ['App']

'''
The App class was mad to be a container/controller for the ui and to manage storage for the multiple sections of clipboards.
'''

#this makes
def make_source_button(App, function, source):
	#this makes a source button and sets each attribute and its action
	import keyboard
	button = ui.Button()
	button.background_color = '#c7c7c7'
	button.title = source.replace('.json','')
	button.border_width = 1
	button.corner_radius = 4
	button.source = source
	button.action = function
	if not keyboard.is_keyboard():
		button.delete_gesture = gestures.long_press(button, App.delete_source,minimum_press_duration=1)
	return button 

class App(object):
	def __setattribute__(self, name, value):
		self.__dict__[name] = value
		
	def __getattr__(self, name):
		return self.__dict__[name]
		
	def __init__(self):
		#these are the lists that are used to
		#store both strings and ui.Buttons that are
		#used in the app
		self.source_buttons = list()
		
	def delete_source(self, data):
		import dialogs
		button = data.view
		if data.began:
			button.bg_color = 'blue'
		if data.ended:
			source_name = button.source_file
			prompt = dialogs.alert('Delete %s?'%source_name, '', 'Yes', 'No', hide_cancel_button = True)
			if prompt == 1:
				self.source_buttons.remove(button)
				self.sources.remove(button.source)
				self.menu_bar.sbc.remove_subview(button)
				scripts.delete_clip_file(source_name)
				self.menu_bar.layout()
			else:
				pass
		
	def set_clipboard_source(self, button):
		#this method sets the file whose content
		#will be displayed on the clipboard ui
		self.Clip_Data_Source.set_source(button.source)
		self.set_clipboard()
		
	def delete_clip(self, clip):
		#this deletes the button associated with
		#the clip as well as from the json source file
		self.clips.remove(clip)
		self.save_clips()
		
	def make_source_buttons(self):
		source = self.Clip_Data_Source
		for source in source.sources:
			button = make_source_button(self, self.set_clipboard_source, source)
			self.source_buttons.append(button)
			
		import keyboard
		if keyboard.is_keyboard():
			self.menu_bar.set_menu()
		else:
			add_source_button = ui.Button()
			add_source_button.image = ui.Image.named('iob:plus_32')
			add_source_button.action = self.add_source
			add_source_button.tint_color = 'white'
			self.source_buttons.append(add_source_button)
			self.menu_bar.set_menu()
		
	def add_source(self, button):
		import dialogs
		prompt = dialogs.input_alert('Add new source', 'New Source file Name?','','Add Source')
		self.sources.append(prompt)
		
		button = make_source_button(self,self.set_clipboard_source,prompt)
		scripts.create_clip_file('%s.json'%(prompt))
		self.menu_bar.sbc.add_subview(button)
		self.source_buttons.insert(-1,button)
		self.menu_bar.layout()
		
	def save_clips(self):
		#saves the current clip list and any additions from the save button to the file
		scripts.save_clips(self.source, self.clips)
		
	def load_clipboard_view(self):
		#loads the clipboard view and inserts itself into the view to allow 
		#the view to access data from/call on the  App object
		self.clipboard = app_ui.ClipBoard(self)
		
	def load_menu_bar(self):
		#same as above
		self.menu_bar = app_ui.Menu_Bar(self)
		
	def set_clipboard(self):
		#sets the items that will be displayed on the Clipboard ui
		self.clipboard.set_items()
		

	def load_data_source(self):
		self.Clip_Data_Source = scripts.Clip_Data_Source(self)
		
	def initialize(self):
		self.load_data_source()
		self.load_menu_bar()
		self.load_clipboard_view()
		self.make_source_buttons()
		self.set_clipboard()
		
	def save_clip(self,clip):
		self.clips.append(clip)
		self.clipboard.clip_table.insert_rows([len(self.clips)-1])
		scripts.save_clip(self.source, clip)
		
		
	def run(self):
		import appex
		import keyboard
		
		if appex.is_running_extension():
			self.clipboard.present()
		elif keyboard.is_keyboard():
			keyboard.set_view(self.clipboard)
		else:
			self.clipboard.present('fullscreen')
			
			
