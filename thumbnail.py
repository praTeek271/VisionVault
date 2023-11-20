import os
from PIL import Image
import PySimpleGUI as sg
import io

def thumb_maker(image_path, ods=0):
    thumb_path = None

    if ods != 1 and not image_path.startswith("static/images"):
        image_path = os.path.join("images", image_path)
        print(f"ERROR :: --> Image path must start with \'images/\'<-- :: {image_path}")

    try:
        with Image.open(image_path) as image:
            print(f"Image path :: {image_path}")
            image.thumbnail((500, 500), Image.ANTIALIAS)  # Resize image to 500x500 (max size)
            image = image.convert("RGB")  # Convert to RGB color mode
            print('image converted to RGB')
            s = os.path.splitext(os.path.basename(image_path))[0]
            thumb_dir = "static/_thumb"
            print('thumb_dir created')
            os.makedirs(thumb_dir, exist_ok=True)
            thumb_path = os.path.join(thumb_dir, f"{s}_thumb.jpg")
            image.save(thumb_path)

    except Exception or Warning as e:
        # print("ERROR :: -->", e, "<-- ::")
        # try it for 3 times then pass
        print("ERROR :: -->", e, "<-- ::")
    return thumb_path
if __name__=="__main__":
        
    # GUI layout
    layout = [
        [sg.Text("Image Path:"), sg.Input(key="-IMAGE_PATH-"), sg.FileBrowse()],
        [sg.Image(key="-IMAGE_PREVIEW-")],
        [sg.Text(size=(40, 1), key="-OUTPUT-")],
        [sg.Button("Generate Thumbnail"), sg.Button("Exit")]
    ]

    # Create the window
    window = sg.Window("Thumbnail Maker", layout)

    # Event loop
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == "Exit":
            break
        
        if event == "Generate Thumbnail":
            image_path = values["-IMAGE_PATH-"]
            thumb_path = thumb_maker(image_path, 1)
            window["-OUTPUT-"].update(f"Thumbnail generated: {thumb_path}")
            
            # Update image preview
            image = Image.open(image_path)
            image.thumbnail((200, 200))
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE_PREVIEW-"].update(data=bio.getvalue())
            
    # Close the window
    window.close()
