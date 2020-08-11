import ui
import gestures

__all__ = ['Clip_View']
def is_url(clip):
	#uses regex and the general url schema (https://www.domain.com) to verify if 
	#the clip is an url 
	import re
	url_scheme = r'\w+:\/\/(\w+\.)?\w+\.\w+'
	matcher = re.compile(url_scheme)
	
	if matcher.match(clip):
		return True
	else:
		return False
		
class Clip_View(ui.View):
	def __init__(self, App, clip = str()):
		self.App = App
		self.clip = clip
		self.border_width = 2
		self.corner_radius = 5
		self.update_interval = 1
		
		clip_button = ui.Button()
		clip_button.title = clip
		clip_button.action = self.insert_clip
		self.clip_button = clip_button
		self.add_subview(clip_button)
		
		
		delete_button = ui.Button()
		delete_button.action = self.delete
		delete_button.title = 'Delete?'
		delete_button.bring_to_front()
		delete_button.hidden = True
		delete_button.background_color = '#a4aca4'
		self.delete_button = delete_button
		self.add_subview(delete_button)
		gestures.long_press(clip_button,self.copy_clip_to_clipboard)
		self.show_del_gesture = gestures.swipe(clip_button,self.show_button,direction = gestures.LEFT)
		self.hide_del_gesture = gestures.swipe(delete_button,self.hide_button,direction = gestures.RIGHT)
		self.show_del_gesture.before(self.hide_del_gesture)
		
		self.browser_button = ui.Button()
		self.browser_button.action = self.open_in_browser
		self.add_subview(self.browser_button)
		self.browser_button.hidden = True
		self.browser_button.background_color = '#a4aca4'
		self.browser_button.title = 'Open in Browser'
		self.browser_button.bring_to_front()
		
	def enable_browser_gesture(self):
		#has not been implememebted yet
		#the browser gesture will replace the clip button with the "open in browser" button
		#which will open a browser and load the webpage associated with the url/clip
		show = gestures.swipe(self.clip_button,self.show_browser,direction = gestures.RIGHT)
		hide =gestures.swipe(self.browser_button,self.hide_browser,direction = gestures.LEFT)
		show.before(hide)
		
	def show_browser(self, data):
		self.browser_button.hidden = False
		
	def hide_browser(self, data):
		self.browser_button.hidden = True
		
	def update(self):
		if self.clip_button.title is not self.clip:
			self.clip_button.title = self.clip 
		else:
			pass
		
	def open_in_browser(self,button):
		'''
		import webbrowser
		import clipboard
		import urllib
		import re
		url = self.clip
		url = urllib.parse.quote_plus(url)
		callback = "googlechrome-x-callback://x-callback-url/open/?url=YOURL&x-source=Safari&x-success=YOURL"	
		callback = re.sub("YOURL", url, callback)
		webbrowser.open(callback)
		'''
		pass
	def hide_button(self, data):
		self.delete_button.hidden = True
		
	def insert_clip(self,button):
		import keyboard
		keyboard.insert_text(self.clip)
		
	def copy_clip_to_clipboard(self, data):
		import clipboard
		clipboard.set(self.clip)
		self.clip_button.title = 'Copied to clipboard'
		
	def show_button(self, data):
		self.delete_button.hidden = False
		
	def delete(self, button):
		button.hidden = True
		self.App.clipboard.buttons.remove(self)
		self.App.clipboard.layout()
		self.App.delete_clip(self)
		
	def layout(self):
		clip_button = self.clip_button
		clip_button.frame = self.bounds
		
		del_button = self.delete_button
		del_button.frame = self.bounds
		
		brow_button = self.browser_button
		brow_button.frame = self.bounds
		
	def clip_is_url(self):
		return is_url(self.clip)
