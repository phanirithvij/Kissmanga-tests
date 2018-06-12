# [KissManga.com](http://kissmanga.com) Downloader

Inspired By [Pratikh's Kissmanga-Pdf-Downloader](https://github.com/pratikhit07/kissmanga-pdf-downloader)

Added some more options such as [range-download](https://github.com/phanirithvij/Kissmanga-tests#range-download)

## Usage

After cloning the repo

```bash
    cd Kissmanga-tests
    chmod +x *.py
    ./KissMangaDownload.py
```

## Dependencies

### Nodejs and npm

```bash
    node
```

Download from [node](https://nodejs.org)

#### CryptoJS

```bash
    crypto-js
```

Do

```bash
    npm install crypto-js
```

### Python and libraries

```bash
    python2.7 or 3.x
```

Installation

```bash
    sudo apt-get install python
```

#### Requirements

```python3
    cfscrape
    bs4
    requests
```

Do

```bash
    pip install -r requirements.txt
```

## Need to Implement

### range-download

eg:

* chapter 1 to 39

### IMPORTANT

#### About index.js

TODO(Not a todo but it's important)

* [http://kissmanga.com/Scripts/io.js](http://kissmanga.com/Scripts/lo.js)
* [http://kissmanga.com/Scripts/ca.js](http://kissmanga.com/Scripts/ca.js)

* and [crypto-js](https://www.npmjs.com/package/crypto-js) npm

are in [index.js](https://github.com/phanirithvij/Kissmanga-tests/blob/master/index.js) which is used as the heart for the decryption of the image links
