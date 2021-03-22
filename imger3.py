"""
Imger3.py v1.0 Public Release

Creator: Mile

This script relies on Pillow (PIL).

"""

import os.path
import random
import time
from os import listdir
from twisted.internet.reactor import callLater
from pyspades.contained import BlockAction, SetColor
from pyspades.constants import *
from pyspades.common import make_color
from piqueserver.commands import command, get_player, name, admin
from PIL import Image

# USER INPUTS

EMOTE_COOLDOWN = 20


# END OF USER INPUTS

DISABLED_USERS = []

with open('img/userdata/DISABLED_USERS.txt', 'r') as userd:
    for name in userd:
        DISABLED_USERS.append(name.rstrip('\n'))


VOXEL_PROC_EMOTES = {}


def processvoxels(protocol, map, is_forced, is_emote):
    if is_emote:
        if not VOXEL_PROC_EMOTES:
            return
        else:
            entry_list = list(VOXEL_PROC_EMOTES.items())
            randomVox = random.choice(entry_list)
            VOXEL_PROC_EMOTES.pop(randomVox[0])
            p = randomVox[0]
            RGB = randomVox[1]
            zee = map.get_z(p[0], p[1])
    else:
        if not VOXEL_PROC_HEAVEN:
            return
        else:
            entry_list = list(VOXEL_PROC_HEAVEN.items())
            randomVox = random.choice(entry_list)
            VOXEL_PROC_HEAVEN.pop(randomVox[0])
            p = randomVox[0]
            RGB = randomVox[1]
            zee = 1
    block_action, set_color = BlockAction(), SetColor()
    set_color.value = make_color(RGB[0], RGB[1], RGB[2])
    set_color.player_id = 33
    protocol.broadcast_contained(set_color)
    block_action.player_id = 33
    if not is_emote:
        map.set_point(p[0], p[1], zee, RGB)
    block_action.x = p[0]
    block_action.y = p[1]
    block_action.z = zee
    block_action.value = BUILD_BLOCK
    if is_forced:
        protocol.broadcast_contained(block_action, save=True)
    else:
        # Send block updates to everyone but voxlap and turned off users
        protocol.broadcast_contained(block_action, save=not is_emote, rule=lambda p: p.is_img is True)


def imger(protocol, a, b, map, gn):
    graffiti = Image.open('img/' + gn + '.png')

    value = int(graffiti.width / 2)
    voxel_selection_user = list()

    for a2 in range(a - value, a + value):
        for b2 in range(b - value, b + value):
            result = tuple((a2, b2))
            voxel_selection_user.append(result)

    for p in voxel_selection_user:
        if map.get_solid(p[0], p[1], map.get_z(p[0], p[1])):
            px = p[0] - a - value
            py = p[1] - b - value
            if graffiti.getpixel((px, py))[0] == 0 and \
                    graffiti.getpixel((px, py))[1] == 0 and \
                    graffiti.getpixel((px, py))[2] == 0:
                continue
            else:
                R3 = graffiti.getpixel((px, py))[0]
                G3 = graffiti.getpixel((px, py))[1]
                B3 = graffiti.getpixel((px, py))[2]
                if R3 > 254:
                    R3 = 254
                if G3 > 254:
                    G3 = 254
                if B3 > 254:
                    B3 = 254
                if R3 < 0:
                    R3 = 0
                if G3 < 0:
                    G3 = 0
                if B3 < 0:
                    B3 = 0
                VOXEL_PROC_EMOTES[p] = tuple((R3, G3, B3))
    iter = 0.0
    count = 0
    while count < graffiti.width * graffiti.height:
        callLater(iter, processvoxels, protocol, map, 0, 1)
        iter += 0.005
        count += 1


def client_check(self):
    goodclient = ["OpenSpades", "BetterSpades"]
    for client in goodclient:
        if not self.is_img and client in self.client_string and self.name not in DISABLED_USERS:
            self.is_img = True
            self.send_chat("Client authentication complete. Imger turned ON.")


@command("img")
def img(self):
    if "Voxlap" not in self.client_string:
        if self.is_img:
            self.is_img = False
            DISABLED_USERS.append(self.name)
            self.send_chat("Imger turned OFF. Named added to OFF registry")

        else:
            self.is_img = True
            if self.name in DISABLED_USERS:
                DISABLED_USERS.remove(self.name)
            self.send_chat("Imger turned ON. Name removed from OFF registry.")
    else:
        self.send_chat("Cannot run imger on classic client. Please upgrade to OpenSpades or BetterSpades.")


@command("emote")
def emote(self, filename='owo'):
    if os.path.isfile('img/' + filename + '.png'):
        cooldown = int(time.time() - self.emote_time)
        if cooldown > EMOTE_COOLDOWN:
            protocol = self.protocol
            map = protocol.map
            playerx = int(self.world_object.position.x)
            playery = int(self.world_object.position.y)
            imger(protocol, playerx, playery, map, filename)
            self.emote_time = time.time()
        else:
            self.send_chat(str(EMOTE_COOLDOWN) + " seconds cooldown between emotes. (" + str(EMOTE_COOLDOWN - cooldown) + " seconds remaining.)")
    else:
        self.send_chat("No emote found.")


@command("emotelist")
def emotelist(self):
    files = [f for f in listdir('img/')]
    for r in (("\'", ""), (".png", ""), ("[", ""), ("]", "")):
        files = str(files).replace(*r)
    self.send_chat(files)
    self.send_chat("Type /emote <name> to confirm your choice.")


def apply_script(protocol, connection, config):
    class ImgProtocol(protocol):
        def __init__(self, *arg, **kw):
            protocol.__init__(self, *arg, **kw)
            self.imgerglow_server_message(True, True)

        def imgerglow_server_message(self, sendFirstMsg, sendFirstFirstMsg):
            if sendFirstMsg:
                message = "Imger enabled on this server. You can toggle the plugin with /img"
                self.send_chat(message)
                if sendFirstFirstMsg:
                    callLater(300, self.imgerglow_server_message, False, False)
                else:
                    callLater(200, self.imgerglow_server_message, False, False)
            else:
                self.send_chat("Type /emotelist to view available patterns.")
                callLater(200, self.imgerglow_server_message, True, False)

        def on_map_change(self, map):
            global DISABLED_USERS
            with open('img/userdata/DISABLED_USERS.txt', 'w') as file:
                userstr = ""
                for user in DISABLED_USERS:
                    userstr += str(user) + "\n"
                file.write(userstr)
            return protocol.on_map_change(self, map)

    class ImgConnection(connection):

        def __init__(self, *args, **kwargs):
            connection.__init__(self, *args, **kwargs)
            self.is_img = True
            self.emote_time = 0

        def on_spawn(self, pos):
            if self.is_img and "Voxlap" in self.client_string:
                self.is_img = False
            elif self.is_img and self.name in DISABLED_USERS:
                self.is_img = False
            callLater(5, client_check, self)
            return connection.on_spawn(self, pos)

    return ImgProtocol, ImgConnection
