from tkinter import *
from tkinter import ttk
from tkinter.font import *
import os
from tkinter.messagebox import *
from tkinter.filedialog import *
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from PIL import ImageTk, Image
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, USLT, TCOM, TCON, TDRC, TEXT, TRCK, TOPE, TXXX

# constant
TRACK_ID = 0
TITLE_ID = 1
ARTIST_ID = 2
ALBUM_ID = 3
YEAR_ID = 4
COMPOSER_ID = 5
LYRICIST_ID = 6
PERFORMER_ID = 7
BITRATE_ID = 8
LENGTH_ID = 9
DIR_ID = 10

TOTAL_HEAD = ["#", "Title", "Artist", "Album", "Year", "Composer", "Lyricist", "Performer", "Bitrate", "Length",
              "Directory"]
size_col = [150, 35, 200, 100, 150, 50, 100, 100, 100, 60, 60, 200]

TOTAL_ID = len(TOTAL_HEAD)

bool_list = ("", "=", ">", "<", ">=", "<=", "between")
valid_ext = ['.mp3', '.MP3', '.m4a', '.flac', '.FLAC']  # '.mp4', '.MP4',

# Init
list_dir = []
rev = [False] * (TOTAL_ID + 1)

def get_link():
	global local_dir, link_pic
	local_dir = os.getcwd()
	local_dir = local_dir.replace('\\', '/')
	link_pic = local_dir + "/pic/"

	f = open(local_dir+"/"+"music-directory.txt", 'r')
	global list_dir
	list_dir = []
	while True:
		line = f.readline()
		if line == '':
			break
		else:
			if line.find('\n') != -1:
				line = line[:len(line)-1]

			line = line.replace('\\', '/')
			if line != '':
				list_dir.append(line)

	f.close()


def search_song(event):
	tree.delete(*tree.get_children())
	for i in range(1, TOTAL_ID+1):
		tree.heading('#'+str(i), image=root_image)
		rev[i] = False

	overall_list = [x.lower() for x in overall_entry.get().split()]

	_title = song_entry.get()
	_artist = artist_entry.get()
	_composer = composer_entry.get()
	_lyricist = lyricist_entry.get()
	_performer = performer_entry.get()
	_album = album_entry.get()

	_bool_len = bool_len_chose.get()
	_len_num1 = len_num1.get()
	_len_num2 = len_num2.get()

	_bool_year = bool_year_chose.get()
	_year_num1 = year_num1.get()
	_year_num2 = year_num2.get()

	_bool_bitrate = bool_bitrate_chose.get()
	_bitrate_num1 = bitrate_num1.get()
	_bitrate_num2 = bitrate_num2.get()

	if _bool_len != '':
		if _bool_len == 'between' and _len_num1.isdigit() and _len_num2.isdigit():
			_len_num1 = int(_len_num1)
			_len_num2 = int(_len_num2)
			if _len_num1 > _len_num2:
				_len_num1, _len_num2 = _len_num2, _len_num1

		elif _bool_len != 'between' and _len_num1.isdigit():
			_len_num1 = int(_len_num1)
		else:
			showinfo("Error", "Invalid input!")
			return None

	if _bool_year != '':
		if _bool_year == 'between' and _year_num1.isdigit() and _year_num2.isdigit():
			_year_num1 = int(_year_num1)
			_year_num2 = int(_year_num2)
			if _year_num1 > _year_num2:
				_year_num1, _year_num2 = _year_num2, _year_num1

		elif _bool_year != 'between' and _year_num1.isdigit():
			_year_num1 = int(_year_num1)
		else:
			showinfo("Error", "Invalid input!")
			return None

	if _bool_bitrate != '':
		if _bool_bitrate == 'between' and _bitrate_num1.isdigit() and _bitrate_num2.isdigit():
			_bitrate_num1 = int(_bitrate_num1)
			_bitrate_num2 = int(_bitrate_num2)
			if _bitrate_num1 > _bitrate_num2:
				_bitrate_num1, _bitrate_num2 = _bitrate_num2, _bitrate_num1

		elif _bool_bitrate != 'between' and _bitrate_num1.isdigit():
			_bitrate_num1 = int(_bitrate_num1)
		else:
			showinfo("Error", "Invalid input!")
			return None

	# print(_title, _artist, _album, _bool_len, _len_num1, _len_num2, _bool_year, _year_num1, _year_num2)

	files_found = 0

	for _dir in list_dir:
		if os.path.isdir(_dir) is False:
			continue

		_dir.replace('\\', '/')
		for __dir in os.listdir(_dir):
			audio_info = [''] * TOTAL_ID
			audio_ext = os.path.splitext(__dir)[1]

			if os.path.isfile(os.path.join(_dir, __dir)) and audio_ext in valid_ext:
				if audio_ext == '.mp3' or audio_ext == '.MP3':
					audio = MP3(_dir + "/" + __dir)
				elif audio_ext == '.flac' or audio_ext == '.FLAC':
					audio = FLAC(_dir + "/" + __dir)

				audio_info[TRACK_ID] = '' if 'TRCK' not in audio else str(audio['TRCK'])  # track
				audio_info[TITLE_ID] = '' if 'TIT2' not in audio else str(audio['TIT2'])  # title
				audio_info[ARTIST_ID] = '' if 'TPE1' not in audio else str(audio['TPE1'])  # artist
				audio_info[ALBUM_ID] = '' if 'TALB' not in audio else str(audio['TALB'])  # album
				audio_info[YEAR_ID] = '' if 'TDRC' not in audio else str(audio['TDRC'])  # year
				audio_info[COMPOSER_ID] = '' if 'TCOM' not in audio else str(audio['TCOM'])  # composer
				audio_info[LYRICIST_ID] = '' if 'TEXT' not in audio else str(audio['TEXT'])  # lyricist
				audio_info[PERFORMER_ID] = '' if 'TXXX:PERFORMER' not in audio else str(audio['TXXX:PERFORMER'])  # performer
				audio_info[BITRATE_ID] = str(audio.info.bitrate)

				audio_len = str(audio.info.length)
				len_hour = int(audio_len[:audio_len.find('.')]) // 3600
				len_min = (int(audio_len[:audio_len.find('.')]) % 3600) // 60
				len_sec = int(audio_len[:audio_len.find('.')]) % 60
				audio_info[LENGTH_ID] = ('0' if len_hour < 10 else '') + str(len_hour) + ":" + \
				                        ('0' if len_min < 10 else '') + str(len_min) + ":" + \
				                        ('0' if len_sec < 10 else '') + str(len_sec)
				# + audio_len[audio_len.find('.'):]

				audio_info[DIR_ID] = _dir

				if _bool_len == 'between':
					len_satisfied = (_len_num1 <= len(audio_info[TITLE_ID]) <= _len_num2)
				elif _bool_len == '=':
					len_satisfied = (len(audio_info[TITLE_ID]) == _len_num1)
				elif _bool_len == '>':
					len_satisfied = (len(audio_info[TITLE_ID]) > _len_num1)
				elif _bool_len == '>=':
					len_satisfied = (len(audio_info[TITLE_ID]) >= _len_num1)
				elif _bool_len == '<':
					len_satisfied = (len(audio_info[TITLE_ID]) < _len_num1)
				elif _bool_len == '<=':
					len_satisfied = (len(audio_info[TITLE_ID]) <= _len_num1)
				else:
					len_satisfied = True

				if audio_info[YEAR_ID] == '':
					year_satisfied = (_bool_year == '')
				elif _bool_year == 'between':
					year_satisfied = (_year_num1 <= int(audio_info[YEAR_ID]) <= _year_num2)
				elif _bool_year == '=':
					year_satisfied = (int(audio_info[YEAR_ID]) == _year_num1)
				elif _bool_year == '>':
					year_satisfied = (int(audio_info[YEAR_ID]) > _year_num1)
				elif _bool_year == '>=':
					year_satisfied = (int(audio_info[YEAR_ID]) >= _year_num1)
				elif _bool_year == '<':
					year_satisfied = (int(audio_info[YEAR_ID]) < _year_num1)
				elif _bool_year == '<=':
					year_satisfied = (int(audio_info[YEAR_ID]) <= _year_num1)
				else:
					year_satisfied = True

				if _bool_bitrate == 'between':
					bitrate_satisfied = (_bitrate_num1 <= int(audio_info[BITRATE_ID]) <= _bitrate_num2)
				elif _bool_bitrate == '=':
					bitrate_satisfied = (int(audio_info[BITRATE_ID]) == _bitrate_num1)
				elif _bool_bitrate == '>':
					bitrate_satisfied = (int(audio_info[BITRATE_ID]) > _bitrate_num1)
				elif _bool_bitrate == '>=':
					bitrate_satisfied = (int(audio_info[BITRATE_ID]) >= _bitrate_num1)
				elif _bool_bitrate == '<':
					bitrate_satisfied = (int(audio_info[BITRATE_ID]) < _bitrate_num1)
				elif _bool_bitrate == '<=':
					bitrate_satisfied = (int(audio_info[BITRATE_ID]) <= _bitrate_num1)
				else:
					bitrate_satisfied = True

				overall_satisfied = True
				if len(overall_list) > 0:
					for item in overall_list:
						check_a_item = False
						for _id in range(TOTAL_ID):
							if audio_info[_id].lower().find(item) != -1:
								check_a_item = True
								break

						overall_satisfied = check_a_item
						if overall_satisfied is False:
							break

				if overall_satisfied:
					if _title == '' or (audio_info[TITLE_ID].lower()).find(_title.lower()) != -1:
						if _artist == '' or audio_info[ARTIST_ID].lower().find(_artist.lower()) != -1:
							if _composer == '' or audio_info[COMPOSER_ID].lower().find(_composer.lower()) != -1:
								if _lyricist == '' or audio_info[LYRICIST_ID].lower().find(_lyricist.lower()) != -1:
									if _performer == '' or audio_info[PERFORMER_ID].lower().find(_performer.lower()) != -1:
										if _album == '' or _album.lower() == str(audio_info[ALBUM_ID]).lower():
											if len_satisfied and year_satisfied and bitrate_satisfied:
												# tree.insert('', END, _dir, text=_dir, open=True)
												tree.insert('', END, text=__dir, values=audio_info)
												files_found += 1

	status.set(str(files_found) + " file" + ("" if files_found == 1 else "s") + " found.")


def called_len(event):
	global len_num1, len_num2

	if bool_len_chose.get() == 'between':
		len_num1_entry.grid()
		len_num2_entry.grid()
	elif bool_len_chose.get() != '':
		len_num1_entry.grid()
		len_num2_entry.grid_remove()
	else:
		len_num1_entry.grid_remove()
		len_num2_entry.grid_remove()

	len_num1.set('')
	len_num2.set('')


def called_year(event):
	global year_num1, year_num2

	if bool_year_chose.get() == 'between':
		year_num1_entry.grid()
		year_num2_entry.grid()
	elif bool_year_chose.get() != '':
		year_num1_entry.grid()
		year_num2_entry.grid_remove()
	else:
		year_num1_entry.grid_remove()
		year_num2_entry.grid_remove()

	year_num1.set('')
	year_num2.set('')


def called_bitrate(event):
	global bitrate_num1, bitrate_num2

	if bool_bitrate_chose.get() == 'between':
		bitrate_num1_entry.grid()
		bitrate_num2_entry.grid()
	elif bool_bitrate_chose.get() != '':
		bitrate_num1_entry.grid()
		bitrate_num2_entry.grid_remove()
	else:
		bitrate_num1_entry.grid_remove()
		bitrate_num2_entry.grid_remove()

	bitrate_num1.set('')
	bitrate_num2.set('')


def add_directory():
	global local_dir
	add_dir = askdirectory(title="Choose folder you want to search")
	list_dir.append(add_dir)

	f = open(local_dir + "/" + "music-directory.txt", 'a')
	f.write(add_dir+'\n')
	f.close()


def sort_column(col):
	if col == 0:
		return None
	else:
		_col = "#" + str(col)

	if len(tree.get_children()) == 0:
		return None

	if col == ALBUM_ID+1:
		col_list = [(tree.set(child, "#"+str(ALBUM_ID+1)), tree.set(child, "#"+str(TRACK_ID+1)), child)
		            for child in tree.get_children()]

		for i in range(len(col_list)):
			col_list[i] = (col_list[i][0], 0 if col_list[i][1] == '' else int(col_list[i][1]), col_list[i][2])

		# tuple: (album, track, child)
	elif col == YEAR_ID+1:
		col_list = [(tree.set(child, "#"+str(YEAR_ID+1)),
		             tree.set(child, "#"+str(ALBUM_ID+1)), tree.set(child, "#"+str(TRACK_ID+1)), child)
		            for child in tree.get_children()]

		for i in range(len(col_list)):
			col_list[i] = (0 if col_list[i][0] == '' else int(col_list[i][0]),
			               col_list[i][1], 0 if col_list[i][2] == '' else int(col_list[i][2]), col_list[i][3])

		# tuple: (year, album, track, child)
	else:
		col_list = [(tree.set(child, _col), child) for child in tree.get_children()]  # tuple: (#_col.val, child)

	col_list.sort(key=lambda t: t, reverse=rev[col])

	for i in range(1, TOTAL_ID+1):
		if '#'+str(i) != _col:
			tree.heading('#'+str(i), image=root_image)
			rev[i] = False
		else:
			tree.heading('#'+str(i), image=down_image if rev[i] else up_image)
			rev[i] = not rev[i]

	for index, tup in enumerate(col_list):  # enumerate: list of tuple (index, (..., child))
		tree.move(tup[len(tup)-1], '', index)


def play_music(*args):
	for item in args:
		filename = tree.item(item)['values'][TOTAL_ID-1] + "/" + tree.item(item)['text']
		os.startfile(filename)


def select_idx(event, idx):
	if len(tree.get_children()) == 0:
		return None

	tree.selection_set(tree.get_children()[idx])


def on_right_click(event):
	region = tree.identify("region", event.x, event.y)

	global right_row, right_col
	right_row = None
	right_col = None

	if region == "tree":
		right_row = tree.identify_row(event.y)

	elif region == "cell":
		right_col = tree.identify_column(event.x)
		right_row = tree.identify_row(event.y)

	else:
		# if region == "heading"
		return None

	if right_row in tree.selection():
		rightmenu.entryconfig(0, state=NORMAL)
	else:
		for item in tree.selection():
			tree.selection_remove(item)

		rightmenu.entryconfig(0, state=DISABLED)

	rightmenu.post(event.x_root, event.y_root)


def Edit():  # just edit info of a file, not multiple files
	edit_id = [TITLE_ID, ARTIST_ID, ALBUM_ID, YEAR_ID, TRACK_ID, COMPOSER_ID, LYRICIST_ID, PERFORMER_ID]
	edit_label_list = [None] * len(edit_id)
	edit_entry_list = [None] * len(edit_id)

	def ok_pressed():
		try:
			tags = ID3(_dir + "/" + __dir)
		except:
			print("Adding ID3 header;")
			tags = ID3()

		tags['TRCK'] = TRCK(encoding=3, text=edit_entry_list[TRACK_ID].get())
		tags['TIT2'] = TIT2(encoding=3, text=edit_entry_list[TITLE_ID].get())
		tags['TPE1'] = TPE1(encoding=3, text=edit_entry_list[ARTIST_ID].get())
		tags['TALB'] = TALB(encoding=3, text=edit_entry_list[ALBUM_ID].get())
		tags['TDRC'] = TDRC(encoding=3, text=edit_entry_list[YEAR_ID].get())
		tags['TCOM'] = TCOM(encoding=3, text=edit_entry_list[COMPOSER_ID].get())
		tags['TEXT'] = TEXT(encoding=3, text=edit_entry_list[LYRICIST_ID].get())
		tags['TXXX:PERFORMER'] = TXXX(encoding=3, desc='PERFORMER', text=edit_entry_list[PERFORMER_ID].get())

		try:
			tags.save(_dir + "/" + __dir)
		except:
			print("denied")

		new_val = list(tree.item(right_row)['values'])
		for in_id in edit_id:
			if new_val[in_id] != edit_entry_list[in_id].get():
				new_val[in_id] = edit_entry_list[in_id].get()

		tree.item(right_row, values=new_val)

		win.destroy()

	# Info
	global right_row, right_col

	_dir = tree.item(right_row)['values'][DIR_ID]
	__dir = tree.item(right_row)['text']
	# print(tree.selection())
	old_info = list(tree.item(right_row)['values'])
	# print(right_row, old_info)

	# window
	win = Toplevel()
	win.wm_title("Edit")

	win_canvas = Canvas(win, bd=0, highlightthickness=0,
	                    scrollregion=(0, 0, win.winfo_screenwidth(), win.winfo_screenheight()))
	win_canvas.grid(row=0, column=0, sticky='nsew')

	'''
	hscr = Scrollbar(win, orient='horizontal', command=win_canvas.xview)
	hscr.grid(row=1, column=0, sticky='ew')
	vscr = Scrollbar(win, orient='vertical', command=win_canvas.yview)
	vscr.grid(row=0, column=1, sticky='ns')
	win_canvas.configure(xscrollcommand=hscr.set, yscrollcommand=vscr.set)
	'''

	filename_label = Label(win_canvas, text="Filename")
	filename_label.grid(row=0, column=0, sticky='w')
	filename_entry = Entry(win_canvas)
	filename_entry.grid(row=0, column=1, columnspan=2, sticky='ew')
	filename_entry.insert(END, __dir)
	filename_entry.config(state='readonly')

	dir_label = Label(win_canvas, text="Directory")
	dir_label.grid(row=1, column=0, sticky='w')
	dir_entry = Entry(win_canvas)
	dir_entry.grid(row=1, column=1, columnspan=2, sticky='ew')
	dir_entry.insert(END, _dir)
	dir_entry.config(state='readonly')

	for i in range(len(edit_id)):
		# 0: _label, 1: _entry
		_id = edit_id[i]
		# print(_id, old_info[_id])
		edit_label_list[_id] = Label(win_canvas, text=TOTAL_HEAD[_id])
		edit_label_list[_id].grid(row=i+2, column=0, sticky='w')
		edit_entry_list[_id] = Entry(win_canvas, relief=GROOVE)
		edit_entry_list[_id].grid(row=i+2, column=1)
		edit_entry_list[_id].delete(0, END)
		edit_entry_list[_id].insert(END, old_info[_id])

	btn_ok = Button(win, text="OK", command=ok_pressed)
	btn_ok.grid(row=2, column=0, columnspan=2)

	win.mainloop()


root = Tk()
root.wm_title("Search music tool")

# default_font = nametofont("TkDefaultFont")
# default_font.configure(size=10)
# root.option_add("*Font", default_font)

root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

get_link()

# search frame
search_frame = Frame(root)
search_frame.grid(row=0, column=0, sticky='w', columnspan=2)

overall_label = Label(search_frame, text="Overall search: ")
overall_label.grid(row=0, column=0, sticky='w')
overall_entry = Entry(search_frame, text='')
overall_entry.grid(row=0, column=1, columnspan=2, sticky='ew')

song_label = Label(search_frame, text="Song (contains): ")
song_label.grid(row=1, column=0, sticky='w')
song_entry = Entry(search_frame, text='')
song_entry.grid(row=1, column=1, sticky='w')

song_len_label = Label(search_frame, text="Length of song name: ")
song_len_label.grid(row=1, column=2, sticky='w')

bool_len_chose = StringVar()
bool_len_chose.set('')
song_len_entry = ttk.Combobox(search_frame, width=10, values=bool_list, state='readonly', textvariable=bool_len_chose)
song_len_entry.bind("<<ComboboxSelected>>", called_len)
song_len_entry.grid(row=1, column=3, sticky='w')

len_num1 = StringVar()
len_num1.set('')
len_num1_entry = Entry(search_frame, width=10, textvariable=len_num1)
len_num1_entry.grid(row=1, column=4, sticky='w')
len_num1_entry.grid_remove()

len_num2 = StringVar()
len_num2.set('')
len_num2_entry = Entry(search_frame, width=10, textvariable=len_num2)
len_num2_entry.grid(row=1, column=5, sticky='w')
len_num2_entry.grid_remove()

artist_label = Label(search_frame, text="Artist: ")
artist_label.grid(row=3, column=0, sticky='w')
artist_entry = Entry(search_frame, text='')
artist_entry.grid(row=3, column=1, sticky='w')

composer_label = Label(search_frame, text="Composer: ")
composer_label.grid(row=3, column=2, sticky='w')
composer_entry = Entry(search_frame, text='')
composer_entry.grid(row=3, column=3, sticky='w')

lyricist_label = Label(search_frame, text="Lyricist: ")
lyricist_label.grid(row=3, column=4, sticky='w')
lyricist_entry = Entry(search_frame, text='')
lyricist_entry.grid(row=3, column=5, sticky='w')

performer_label = Label(search_frame, text="Performer: ")
performer_label.grid(row=3, column=6, sticky='w')
performer_entry = Entry(search_frame, text='')
performer_entry.grid(row=3, column=7, sticky='w')

album_label = Label(search_frame, text="Album: ")
album_label.grid(row=4, column=0, sticky='w')
album_entry = Entry(search_frame, text='')
album_entry.grid(row=4, column=1, sticky='w')

year_label = Label(search_frame, text="Year: ")
year_label.grid(row=4, column=2, sticky='w')
bool_year_chose = StringVar()
bool_year_chose.set('')
year_entry = ttk.Combobox(search_frame, width=10, values=bool_list, state='readonly', textvariable=bool_year_chose)
year_entry.bind("<<ComboboxSelected>>", called_year)
year_entry.grid(row=4, column=3, sticky='w')

year_num1 = StringVar()
year_num1.set('')
year_num1_entry = Entry(search_frame, width=10, textvariable=year_num1)
year_num1_entry.grid(row=4, column=4, sticky='w')
year_num1_entry.grid_remove()

year_num2 = StringVar()
year_num2.set('')
year_num2_entry = Entry(search_frame, width=10, textvariable=year_num2)
year_num2_entry.grid(row=4, column=5, sticky='w')
year_num2_entry.grid_remove()

bitrate_label = Label(search_frame, text="Bitrate: ")
bitrate_label.grid(row=5, column=2, sticky='w')
bool_bitrate_chose = StringVar()
bool_bitrate_chose.set('')
bitrate_entry = ttk.Combobox(search_frame, width=10, values=bool_list, state='readonly', textvariable=bool_bitrate_chose)
bitrate_entry.bind("<<ComboboxSelected>>", called_bitrate)
bitrate_entry.grid(row=5, column=3, sticky='w')

bitrate_num1 = StringVar()
bitrate_num1.set('')
bitrate_num1_entry = Entry(search_frame, width=10, textvariable=bitrate_num1)
bitrate_num1_entry.grid(row=5, column=4, sticky='w')
bitrate_num1_entry.grid_remove()

bitrate_num2 = StringVar()
bitrate_num2.set('')
bitrate_num2_entry = Entry(search_frame, width=10, textvariable=bitrate_num2)
bitrate_num2_entry.grid(row=5, column=5, sticky='w')
bitrate_num2_entry.grid_remove()


# Image
root_image = ImageTk.PhotoImage(Image.open(link_pic + "normal_small.png"))
up_image = ImageTk.PhotoImage(Image.open(link_pic + "up_small.png"))
down_image = ImageTk.PhotoImage(Image.open(link_pic + "down_small.png"))
search_image = ImageTk.PhotoImage(Image.open(link_pic + "search.png"))

# treeview
canvas = Canvas(root, bd=0, highlightthickness=0,
                scrollregion=(0, 0, root.winfo_screenwidth(), root.winfo_screenheight()))
canvas.grid(row=2, column=0, sticky='nsew')

tree = ttk.Treeview(canvas, height=20, selectmode='extended', show="tree headings")
tree.pack(expand=True, fill='both')

hScroll = Scrollbar(root, orient='horizontal', command=tree.xview)
hScroll.grid(row=3, column=0, sticky='ew')
vScroll = Scrollbar(root, orient='vertical', command=tree.yview)
vScroll.grid(row=2, column=1, sticky='ns')
tree.configure(xscrollcommand=hScroll.set, yscrollcommand=vScroll.set)

tree["columns"] = TOTAL_HEAD

for i in range(TOTAL_ID+1):
	tree.heading("#"+str(i), text="Filename" if i == 0 else TOTAL_HEAD[i-1], image=root_image,
	             command=lambda col=i: sort_column(col))
	tree.column("#"+str(i), width=size_col[i], stretch=False)

# button frame
btn_frame = Frame(root)
btn_frame.grid(row=1, column=0, sticky='w', columnspan=2)

btn_add_dir = Button(btn_frame, text="Add directory...", relief=GROOVE, command=add_directory)
btn_add_dir.pack(side=LEFT)

btn_search = Button(btn_frame, image=search_image, text="Search", relief=GROOVE,
                    command=lambda event=None: search_song(event))
btn_search.pack(side=LEFT)

btn_play_all = Button(btn_frame, text="Play all", relief=GROOVE,
                      command=lambda: play_music(*tree.get_children()))
btn_play_all.pack(side=LEFT)

btn_play_selected = Button(btn_frame, text="Play selected", relief=GROOVE,
                           command=lambda: play_music(*tree.selection()))
btn_play_selected.pack(side=LEFT)

root.bind("<Return>", search_song)
tree.bind("<Home>", lambda event, idx=0: select_idx(event, idx))
tree.bind("<End>", lambda event, idx=-1: select_idx(event, idx))
tree.bind("<Control-Shift-Home>", lambda event, key="Home": select_key(event, key))
tree.bind("<Control-Shift-End>", lambda event, key="End": select_key(event, key))
root.bind("<Control-a>", lambda event, key="All": select_key(event, key))
tree.bind('<Button-3>', on_right_click)

# Right-click menu
rightmenu = Menu(root, tearoff=0)
rightmenu.add_command(label="Edit...", command=Edit)

# Status bar
status = StringVar()
status.set("Status bar.")

status_bar = Label(root, relief=FLAT, anchor='w', bd=3, textvariable=status)
status_bar.grid(row=6, column=0, sticky='ew', columnspan=2)

root.mainloop()
