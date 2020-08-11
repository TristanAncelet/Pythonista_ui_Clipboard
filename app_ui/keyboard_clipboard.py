import ui,gestures
from scripts import vert

__all__ = ['ClipBoard']

class ClipBoard(ui.View):
	def __init__(self,App):
		#gestures.disable_swipe_to_close(self)
		self.background_color = 'white'
		self.App = App
		self.scrollview = ui.ScrollView()
		self.scrollview.border_width = 1
		self.add_subview(self.scrollview)
		self.buttons = list()
		
		self.menu = App.menu_bar
		self.add_subview(self.menu)
		
	def set_items(self):
		
		self.buttons = self.App.clip_buttons
		for item in self.buttons:
			self.scrollview.add_subview(item)
		self.layout()
	def reset_clipboard(self):
		for item in self.buttons:
			self.scrollview.remove_subview(item)
		self.buttons.clear()
	def layout(self):
		menu = self.menu
		menu.width = self.width
		menu.height = 32
		if self.buttons:
			
			#settings = self.App.settings
			scrollview = self.scrollview
			scrollview.frame = (0,menu.height,self.width,self.height-menu.height)
			
			#dim = settings['dim']
			#gap = settings['gap']
			
			items = self.buttons
			
				
			gap = (4,4)
			v_gap, h_gap = gap
			number_of_items_wanted_on_screen = i = 4
			width = self.width - 2*h_gap
			height = (self.height/i)-v_gap * (i+1) 
			dim = (width,height)
			
			number_of_items = i = len(items)
			total_height_of_items = height*i + v_gap*(i+1)
			
			if total_height_of_items > scrollview.height:
				scrollview.content_size = (self.width,total_height_of_items)
			else:
				scrollview.content_size = (scrollview.width,scrollview.height)
			vert(dim = dim,view_list = items, gap = gap)
		else:
			pass
		
