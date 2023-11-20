from flask import Flask, request, send_file, render_template, redirect, url_for
import os
from thumbnail import thumb_maker

app = Flask(__name__, static_url_path='', template_folder='templates', static_folder='static')

def check_files():
    image_names = os.listdir('static/images')
    for i in image_names:
        img = os.path.join("static/images", i)
        thumb_name = f"{os.path.splitext(i)[0]}_thumb.jpg"
        thumb_path = os.path.join("static/_thumb", thumb_name)
        
        if thumb_name not in os.listdir("static/_thumb"):
            thumb_maker(img, 1)
            present.append(False)
        else:
            present.append(True)

    if False in present:
        map(thumb_maker, image_names)
    else:
        print("All files are present")

@app.route('/')
def index():
    global present
    present = []
    check_files()
    image_names = os.listdir('static/images')
    thumb_names = os.listdir('static/_thumb')

    # Check if thumbnails are present for all images
    for image_name in image_names:
        thumb_name = f"{os.path.splitext(image_name)[0]}_thumb.jpg"
        thumb_path = os.path.join('static/_thumb', thumb_name)

        if thumb_name not in thumb_names:
            # Thumbnail is missing, generate it
            thumb_maker(image_name, 1)

    thumb_names = os.listdir('static/_thumb')
    thumb_names = list(map(lambda x: os.path.join('_thumb', x), thumb_names))
    file_names = zip(image_names, thumb_names)
    print(file_names)
    return render_template('index.html', file_names=file_names)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']

        # If the user does not select a file, the browser also
        # submits an empty part without filename
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file to the "static/images" directory
            file.save(os.path.join('static/images', file.filename))

            # Create thumbnail immediately after upload
            thumb_maker(file.filename, 1)

            return redirect(url_for('index'))

    return render_template('upload.html')

@app.route('/download')
def download_image():
    image_name = request.args.get('image_name')
    image_path = os.path.join('static/images', image_name)

    if not os.path.exists(image_path):
        return 'Image not found', 404

    return send_file(image_path, as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run()
