import ui
from scripts import Organize as Org

__all__ = ['Menu_Bar']

class Menu_Bar(ui.View):
	def __init__(self,App):
		self.App = App
		self.background_color = '#626262'
		
		self.save_button = save_button = ui.Button()
		save_button.image = ui.Image.named('iow:ios7_download_outline_32')
		self.save_button = save_button
		save_button.background_color = '#bbc4bb'
		
		source_buttons_container = self.sbc = ui.ScrollView()
		self.sbc.shows_horizontal_scroll_indicator = False
		self.sbc.border_width = 1
		self.sbc.shows_vertical_scroll_indicator = False
		self.add_subview(source_buttons_container)
		#self.corner_radius = 4
		#self.background_color = 'white'
		save_button.action = self.App.Clip_Data_Source.save_clip
		self.add_subview(save_button)
		
	def set_menu(self):
		import keyboard
		
		for button in self.App.source_buttons:
			self.sbc.add_subview(button)
		self.layout()
	
	def set_clips(self,button):
		filename = '%s.json'%button.title
		#print(filename)
		self.App.Clip_Data_Source.set_clipboard_source(filename)
		
	def layout(self):
		save_button = self.save_button
		save_button.height = self.height
		save_button.width = self.height
		self.sbc.width = self.width - save_button.width
		
		self.sbc.height = self.height
		self.sbc.x = save_button.width
		
		Org.horiz(parent_view = self.sbc,view_list = self.App.source_buttons,dim = (100,self.sbc.height), gap = (0,4))
