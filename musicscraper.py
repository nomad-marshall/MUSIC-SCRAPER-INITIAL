import vlc
import pafy
import tkinter as tk  # noqa: F401
import customtkinter
from youtubesearch import search_youtube
import os
import yt_dlp as ydl  # noqa: F401
import time  # noqa: F401

#test
class BaseMusicApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1024x700")
        self.root.title("Music Scraper")        
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        

class UITemplate(BaseMusicApp):
    def __init__(self, root):
        super().__init__(root)
        self.setupui(root)

    def setupui(self, root): 
        self.funny_font = customtkinter.CTkFont(
        family="Comic Sans MS", # haha
        size=30,
        weight="bold",  
        )
        
        
class SearchBar(UITemplate):
    def __init__(self, root, search_results_obj):
        super().__init__(root)
        self.search_results_obj = search_results_obj
        self.create_search_bar()
        
    def create_results_area(self):
        self.results_frame = customtkinter.CTkFrame(self.main_frame)
        self.results_frame.pack(fill="both", expand=True, pady=10)
        
    def create_search_bar(self):
        self.search_bar = customtkinter.CTkEntry(
            master=self.root,
            placeholder_text = "Type your search here",
            width=350,
            height=50,
            font=self.funny_font
        )
        self.search_bar.pack(pady=20)
        search_button =customtkinter.CTkButton(
            master=self.root,
            text="Search",
            command=self.perform_search,
            font=self.funny_font
        )
        search_button.pack(pady=10)
    def perform_search(self):
        query=self.search_bar.get()
        if query:
            results = search_youtube(query)
            self.search_results_obj.display_results(results)
        else:
            print("No search query entered.")

class SearchResults(UITemplate):
    def __init__(self, root, media_player):
        super().__init__(root)
        self.selected_media = None
        self.media_player = media_player
        self.create_results_area()
        
    def create_results_area(self):
        self.results_frame = customtkinter.CTkFrame(master=self.root)
        self.results_frame.pack(pady=10, fill="both", expand=True)
    
    def display_results(self, results):
        for widget in self.results_frame.winfo_children():
            widget.destroy() #clears results
        if results:
            for result in results:
                title = result["snippet"]["title"]
                video_id = result["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                result_button = customtkinter.CTkButton(
                    master=self.results_frame,
                    text=title,
                    command=lambda url=video_url: self.select_media(url)
                )
                result_button.pack(pady=5)
        else:
            no_results_label = customtkinter.CTkLabel(
                master=self.results_frame,
                text="No results found.",
            )
            no_results_label.pack(pady=10)
    def select_media(self, media_url):
        print(f"Playing: {media_url}")
        self.selected_media = media_url
        self.media_player.set_selected_media(media_url)

class DropdownOption(UITemplate): #this isnt working atm, need to figure out later
    def __init__(self, root):
        super().__init__(root)
        self.create_option_menu()
        
    def optionmenu_callback(self, choice):  
        print("optionmenu dropdown clicked:", choice)
        
    def create_option_menu(self):
        optionmenu_var = customtkinter.StringVar(value="Select your platform")
        #optionbox_frame = customtkinter.CTkFrame(master=self.root) #new #restructure to frame in grid?
        #optionbox_frame.pack(pady=20) #new
        optionbox = customtkinter.CTkOptionMenu(
            master=self.root,
            values=["Youtube", "Spotify", "Soundcloud"],
            command=self.optionmenu_callback,
            variable=optionmenu_var,)
        optionbox.grid(row=0, column=0, padx=10) #new
    #considering remaking this part to align with grid
    #or shoving it in media buttons
    #much to think about

class VolumeSlider(UITemplate):
    def __init__(self, root, media_player):
        super().__init__(root)
        self.media_player = media_player
        self.create_slider()

    def create_slider(self):
        slider = customtkinter.CTkSlider(
            master=self.root,
            from_=0,
            to=100,
            command=self.slider_event,
            orientation="vertical",)
        slider.pack(padx=0.9, pady=0.5, side="right")
        
    def slider_event(self, value):
        print("Slider value:", value)
        self.media_player.set_volume(int(value)) #should set volume of app
        
class MediaButtons(UITemplate): #to control playing of media
    def __init__(self, root, media_player):
        super().__init__(root)
        self.create_media_buttons()
        self.media_player = media_player
        
    def create_media_buttons(self):
        button_frame = customtkinter.CTkFrame(master=self.root)
        button_frame.pack(pady=20)
        buttons = {
            "Play Audio (MP3)": lambda: self.play_media(), #triggers selfplaymedia via lambda
            "Pause": self.pause_media,
            "Play/Resume": self.play_media,
            "Rewind 10 secs": self.rewind_media,
            "Forward 10 secs": self.forward_media,
            #"Platform": self.option_menu,
            #add a button for uhh
            #option dropdown menu
        } #creates buttons
        for col, (text, command) in enumerate(buttons.items()):
            button = customtkinter.CTkButton(
                master=button_frame,
                text=text,
                command=command #assigns command to buttons
            )
            button.grid(row=0, column=col, padx=10)
            
    def play_media(self): #button functions
        print("Playing audio!")
        self.media_player.play_media()
        
    def pause_media(self):
        print("Pause button clicked!")
        self.media_player.pause_media()
#def stop_media(self): #stop and flush maybe?
#print("Stop button clicked!") #come back to this later
    def rewind_media(self):
        print("Rewind button clicked!")
        self.media_player.rewind_media()
        
    def forward_media(self):
        print("Forward button clicked!")
        self.media_player.forward_media()
        
    def skip_media(self):
        print("Skip button clicked!")
        self.media_player.skip_media()
    #def create_option_menu(self):
    #    print("Platform selected:")
    #    pass

class MediaPlayer(): #to focus on streaming of content
    def __init__(self, root, now_playing):
        self.root=root
        vlc_lib_path=r"C:\Program Files\VideoLAN\VLC"
        os.environ["VLC_PLUGIN_PATH"] = vlc_lib_path
        self.instance = vlc.Instance("--no-video")
        self.player = self.instance.media_player_new()
        self.now_playing = now_playing
        self.current_media = None
        self.selected_media = None
        self.is_playing = False #tracks if its playing
        self.past_position = 0 #position in song

    def set_selected_media(self, media_url):
        self.selected_media = media_url
        self.is_playing = False
        self.last_position = 0
        self.play_media()
      
    def play_media(self, media_type="audio"):
        if not self.selected_media:
            print("No media selected!")
            return
        try:
            print(f"Attempting to play: {self.selected_media}")
            if not self.is_playing:
                if "youtube.com" in self.selected_media:
                    ydl_opts = {
                        'format': 'bestaudio/best', 
                        'quiet': True,  #this stops unnecessary terminal output
                    }
                    with ydl.YoutubeDL(ydl_opts) as ydl_instance:
                        info_dict = ydl_instance.extract_info(self.selected_media, download=False)
                        audio_url = info_dict["url"]
                        title = info_dict.get("title", "unknown title")
                        self.now_playing.update_now_playing(title)
                    
                    media = self.instance.media_new(audio_url) #heres vlc again doing its thing
                    self.player.set_media(media)
                    self.player.play()
                    print(f"Playing {media_type} from YouTube: {self.selected_media}")
                    self.is_playing = True
                else:
                    #fall back to pafy 
                    video = pafy.new(self.selected_media)
                    title = video.title
                    self.now_playing.update_now_playing(title) #updates now playing title
                    best = video.getbest()
                    media = vlc.MediaPlayer(best.url)
                    media.play()
                    print(f"Playing {media_type} with URL: {self.selected_media}")
                    self.is_playing = True
            else: #pause function tracking position in song
                current_time = self.player.get_time()
                self.player.pause()
                self.last_position = current_time
        except Exception as e:
            print(f"Error playing media: {e}")
        
    def set_volume(self, volume):
        try:
            self.player.audio_set_volume(volume)
            print(f"Volume set to: {volume}")
        except Exception as e:
            print(f"Error setting volume: {e}")
        
    def pause_media(self):
        if self.player.is_playing():
            self.player.pause()
    def skip_media(self):
        if self.player.is_playing():
            self.player.skip()
    def rewind_media(self):
        if self.player.is_playing():
            current_time = self.player.get_time()
            new_time = max(0, current_time - 10000) #rewind by 10 secs
            self.player.set_time(new_time)
    def forward_media(self):
        if self.player.is_playing():
            current_time = self.player.get_time()
            new_time = max(0, current_time + 10000) #ff increment of 10
            self.player.set_time(new_time)
    def option_menu(self):
        pass
        
class NowPlaying(UITemplate):
    def __init__(self, root):
        super().__init__(root)
        self.create_now_playing()
    def create_now_playing(self):
        self.now_playing_label = customtkinter.CTkLabel(
            master=self.root,
            text=("Now Playing: None")
        ) #configure this to show current track
        self.now_playing_label.pack(pady=10)
    def update_now_playing(self, title):
        self.now_playing_label.configure(text=f"Now Playing: {title}")
        
      
root = customtkinter.CTk()
now_playing = NowPlaying(root)
media_player = MediaPlayer(root, now_playing)
media_buttons = MediaButtons(root, media_player)
volume_slider = VolumeSlider(root, media_player)
#dropdown = DropdownOption(root) #new
search_results = SearchResults(root, media_player)
search_bar = SearchBar(root, search_results)

root.mainloop()