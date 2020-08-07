from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import pygame
import time
from mutagen.mp3 import MP3

root = Tk()

root.title("MP3 Player")
root.geometry("700x500")

# Initialize Pygame
pygame.mixer.init()

# Create function to deal with the time
def play_time():
    # Check to see if the song is stopped
    if stopped:
        return

    # Gran current song time
    current_time = pygame.mixer.music.get_pos() / 1000
    # Convert song time to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = playlist_box.get(ACTIVE)
    # Add directory structure to the song
    song = '%s/audios/%s.mp3'%(os.getcwd(), song)

    # Find Current Song Length
    song_mut = MP3(song)
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    song_slider.config(to=song_length)

    # Check to see if song is over
    if int(song_slider.get()) == int(song_length):
        stop()

    elif paused:
        # Check to see if paused, if so - end
       pass

    else:
        # Move slider along 1 second at a time
        next_time = int(song_slider.get()) + 1
        # Output new time value to slider, and to length of song
        song_slider.config(to=song_length, value=next_time)

    # Convert slider position to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))

    # Output Slider
    status_bar.config(text='Time Elapsed: %s of %s'%(converted_current_time, converted_song_length))

    # Add converted time to status bar
    if current_time >= 0:
        status_bar.config(text='Time Elapsed: %s of %s'%(converted_current_time, converted_song_length))

    # Create loop to check the time every second
    status_bar.after(1000, play_time)

# Add one song tp playlist
def add_song():
    song = filedialog.askopenfilename(initialdir="audios/", title="Choose a song", filetypes = (("mp3 files", "*.mp3"), ))

    # Strip out directory from mp3 file
    song = os.path.basename(song).split('.')[0]
    playlist_box.insert(END, song)

# Add many songs tp playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="audios/", title="Choose songs", filetypes = (("mp3 files", "*.mp3"), ))

    for song in songs:
        # Strip out directory from mp3 file
        song = os.path.basename(song).split('.')[0]
        playlist_box.insert(END, song)

# Delete a song from playlist
def delete_song():
    # Delete highlighted song from playlist
    playlist_box.delete(ANCHOR)

# Delete all songs from playlist
def delete_all_songs():
    playlist_box.delete(0, END)


# Create play function
def play():

    # Set stopped to false
    global stopped
    stopped = False

    song = playlist_box.get(ACTIVE)
    song = '%s/audios/%s.mp3'%(os.getcwd(), song)

    # Play song with pygame mixer
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Get Song Time
    play_time()

# Create stopped variable
global stopped
stopped = False

# Create Stop Function
def stop():
    pygame.mixer.music.stop()
    # Clear playlist bar
    playlist_box.select_clear(ACTIVE)
    status_bar.config(text='')

    # Set our slider to zero
    song_slider.config(value=0)

    # Set stop variable to True
    global stopped
    stopped=True

# Create function to play previous song
def back():
    # Reset slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)

    # get current song number
    next_one = playlist_box.curselection()
    #  Add one to current number
    next_one = next_one[0] - 1

    # Grab the song title from the playlist
    song = playlist_box.get(next_one)

    # Add directory structure to the song
    song = '%s/audios/%s.mp3'%(os.getcwd(), song)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bat in playlist
    playlist_box.selection_clear(0, END)

    # Move active bar to next song
    playlist_box.activate(next_one)

    # Set active bar to next sog
    playlist_box.selection_set(next_one, last=None)

# Create Next song function
def forward():
    # Reset slider position and status bar
    status_bar.config(text='')
    song_slider.config(value=0)

    # get current song number
    next_one = playlist_box.curselection()
    #  Add one to current number
    next_one = next_one[0] + 1

    # Grab the song title from the playlist
    song = playlist_box.get(next_one)

    # Add directory structure to the song
    song = '%s/audios/%s.mp3'%(os.getcwd(), song)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Clear active bat in playlist
    playlist_box.selection_clear(0, END)

    # Move active bar to next song
    playlist_box.activate(next_one)

    # Set active bar to next sog
    playlist_box.selection_set(next_one, last=None)


# Create Paused variable
global paused
paused = False

# Create Pause Function
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False

    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True

#Create Volume Function
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())

# Create a Slide Function For Song Positioning
def slide(x):
    # Reconstruct song with directory
    song = playlist_box.get(ACTIVE)
    song = '%s/audios/%s.mp3'%(os.getcwd(), song)

    #Load song with pygame mixer
    pygame.mixer.music.load(song)
    #Play song with pygame mixer
    pygame.mixer.music.play(loops=0, start=song_slider.get())


# Create main Frame
main_frame = Frame(root)
main_frame.pack(pady=20)

# Create Playlist Box
playlist_box = Listbox(main_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.grid(row=0, column=0)

# Create Volume Slider Frame
volume_frame = LabelFrame(main_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=30)

# Create Volume Slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, length=125, value=1, command=volume)
volume_slider.pack(pady=10)

# Create Song Slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=2, column=0, pady=20)


# Define Button Images for controls
back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')


# Create Button Frame
control_frame = Frame(main_frame)
control_frame.grid(row=1, column=0, pady=20)

# Create Play/Stop etc buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=back)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=forward)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Main Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create add song menu dropdowns
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
# Add one song tp playlist
add_song_menu.add_command(label="Add one song to playlist", command=add_song)

# Add many songs tp playlist
add_song_menu.add_command(label="Add many songs to playlist", command=add_many_songs)

# Create delete song menu dropdowns
remove_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all songs from playlist", command=delete_all_songs)

# Create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


# Temporary Label
my_label = Label(root, text = '')
my_label.pack(pady=20)




root.mainloop()