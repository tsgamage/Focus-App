import pygame
from threading import Thread

def notify_user():
    pygame.mixer.init()
    notification_sound = pygame.mixer.Sound("assets/sounds/notify.mp3")
    notification_sound.play()
    pygame.time.delay(int(notification_sound.get_length() * 1000))

def play_notification_sound():
    Thread(target=notify_user).start()