from pygame import mixer

class Sound:
    def __init__(self, filenames):
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(0.2)
        self.main_theme = mixer.Sound(filenames['main_theme'])
        self.coin = mixer.Sound(filenames['coin'])
        self.bump = mixer.Sound(filenames['bump'])
        self.stomp = mixer.Sound(filenames['stomp'])
        self.jump = mixer.Sound(filenames['jump'])
        self.death = mixer.Sound(filenames['death'])
        self.kick = mixer.Sound(filenames['kick'])
        self.brick_bump = mixer.Sound(filenames['brick_bump'])
        self.powerup = mixer.Sound(filenames['powerup'])
        self.powerup_appear = mixer.Sound(filenames['powerup_appear'])
        self.pipe = mixer.Sound(filenames['pipe'])

    def play_sfx(self, sfx):
        self.sfx_channel.play(sfx)

    def play_music(self, music):
        self.music_channel.play(music)
