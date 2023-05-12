import os
import random
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
root_directory = r'D:\iKoC2022\Code\MediaBrowser\assets'


@app.route('/')
def home():
    return render_path('')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<path:subpath>')
def render_path(subpath):
    absolute_path = os.path.join(root_directory, subpath)
    if os.path.isfile(absolute_path):
        return send_from_directory(root_directory, subpath)
    else:
        file_list = os.listdir(absolute_path)
        processed_files = process_files(file_list, absolute_path)

        # Get parent folder
        parent_folder = os.path.dirname(subpath) if subpath else ''

        # Get list of sub_folders
        sub_folders = [file for file in processed_files if file['type'] == 'dir']

        current_folder = os.path.basename(subpath) if subpath else 'Root'
        return render_template('index.html', files=processed_files, current_folder=current_folder,
                               parent_folder=parent_folder, current_path=subpath, subfolders=sub_folders)


def process_files(file_names, parent_path):
    dir_list = []
    media_list = []
    img_list = []
    vid_list = []

    for file in file_names:
        file_path = os.path.join(parent_path, file)
        rel_path = os.path.relpath(file_path, root_directory).replace('\\', '/')

        if os.path.isdir(file_path):
            image_files = [f for f in os.listdir(file_path) if
                           f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
            random_image = random.choice(image_files) if image_files else None
            random_image_path = os.path.join(rel_path, random_image).replace('\\',
                                                                             '/') if random_image else 'static/folder-icon.png'
            dir_list.append({'type': 'dir', 'path': rel_path, 'name': file, 'random_image': random_image_path})
        elif file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
            img_list.append({'type': 'image', 'path': rel_path, 'name': file,
                             'mime': 'image/' + os.path.splitext(file)[1][1:].lower()})
        elif file.lower().endswith(('.mp4', '.webm', '.ogv')):
            vid_list.append({'type': 'video', 'path': rel_path, 'name': file,
                             'mime': 'video/' + os.path.splitext(file)[1][1:].lower()})

    return dir_list + img_list + vid_list


if __name__ == '__main__':
    app.run(debug=True)
