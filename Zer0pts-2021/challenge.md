### Introduction

```
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

```
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


### Pollution

http://localhost:8081/text?text=asd123&a[constructor][prototype][pollute]=pollutedxyz

1. `params`
2. `params.__proto__`
3. `Object.__proto__.pollute`
4. `document.__proto__.pollute`