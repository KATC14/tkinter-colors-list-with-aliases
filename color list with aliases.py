import tkinter
from custom import color_tools
from tkinter.ttk import *

# found it here '/Python310/Tools/pynche' part of pyColorChooser.py
# then modified it to work stand alone

class ListViewer:
	def __init__(self):
		self.lastbox = None
		self.dontcenter = 0
		# GUI
		root = tkinter.Tk()
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		root.title('Pynche Color List')
		root.iconname('Pynche Color List')
		#
		# create the canvas which holds everything, and its scrollbar
		#
		self.canvas = tkinter.Text(root, state='normal', width=38, height=40, wrap='word')

		self.canvas = tkinter.Canvas(root, width=160, height=300, borderwidth=2, relief='sunken')
		self.canvas.bind('<MouseWheel>', self.scroll)
		scrollbar = Scrollbar(root, command=self.canvas.yview)
		self.canvas.config(yscrollcommand=scrollbar.set)

		scrollbar.grid(sticky='NS', column=1, row=0)
		self.canvas.grid(sticky='NSEW', column=0, row=0)
		self.populate()

		# alias list
		self.alabel = Label(root, text='Aliases:')
		self.alabel.grid(column=0, row=1)
		self.aliases = tkinter.Listbox(root, height=5, selectmode='browse', state='disabled')
		self.aliases.grid(sticky='NSEW', column=0, row=2)
		root.mainloop()
	def scroll(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/20)), "units")

	def populate(self):
		#
		# create all the buttons
		row = 0
		widest = 0
		bboxes = self.__bboxes = []
		for name in color_tools.tkcolors.unique_names():
			exactcolor = color_tools.tkcolors.allcolors()[name]
			self.canvas.create_rectangle(5, row*20 + 5, 20, row*20 + 20, fill=exactcolor)
			textid = self.canvas.create_text(25, row*20 + 13,text=name,anchor='w')
			x1, y1, textend, y2 = self.canvas.bbox(textid)
			boxid = self.canvas.create_rectangle(3, row*20+3,textend+3, row*20 + 23,outline='',tags=(name, exactcolor, 'all'))
			self.canvas.bind('<ButtonRelease>', self.onrelease)
			bboxes.append(boxid)
			if textend+3 > widest:
				widest = textend+3
			row += 1
		canvheight = (row-1)*20 + 25
		self.canvas.config(scrollregion=(0, 0, 150, canvheight))
		for box in bboxes:
			x1, y1, x2, y2 = self.canvas.coords(box)
			self.canvas.coords(box, x1, y1, widest, y2)

	def onrelease(self, event=None):
		# find the current box
		x = self.canvas.canvasx(event.x)
		y = self.canvas.canvasy(event.y)
		ids = self.canvas.find_overlapping(x, y, x, y)
		for boxid in ids:
			if boxid in self.__bboxes:
				break
		else:
			##print('No box found!')
			return
		tags = self.canvas.gettags(boxid)
		taglist = []
		for t in tags:
			taglist.append(t)
			if t[0] == '#':
				break
		else:
			##print('No color tag found!')
			return
		self.dontcenter = 1
		self.update_yourself(taglist)

	def update_yourself(self, t):#red, green, blue
		# turn off the last box
		if self.lastbox:
			self.canvas.itemconfigure(self.lastbox, outline='')
		# turn on the current box
		self.canvas.itemconfigure(t[1], outline='black')
		self.lastbox = t[1]
		# fill the aliases
		self.aliases.config(state='normal')
		self.aliases.delete(0, 'end')
		#self.aliases.insert('end', '<no aliases>')
		try:
			unaliased = color_tools.tkcolors.allcolors()
			aliased = {}
			for i, x in unaliased.items():
				try:
					aliased[x].append(i)
				except:
					aliased.update({x:[i]})
		except:
			pass

		#t is (#hxcolr, name)
		a = aliased[t[1]]
		a.remove(t[0])#removes its own name so if list has length of 1 its own name is removed meaning it has no aliases
		print(t[1])
		if not a:#if list is empty there is no aliases
			self.aliases.insert('end', '<no aliases>')
		else:
			for i in a:#if list is not empty loop what is there
				self.aliases.insert('end', i)
		self.aliases.config(state='disabled')

		# maybe scroll the canvas so that the item is visible
		if self.dontcenter:
			self.dontcenter = 0
		else:
			ig, ig, ig, y1 = self.canvas.coords(t[1])
			ig, ig, ig, y2 = self.canvas.coords(self.__bboxes[-1])
			h = int(self.canvas['height']) * 0.5
			self.canvas.yview('moveto', (y1-h) / y2)

if __name__ == "__main__":
	ListViewer()
