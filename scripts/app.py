import ui
from app_ui import *
from scripts import *
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
	button.title = source
	button.border_width = 1
	button.corner_radius = 4
	button.source_file = source+'.json'
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
		self.clips = list()
		self.clip_buttons = list()
		self.sources = list()
		self.source_buttons = list()
		#when you open the app this is the
		#default source
		self.source = 'clips.json'
		
	def check_pasteboard(self):
		import clipboard
		#this method checks the string currently stored
		#on the IOs pasteboard and saves it in the general
		#clips category if it isn't already
		clip = clipboard.get()
		if clip in self.clips:
			pass
		else:
			self.clips.append(clip)
			self.save_clips()
	def delete_source(self, data):
		import dialogs
		button = data.view
		if data.began:
			button.bg_color = 
		if data.ended:
			button = data.view
			source_name = button.source_file
			prompt = dialogs.alert('Delete %s?'%source_name,'','Yes','No',hide_cancel_button=True)
			if prompt == 1:
				self.source_buttons.remove(button)
				self.sources.remove(button.source)
				save_sources(self.sources)
				self.menu_bar.sbc.remove_subview(button)
				delete_clip_file(source_name)
				self.menu_bar.layout()
			else:
				pass
		
	def set_clipboard_source(self, button):
		#this method sets the file whose content
		#will be displayed on the clipboard ui
		self.source = button.source_file
		self.clipboard.reset_clipboard()
		self.load_clips()
		self.make_clip_buttons()
		self.set_clipboard()
		
	def delete_clip(self, clip_button):
		#this deletes the button associated with
		#the clip as well as from the json source file
		self.clips.remove(clip_button.clip)
		self.save_clips()
		self.clipboard.scrollview.remove_subview(clip_button)
		self.clipboard.layout()
	def load_sources_file(self):
		self.sources = load_file('sources.json')
	
	def make_source_buttons(self):
		for source in self.sources:
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
		save_sources(self.sources)
		button = make_source_button(self,self.set_clipboard_source,prompt)
		create_file('%s.json'%(prompt))
		self.menu_bar.sbc.add_subview(button)
		self.source_buttons.insert(-1,button)
		self.menu_bar.layout()
	def load_clips(self):
		#this is a function from file_functions.py that 
		#opens the source file and reads the clips within the file and returns the list
		self.clips = get_clips(self.source)
		
	def make_clip_buttons(self):
		#implemented in case this is used to make new buttons when switching to
		#a new source file
		if len(self.clip_buttons) is not 0:
			self.clip_buttons.clear()
		else:
			pass
		#this iterates through the list of strings 
		#and implements as a custom ui.View named Clip_View
		for clip in self.clips:
			clip_button = Clip_View(self, clip = clip)
			
			#not implemented yet but if you have a source file named links.json 
			#you will be able to open them up in an internal web browser
			if clip_button.clip_is_url():
				clip_button.enable_browser_gesture()
			self.clip_buttons.append(clip_button)
			
	def save_clips(self):
		#saves the current clip list and any additions from the save button to the file
		save_clips(self.source, self.clips)
		
	def load_clipboard_view(self):
		#loads the clipboard view and inserts itself into the view to allow 
		#the view to access data from/call on the  App object
		self.clipboard = ClipBoard(self)
		
	def load_menu_bar(self):
		#same as above
		self.menu_bar = Menu_Bar(self)
		
	def set_clipboard(self):
		#sets the items that will be displayed on the Clipboard ui
		self.clipboard.set_items()
		
	def initialize(self):
		self.load_menu_bar()
		self.load_clipboard_view()
		self.load_clips()
		self.load_sources_file()
		self.make_source_buttons()
		self.make_clip_buttons()
		self.set_clipboard()
		
	def save_clip(self,clip):
		self.clips.append(clip)
		self.make_clip_buttons()
		save_clip(self.source, clip)
		self.set_clipboard()
		
	def run(self):
		import appex
		import keyboard
		
		if appex.is_running_extension():
			self.clipboard.present()
		elif keyboard.is_keyboard():
			keyboard.set_view(self.clipboard)
		else:
			self.clipboard.present('fullscreen')
			
			
