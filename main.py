from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

# Загрузка текстуры
def load_texture(path):
    texture_surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_size()

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    return tex_id


# Рисуем дом с текстурами
def draw_textured_building(textures):
    glEnable(GL_TEXTURE_2D)

    # Фронт
    glBindTexture(GL_TEXTURE_2D, textures['front'])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-1, -2.5,  1)
    glTexCoord2f(1, 0); glVertex3f( 1, -2.5,  1)
    glTexCoord2f(1, 1); glVertex3f( 1,  2.5,  1)
    glTexCoord2f(0, 1); glVertex3f(-1,  2.5,  1)
    glEnd()

    # Назад
    glBindTexture(GL_TEXTURE_2D, textures['back'])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f( 1, -2.5, -1)
    glTexCoord2f(1, 0); glVertex3f(-1, -2.5, -1)
    glTexCoord2f(1, 1); glVertex3f(-1,  2.5, -1)
    glTexCoord2f(0, 1); glVertex3f( 1,  2.5, -1)
    glEnd()

    # Лево
    glBindTexture(GL_TEXTURE_2D, textures['left'])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-1, -2.5, -1)
    glTexCoord2f(1, 0); glVertex3f(-1, -2.5,  1)
    glTexCoord2f(1, 1); glVertex3f(-1,  2.5,  1)
    glTexCoord2f(0, 1); glVertex3f(-1,  2.5, -1)
    glEnd()

    # Право
    glBindTexture(GL_TEXTURE_2D, textures['right'])
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f( 1, -2.5,  1)
    glTexCoord2f(1, 0); glVertex3f( 1, -2.5, -1)
    glTexCoord2f(1, 1); glVertex3f( 1,  2.5, -1)
    glTexCoord2f(0, 1); glVertex3f( 1,  2.5,  1)
    glEnd()

    glDisable(GL_TEXTURE_2D)

# Основной цикл
def main():
    pygame.init()
    display = (1000, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[1]/display[0]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    glEnable(GL_DEPTH_TEST)

    # Загружаем текстуры
    textures = {
        'front': load_texture('front.jpg'),
        'back': load_texture('back.jpg'),
        'left': load_texture('left.jpg'),
        'right': load_texture('right.jpg')
    }

    angle = 0
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glRotatef(0, 0, 0, 0)
        glRotatef(0.4, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_textured_building(textures)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()