# oxlos

(A reboot of) a Pinax-based platform for crowd-sourced collaborative corpus linguistics.

See <https://vimeo.com/10515200> for a 2010 talk that provides some background to earlier versions of this project.

## Getting Started

Make sure you are using a virtual environment of some sort (e.g. `virtualenv` or
`pyenv`).

```
npm install
pip install -r requirements.txt
./manage.py migrate
./manage.py loaddata sites
npm run dev
```

Browse to http://localhost:3000/
