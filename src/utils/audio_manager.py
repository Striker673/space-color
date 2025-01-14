import pygame


class AudioManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AudioManager, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.load_audio()

    def load_audio(self):
        sound_effects = {'jump': 'jump.wav', 'death': 'death.wav', 'collect': 'collect.wav'}

        for sound_name, filename in sound_effects.items():
            try:
                sound = pygame.mixer.Sound(f"../assets/sounds/{filename}")
                self.sounds[sound_name] = sound
                self.sounds[sound_name].set_volume(self.sfx_volume)
            except Exception as e:
                print(f"Error loading sound {sound_name}: {e}")

    def play_music(self):
        try:
            pygame.mixer.music.load("../assets/sounds/soundtrack.mp3")
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # -1 =  infinite loop
        except Exception as e:
            print(f"Error playing music: {e}")

    def play_sound(self, sound_name: str):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def set_music_volume(self, volume: float):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume: float):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def stop_music(self):
        pygame.mixer.music.stop()

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()
