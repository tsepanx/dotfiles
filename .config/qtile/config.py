# -*- coding: utf-8 -*-
import os, random
import subprocess
from libqtile.config import Key, Screen, Group, Match, Drag, Click, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from bars import get_screens
from keys import default_keys

TERMINAL_CMD = 'alacritty'

home = os.path.expanduser('~')

cmd_run = lambda s: subprocess.call(s.split())

def term_command(cmd=None, title=None, t=TERMINAL_CMD):
    if not cmd:
        return t
    else:
        title = cmd if not title else title
        return f"{t} -t '{title}' -e '{cmd}'"

def prin(*s):
    subprocess.call(['notify-send', *list(map(str, s))])


################################################################################
# ------------------------------      APPS      ------------------------------ #
################################################################################

class App:
    def __init__(self, run, wm_class=None, wm_name=None, frame=None):
        self.run = run
        self.wm_class = wm_class
        self.wm_name = wm_name

        if frame:
            self.width, self.height = frame

    def match(self):
        return Match(
            wm_class=[self.wm_class], 
            title=[self.wm_name] if self.wm_name else None
        )

    def spawn(self):
        return lazy.spawn(self.run)

    def __str__(self):
        return self.run


class TermApp(App):
    def __init__(self, cmd, **kwargs):
        super().__init__(term_command(cmd), None, cmd, **kwargs)


class Apps:
    BROWSER = App('firefox', 'firefox')
    CHROMIUM = App('chromium')
    TOR_BROWSER = App('sh .tor-browser/Browser/firefox', 'Tor Browser')

    TG = App('telegram-desktop', 'TelegramDesktop')
    FM = App('pcmanfm', 'Pcmanfm')
    GPARTED = App('gparted', 'GParted')
    TIMESHIFT = App('timeshift-launcher', 'Timeshift-gtk')
    KEEPASS = App('keepassxc', 'KeePassXC')
    NITROGEN = App('nitrogen', 'Nitrogen')
    MPV = App('mpv', 'mpv')

    SCREENSHOT = App('flameshot gui')

    DMENU = App("dmenu_run -p 'Run: '")
    ROFI = App("rofi -show run")

    HIBERRNATION = App('systemctl hibernate')
    LOCK = App('i3lock-fancy -p')

    THUNDERBIRD = App('thunderbird', 'Thunderbird', frame=(1100, 600))
    VIRT_MANAGER = App('virt-manager', 'Virt-manager')
    ELECTRUM = App('electrum', 'electrum')

    TERM = TermApp('')

    HTOP = TermApp('htop')
    RANGER = TermApp('ranger')
    NCMPCPP = TermApp('ncmpcpp')
    MUTT = TermApp('mutt')


################################################################################
# --------------------------      KEYBINDINGS      --------------------------- #
################################################################################

mod = "mod4"
alt = "mod1"
ctrl = "control"

def map_keys(mod_keys, keys_dict):
    mapper = lambda x: Key(mod_keys, x[0], x[1].spawn())
    return list(map(mapper, keys_dict.items()))

# === MOD + ALT + KEY ===
mod_alt_keys = {
    'l': Apps.BROWSER,
    'c': Apps.CHROMIUM,
    't': Apps.TOR_BROWSER,
    'p': Apps.FM,
    'f': Apps.SCREENSHOT,
    'm': Apps.NCMPCPP,
    'n': Apps.TG,
    'r': Apps.RANGER,
    'k': Apps.KEEPASS,
    'v': Apps.VIRT_MANAGER,
    'e': Apps.MUTT,
}

# === MOD + CONTROL + KEY ===
mod_control_keys = {
    'v': Apps.TIMESHIFT,
    'g': Apps.GPARTED,
    # 'e': Apps.DMENU,
}

# === CONTROL + ALT + KEY ===
control_alt_keys = {
    'k': Apps.HIBERRNATION,
    'l': Apps.LOCK,
}

keys = [
    *default_keys(),

    *map_keys([mod, alt], mod_alt_keys),
    *map_keys([mod, ctrl], mod_control_keys),
    *map_keys([ctrl, alt], control_alt_keys),

    # --- MY ---
    Key([mod], "Return", Apps.TERM.spawn()),
    # Key([mod, "shift"], "Return", Apps.ROFI.spawn()),
    Key([mod, "shift"], "Return", Apps.DMENU.spawn()),
    Key(["control"], "q", None),

    # Key([], 'F12', lazy.group['scratchpad'].dropdown_toggle('term')),
]

################################################################################
# ----------------------------      LAYOUTS      ----------------------------- #
################################################################################

layout_theme = {
    "border_width": 3,
    "margin": 3,
    "border_focus": "aa75c8",
    "border_normal": "1D2330"
}

layouts = [
    # layout.Zoomy(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # laout.MonadWide(**layout_theme),
    # layout.Slice(),


    # layout.MonadTall(
    #     ratio=0.55,
    #     **layout_theme
    # ),


    layout.Columns(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Max(**layout_theme),
]


################################################################################
# -----------------------------      GROUPS      ----------------------------- #
################################################################################

class GroupCreator:
    __groups = []
    cur_ind = 0
    GROUP_NAMES = 'asdfuiop123456789qwert'

    @staticmethod
    def label(name, icon):
        return f'{icon} {name.capitalize()}'

    def new(self, icon='???', app_spawn=[], app_matches=[], custom_name=None, **kwargs):
        name = self.GROUP_NAMES[self.cur_ind]
        label_name = name if not custom_name else custom_name
        label = self.label(label_name, icon)

        matches = list(map(lambda x: x.match(), app_matches))
        spawn = list(map(lambda x: x.run, app_spawn))

        new_group = Group(
            name=name,
            label=label,
            matches=matches,
            spawn=spawn,
            **kwargs,
        )

        self.__groups.append(new_group)
        self.cur_ind += 1

    def get_keys(self):
        for i in self.GROUP_NAMES:
            yield Key([mod], i, lazy.group[i].toscreen())
            yield Key([mod, "shift"], i, lazy.window.togroup(i))

    def get_groups(self):
        return self.__groups


floating_group_settings = {'layouts': [layout.Floating(**layout_theme)], 'layout': 'floating'}

creator = GroupCreator()
group = creator.new

# === Groups declare ===
# ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ??? ???? ??????????????????? ??? ??? ??? ??? ??? ???v  ??? ??? ??? ?????????? ????
# ???  ???   ???    ??? ??? ??? ??? ??? ??? ???


group("???", layout='max')
group("???")
group("???")

group("???")
group("???")

group("???")
group("???")

group("??? ???", [Apps.HTOP], [Apps.TG])
group("???") # 1
group("???") # 2
# group("???") # Royal
group("???") # 3 Comet
group("???") # 4 Key
group("???")
group("???") # 6
group("???") # 7 Frame
group("???")
group("???")
# group("???  ??? ??? ??? ??? ??? ??? ??? ???")

group("", custom_name='{', layout='max')
group("", custom_name='{', layout='max')
group("", custom_name='(', layout='max')
group("", custom_name=')', layout='max')
group("+", [], [Apps.TOR_BROWSER], layout='max')


# === --- ===


groups = [
    *creator.get_groups(),
    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown("term", "termite", opacity=0.8, on_focus_lost_hide=False),

        # define another terminal exclusively for qshell at different position
        # DropDown("qshell", "urxvt -hold -e qshell",
        #          x=0.05, y=0.4, width=0.9, height=0.6, opacity=0.9,
        #          on_focus_lost_hide=True) 
        ]),
]

keys.extend(list(creator.get_keys()))

################################################################################
# -------------------------      FLOATING RULES      ------------------------- #
################################################################################

floating_windows = [
    Apps.RANGER,
    Apps.NCMPCPP,
    Apps.GPARTED,
    Apps.TIMESHIFT,
    Apps.NITROGEN,
    # Apps.MPV,
    Apps.THUNDERBIRD,
    # Apps.ELECTRUM,
]

@hook.subscribe.client_new
def for_window(window):
    def get_window_class(window):
        return window.window.get_wm_class()[1]

    def get_window_name(window):
        return window.window.get_name()

    def match_window(name, classname, floating_windows):
        for i in floating_windows:
            match_pair = (i.wm_class if i.wm_class else classname, i.wm_name if i.wm_name else name)

            if match_pair == (classname, name):
                return i

        return None

    name = get_window_name(window)
    classname = get_window_class(window)

    matched = match_window(name, classname, floating_windows)

    if matched:
        window.floating = True
        window.width = matched.width
        window.height = matched.height


################################################################################
# -----------------------------      OTHER      ------------------------------ #
################################################################################

screens = get_screens()

mouse = [
    Drag([mod], "Button1", 
        lazy.window.set_position_floating(), 
        lazy.window.bring_to_front(),
        start=lazy.window.get_position(),
    ),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

follow_mouse_focus = True
bring_front_click = True
cursor_warp = False
focus_on_window_activation = True # "smart"


@hook.subscribe.startup_once
def start_once():
    cmd_run(home + '/.config/qtile/autostart.sh')


@hook.subscribe.focus_change
def float_to_front(qtile):
    # print(qtile.currentGroup.windows)
    for window in qtile.currentGroup.windows:
        if window.floating:
            window.cmd_bring_to_front()

@hook.subscribe.focus_change
def float_mpv():
    subprocess.Popen(os.path.expanduser('~/.config/qtile/mpv.py'))

wmname = "Wayland"
