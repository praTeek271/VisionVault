from PIL import Image



app = Flask(__name__, static_url_path='', template_folder='templates', static_folder='static')



# ...

def check_files():
    image_names = os.listdir('static/images')
    for i in image_names:
        img = os.path.join("static/images", i).split(".")[0] + "_thumb"
        if img not in os.listdir("static/_thumb"):
            present.append(False)
            thumb_path = thumb_maker(i)
            # Create thumbnail image
            image_path = os.path.join("static/images", i)
            image = Image.open(image_path)
            image.thumbnail((100, 100))
            image.save(thumb_path)
        else:
            present.append(True)

    if False in present:
        thumb_names = map(thumb_maker, image_names)
    else:
        print("All files are present")

# ...
