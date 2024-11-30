import pygame.midi
pygame.midi.init()
for i in range(pygame.midi.get_count()):
    print(pygame.midi.get_device_info(i))
pygame.midi.quit()
