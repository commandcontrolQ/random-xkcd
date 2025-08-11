# xkcd random parser
import ctypes, re, html, os, io
from html.parser import HTMLParser
from urllib.request import urlopen, urlretrieve

# Create message box using built-in function
# Windows-exclusive, tkinter.messagebox would be more inclusive
msg = lambda title, text, style=0: ctypes.windll.user32.MessageBoxW(0, text, title, style)


# Check if user has every non-default module
try:
    import requests
except ModuleNotFoundError:
    msg("Missing module!", "Error during initialisation: The 'requests' module is not installed!")
    exit(-1)

try:
    import tkinter
    from tkinter import font as tkfont
except ModuleNotFoundError:
    msg("Missing module!", "Error during initialisation: Tkinter is either not installed or not configured!")
    exit(-1)

try:
    from PIL import ImageTk, Image
except ModuleNotFoundError:
    msg("Missing module!", "Error during initialisation: The 'pillow' module is not installed!")
    
    
def show_comic(i, title, src, text):
    root = tkinter.Tk()
    root.title(f"xkcd - {i}")
    root.resizable(False, False) # Prevent window from being resized

    # Download favicon to temp folder and replace default Tk icon
    # 'TEMP' env var is Windows-exclusive, force /tmp on Darwin & Linux?
    # https://stackoverflow.com/a/33139792
    # https://stackoverflow.com/a/22776
    TEMP_ICON_PATH = f"{os.environ.get('TEMP')}\\xkcd.ico"
    urlretrieve("https://xkcd.com/s/919f27.ico", TEMP_ICON_PATH)
    root.iconbitmap(TEMP_ICON_PATH)

    # Create a new "largefont" for the title
    # Use TkDefaultFont to avoid hardcoding a font
    largefont = tkfont.nametofont("TkDefaultFont").actual()
    largefont["size"] = largefont["size"] + 3

    # https://stackoverflow.com/a/65638774
    # Class for creating PhotoImage from URL
    class WebImage:
        def __init__(self, url):
            with urlopen(url) as u:
                imgdata = u.read()
            img = Image.open(io.BytesIO(imgdata))
            self.image = ImageTk.PhotoImage(img)
        def get(self):
            return self.image
    img = WebImage(src).get()

    label_title = tkinter.Label(root, text=title, justify="center", font=largefont)
    label_title.pack()

    label_img = tkinter.Label(root, image=img, justify="center")
    label_img.pack()

    label_text = tkinter.Label(root, text=text, justify="center", wraplength=img.width())
    label_text.pack()

    # root.attributes('-topmost',True)
    root.mainloop()

# ChatGPT
# Take HTML tag and convert to dictionary of attributes
def tag2dict(tag_str):
    class TagParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.attrs_dict = {}

        def handle_starttag(self, tag, attrs):
            self.attrs_dict = dict(attrs)

    parser = TagParser()
    parser.feed(tag_str)
    return parser.attrs_dict

url = "https://c.xkcd.com/random/comic"
rqst = requests.get(url)

match rqst.status_code:
    case 200:
        # https://stackoverflow.com/a/12982689
        # Regex that removes HTML tags from strings. Only used for TITLE, could be removed?
        notags = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        
        raw = rqst.text
        index = tag2dict(raw.split("\n")[16])['content'][17:-1] # The number of the comic
        imgdt = tag2dict(raw.split("\n")[raw.split("\n").index('<div id="comic">') + 1]) # The 'img' tag where the image source and text live
        
        TITLE = notags.sub("", raw.split("\n")[4])[6:] # Title of the comic
        IMAGE = f"https:{imgdt['src']}" # The 'img' tag's src parameter omits 'https:', add that back!
        TEXT  = html.unescape(imgdt['title']) # Some strings contain HTML entities (&#39;), revert those! 

        show_comic(index, TITLE,IMAGE,TEXT)
        
    case 429:
        msg("Too many requests", "You are being rate-limited, please slow down ;_;")
    case _:
        msg(rqst.status_code, f"HTTP code other than 200 has been returned - {rqst.status_code}!")
