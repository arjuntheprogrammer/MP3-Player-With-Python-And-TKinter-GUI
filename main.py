from tkinter import *
from tkinter import filedialog
import os
import pygame

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

# Initialize Pygame
pygame.mixer.init()

# Create function to deal with the time
def play_time():
    pass

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
    song = playlist_box.get(ACTIVE)
    song = '%s/audios/%s.mp3'%(os.getcwd(), song)

    # Play song with pygame mixer
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    # Get Song Time
    play_time()

# Create Stop Function
def stop():
    pygame.mixer.music.stop()
    # Clear playlist bar
    playlist_box.select_clear(ACTIVE)

# Create function to play previous song
def back():
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



# Create Playlist Box
playlist_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
playlist_box.pack(pady=20)

# Define Button Images for controls
back_btn_image = PhotoImage(file='images/back50.png')
forward_btn_image = PhotoImage(file='images/forward50.png')
play_btn_image = PhotoImage(file='images/play50.png')
pause_btn_image = PhotoImage(file='images/pause50.png')
stop_btn_image = PhotoImage(file='images/stop50.png')

# Create Button Frame
control_frame = Frame(root)
control_frame.pack(pady=20)

# Create Play/Stop etc buttons
back_button = Button(control_frame, image=back_btn_image, command=back)
forward_button = Button(control_frame, image=forward_btn_image, command=forward)
play_button = Button(control_frame, image=play_btn_image, command=play)
pause_button = Button(control_frame, image=pause_btn_image, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_image, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)


# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create add song menu dropdows
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
status_bar = Label(root, text='nothing', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)



# Temporary Label
my_label = Label(root, text = '')
my_label.pack(pady=20)

root.mainloop()