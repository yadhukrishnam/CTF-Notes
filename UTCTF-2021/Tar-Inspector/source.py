import subprocess
import os
import re
from random import randrange
from treeify import tree_from_listing

from flask import *

# set up upload/extract folders
ALLOWED_EXTENSIONS = {'tar'}
UPLOAD_DIR = '/tmp/uploads'
EXTRACT_DIR = '/tmp/extracts'
if not os.path.isdir(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)
if not os.path.isdir(EXTRACT_DIR):
    os.mkdir(EXTRACT_DIR)

# configure app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_PATH'] = 2 ** 16 # 64 KB
app.secret_key = 'l1k29348n1goin198ndgn1e'

# checks if a file is a .tar file for user feedback reasons
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# creates a secured version of the filename
def secure_filename(filename):
    # strip extension and any sneaky path traversal stuff
    filename = filename[:-4]
    filename = os.path.basename(filename)
    # escape shell metacharacters
    filename = re.sub("(!|\$|#|&|\"|\'|\(|\)|\||<|>|`|\\\|;)", r"\\\1", filename)
    filename = re.sub("\n", "", filename)
    # add extension
    filename += '__'+hex(randrange(10000000))[2:]+'.tar'
    return filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print('uploading file...', flush=True)
    if 'file' not in request.files:
        return redirect('/')
    f = request.files['file']
    if f.filename == '':
        flash('No selected file!')
        return redirect('/')
    if allowed_file(f.filename):
        filename = secure_filename(f.filename)
        print(filename, flush=True)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        command = 'tar xvf {}/{}'.format(app.config['UPLOAD_FOLDER'], filename)
        print(command, flush=True)
        p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=EXTRACT_DIR)
        if p.returncode != 0:
            print(p.stderr.decode('ascii'), flush=True)
            flash('Failed to un-tar your archive :(')
            return redirect('/')
        print(p.stdout.decode('ascii'), flush=True)
        listing = [line for line in p.stdout.decode('ascii').split('\n')[:-1]]
        content = tree_from_listing(listing).split('\n')
        return render_template('results.html', content=content, filename=filename)
    else:
        flash('Invalid file extension! Only .tar files allowed.')
        return redirect('/')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
