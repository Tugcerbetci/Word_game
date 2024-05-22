import pygame
from pygame.locals import *

pygame.init()

# Pencere boyutları
WIDTH = 800
HEIGHT = 600

# Renkler
PINK = (255, 192, 203)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Pencere oluşturma
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kelime Oyunu")

clock = pygame.time.Clock()

def draw_text(text, color, x, y, font_size=30, italic=False):
    font = pygame.font.Font(None, font_size)
    font.set_italic(italic)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    window.blit(text_surface, text_rect)

def get_input(oyuncu_index, timeout):
    input_text = ""
    input_finished = False
    start_time = pygame.time.get_ticks()

    while not input_finished:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    input_finished = True
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        window.fill(PINK)
        draw_text(f"Kelime: {input_text}", RED if oyuncu_index == 0 else BLUE, WIDTH // 2, HEIGHT // 2, font_size=40, italic=True)
        draw_text(f"Oyuncu {oyuncu_index + 1}", RED if oyuncu_index == 0 else BLUE, WIDTH // 2, HEIGHT // 2 + 50, font_size=30)

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        remaining_time = timeout - elapsed_time
        draw_text(f"Kalan Süre: {remaining_time}", RED if oyuncu_index == 0 else BLUE, WIDTH // 2, HEIGHT - 50, font_size=30)

        pygame.display.flip()
        clock.tick(60)

        if remaining_time <= 0:
            input_finished = True

    return input_text.lower()

def kelime_oyunu():
    kelimeler = set()  # Oyun sırasında girilen kelimeleri tutmak için bir küme kullanıyoruz
    oyuncular = ["Oyuncu 1", "Oyuncu 2"]
    oyuncu_index = 0
    kelime_sayisi = 1
    timeout = 20  # Oyunculara verilecek süre (saniye cinsinden)

    while True:
        oyuncu = oyuncular[oyuncu_index]
        draw_text(f"Kelime Sayısı: {kelime_sayisi}", RED if oyuncu_index == 0 else BLUE, WIDTH - 100, 30, font_size=25, italic=True)
        yeni_kelime = get_input(oyuncu_index, timeout)

        # Girilen kelimenin geçerli olup olmadığını kontrol ediyoruz
        if not yeni_kelime.isalpha():
            print("Geçerli bir kelime girmelisiniz. Sadece harflerden oluşmalıdır.")
            continue

        # Daha önce girilen bir kelimeyi tekrarlamaya çalışan oyuncuyu kontrol ediyoruz
        if yeni_kelime in kelimeler:
            print(f"{oyuncu}, daha önce kullanılan bir kelimeyi tekrarladınız. Kaybettiniz!")
            break

        # İlk kelime için herhangi bir kısıtlama olmadığından doğrulama yapmıyoruz
        if not kelimeler:
            kelimeler.add(yeni_kelime)
        else:
            # Önceki kelimenin son harfi ile başlayan bir kelime kontrolü yapıyoruz
            onceki_kelime = list(kelimeler)[-1]
            if onceki_kelime[-1].lower() == yeni_kelime[0].lower():
                kelimeler.add(yeni_kelime)
                kelime_sayisi += 1
            else:
                print(f"{oyuncu}, kelimenin son harfi ile başlayan bir kelime girmelisiniz. Kaybettiniz!")
                break

        oyuncu_index = (oyuncu_index + 1) % 2  # Oyuncu sırasını değiştiriyoruz

    draw_text("Oyun bitti!", RED if oyuncu_index == 1 else BLUE, WIDTH // 2, HEIGHT // 2 + 100, font_size=40)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        draw_text("Tekrar Oyna? (E/H)", RED if oyuncu_index == 1 else BLUE, WIDTH // 2, HEIGHT // 2 + 150, font_size=30)

        pygame.display.flip()
        clock.tick(60)

        keys = pygame.key.get_pressed()
        if keys[K_e]:
            return  # Oyunu tekrar başlat
        elif keys[K_h]:
            pygame.quit()
            exit()

# Oyunu başlatmak için fonksiyonu çağırıyoruz
kelime_oyunu()
