Keyboard Tiler
===================
What is it?
-----------
Why not have your keyboard represent the grid/tiles of your screen? This is a python2 script to place windows on the tiles of your screen representing the tiles(keys) of your keyboard. The keys from 1 down to Z over to / and up to 0 forms a 4x10 grid, giving us 40 tiles to work with.

With this script you can have tiling functionality with simple keybindings in any floating WM. It has been tested on Pekwm and Openbox so far, though any window manager that works well with xdotool should work.

Some examples (look down at your keyboard and you'll get the idea):
- Fullscreen: `python2 keyboard-tiler.py place  '1' '/'`
- Top Half of Screen: `python2 keyboard-tiler.py place '1' 'p'`
- Top Right of Screen: `python2 keyboard-tiler.py place '6' 'p'`
- Right Half of Screen: `python2 keyboard-tiler.py place '6' '/'`

The best part? You can hook this into a chorded keymap program such as xchainkeys or just pipe it from dmenu.


Usage
-----

**Prerequisites:** python2, xdotool (just a port of keyboard-tiler to python with stronger argument enforcing)

Keyboard Tiler is just a simple script so using it is as simple as ```python2 keyboard-tiler.py place '1' '/'``` (that would make a window fullscreen). You
can
also copy the script to your $PATH to have accessible anywhere. I'd recommend throwing it in a personal bin folder (like ```~/bin```).

### Usage with xchainkeys
[Xchainkeys](http://code.google.com/p/xchainkeys/) provides chorded/chained keybindings for X11. Xchainkeys can be used to hook into keyboard-tiler.py very easily. Installation details for xchainkeys can be found [here](http://code.google.com/p/xchainkeys/).

- Generate xchainkeys config using provided script: ```python2 keyboard-tiler.py makechains > ~/.config/xchainkeys/xchainkeys.conf```
	* Optional: "moded" option: ```python2 keyboard-tiler.py makechains -m > ~/.config/xchainkeys/xchainkeys.conf```
	* Optional: "decheight" option ```python2 keyboard-tiler.py -d 20 place 1 p``` will change the decoration height the program is accounting for.
- That's it! Run ```xchainkeys && disown``` and your done.
- Hit W-x (or your specified hotkey) and then two sucessive keys
- Add xchainkeys to your ```.xinitrc``` to have it autostart


### Usage with Dmenu & xbindkeys
[Dmenu](http://tools.suckless.org/dmenu/) provides an excellent way to run the script in a chorded type of fashion but not having to run xchainkeys. If you're a loyal Dmenu user this option will appeal to you.

- Add the following to your ```~/.xbindkeys```


``` bash
"echo Hit 2 Keys and Enter | dmenu -b -p 'Keyboard Tiler' | xargs -0 -I KEYS python2 ~/bin/keyboard-tiler.py 'KEYS'"
m:0x40 + c:53
Mod4 + x
```
- Start xbindkeys like ```xbindkeys```
- Hit ```W-x``` and then two sucessive key and enter
- Add xbindkeys to your ```.xinitrc``` to have it autostart

Contributing
------------
- All feedback is welcome!
- Feel free to fork this repo create a topic branch and issue me a pull request.

More Info
---------
- [Original Project Page](http://userbound.com/projects/keyboard-tiler)
- [Original Project](https://github.com/mil/keyboard-tiler)
