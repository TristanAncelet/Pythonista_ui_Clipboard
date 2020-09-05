import ui,gestures
from scripts import vert

__all__ = ['ClipBoard']

class ClipBoard(ui.View):
	def __init__(self,App):
		#gestures.disable_swipe_to_close(self)
		self.background_color = 'white'
		self.App = App
		self.clip_table = clip_view = ui.TableView()
		clip_view.delegate = self.App.Clip_Data_Source
		clip_view.data_source = self.App.Clip_Data_Source
		self.add_subview(self.clip_table)
		
		self.menu = App.menu_bar
		self.add_subview(self.menu)
		
	def set_items(self):
		self.clip_table.reload()
		
	def layout(self):
		menu = self.menu
		menu.width = self.width
		menu.height = 32
		
		scrollview = self.clip_table
		scrollview.frame = (0,menu.height,self.width,self.height-menu.height)

