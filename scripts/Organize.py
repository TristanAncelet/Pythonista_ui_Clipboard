'''
This file contains functions and classes to help organize your ui views.
'''

__all__ = ['horiz', 'vert', 'grid', 'View_Handler']

def horiz(parent_view = None, ref_view = None, auto_sizing = True, view_list = list(), dim = (100,200), gap = (4,4), views_on_screen = 4):
	import ui
	v_gap, h_gap = gap

	if auto_sizing == True:
		import math
		view_width = math.floor((parent_view.width/views_on_screen) - (h_gap*views_on_screen))
		view_height = parent_view.height - 2 * gap
	else:
		view_width, view_height = dim
	
	#horizontal (x) displacement of each view
	x = lambda i: (view_width*i + h_gap*(i+1))
	if type(parent_view) == ui.ScrollView:
		i = len(view_list)
		content_width = x(i)
		if content_width > parent_view.width:
			content_height = view_height
			size = (content_width,content_height)
			parent_view.content_size = size
		else:
			parent_view.content_size = parent_view.bounds
		
	#using the count of each item to determine it's place
	for count, view in enumerate(view_list):
		if auto_sizing is True:
			view.frame = (x(count), v_gap, view_width, view_height)
		else:
			view.x = x(i)



def vert(view_list = list(), dim = (50,50), gap = (0,4)):
	view_width, view_height = dim
	
	h_gap, v_gap = gap
	
	#vertical (y) displacement of each view
	y = lambda i: (view_height*i + v_gap*(i+1))
	
	#using the count of each item to determine it's place
	for i,view in enumerate(view_list):
		view.frame = (h_gap , y(i), view_width, view_height)

'''
If youre using the grid function directly make use of these kwargs:
	
	views_per_row = 3
		is the number of views allowed per row.
	
	parent_view = None
		is the view whoes subviews are being managed
		
	aspect_ratio = 1
		is the ratio of height/width of the view. which can be used in something like a gallery displaying photos.
'''
def grid(view_list = list(),parent_view = None, dim = (50,50), views_per_row = 
3,aspect_ratio = 1, gap = (4,4)):
	y_gap, x_gap = gap
	#if the parent view is included in the function it will automatically scale the
	#width and height in respect to the width of the parent view
	if parent_view is None:
		view_width, view_height = dim
	else:
		import math
		i = views_per_row
		view_width = math.floor(superview.width/i) - (i + 1) * gap
		view_height = view_width * aspect_ratio
		
	#these lambda functions are made to work with the enumeration of the view_list
	col = lambda i: i%views_per_row
	x = lambda i: col(i)*view_width + (col(i)+1) * x_gap
	
	row = lambda i: i // views_per_row
	y = lambda i: row(i) * view_height + (row(i) + 1) * y_gap
	
	if type(parent_view) is ui.ScrollView:
		i = len(view_list)
		content_size = (parent_view.width, y(i + 2))
		
		if parent_view.content_size == content_size:
			pass
		else:
			parent_view.content_size = content_size
	
	
	#this enumerates the view_list and places them in refrence to the count/index
	#of the view
	for count, view in enumerate(view_list):
		view.frame = (x(count),y(count),view_width,view_height)
	
'''
The View_Handler class is just a convinent way to organize the views within a parent view. without having to designate each

the parent_view and view list are 
'''
class View_Handler():
	
	def __init__(self, parent_view, view_list = None, stack_type = 'vert', size_reg = 'auto'):
		self.pv = parent_view
		self.ViewList = view_list
		
		self.size_reg = size_reg
		self.StackType = stack_type
	def change_layout_type(self, type):
		if self.type is not  type:
			self.type = type
		else:
			pass
	def layout(self):
		types = {
			'vert': self.place_views_vertically,
			'horiz':self.place_views_horizontally,
			'grid':self.place_views_in_grid
		}
		
		
	def get_view_list(self, views):
		#if no views are given it defaults to all the subviews in the handled view.
		if views and self.view_list is None:
			views = self.pv.subviews
		else:
			try:
				views = self.view_list
			except:
				views = views
		return views
		
	def place_views_vertically(self, views = None, dim = (50,50), gap = 4):
		views = self.get_view_list(views)
		vert(views, dim = dim, gap = gap)
		
	def place_views_horizontally(self, views = list(), dim = (50,50), gap = 4):
		views = self.get_view_list(views)
		horiz(views, dim = dim, gap = gap)
		
	def place_views_in_grid(self, views = None, dim = (50,50), gap = 4):
		views = self.get_view_list(views)
		grid(parent_view = self.pv,view_list = views)
