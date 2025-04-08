import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def load_texture(path):
    try:
        texture_surface = pygame.image.load(path).convert_alpha()
        texture_data = pygame.image.tostring(texture_surface, "RGBA", True)

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texture_surface.get_width(),
                     texture_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        return tex_id
    except Exception as e:
        print(f"Ошибка загрузки текстуры {path}: {str(e)}")
        return None


# Вершины с текстурными координатами (x,y,z, u,v)
vertices = (
    # Передняя грань (front)
    ((1, -2.5, 1), (0, 0)),  # низ-лево
    ((1, 2.5, 1), (0, 1)),  # верх-лево
    ((-1, 2.5, 1), (1, 1)),  # верх-право
    ((-1, -2.5, 1), (1, 0)),  # низ-право

    # Задняя грань
    ((1, -2.5, -1), (1, 0)),  # 0
    ((1, 2.5, -1), (1, 1)),  # 1
    ((-1, 2.5, -1), (0, 1)),  # 2
    ((-1, -2.5, -1), (0, 0)),  # 3

    # Правая грань
    ((1, -2.5, -1), (0, 0)),  # 0
    ((1, 2.5, -1), (0, 1)),  # 1
    ((1, 2.5, 1), (1, 1)),  # 5
    ((1, -2.5, 1), (1, 0)),  # 4

    # Левая грань
    ((-1, -2.5, -1), (1, 0)),  # 3
    ((-1, 2.5, -1), (1, 1)),  # 2
    ((-1, 2.5, 1), (0, 1)),  # 7
    ((-1, -2.5, 1), (0, 0)),  # 6

    # Верх
    ((1, 2.5, -1), (0, 0)),  # 1
    ((-1, 2.5, -1), (1, 0)),  # 2
    ((-1, 2.5, 1), (1, 1)),  # 7
    ((1, 2.5, 1), (0, 1)),  # 5

    # Низ
    ((1, -2.5, -1), (0, 1)),  # 0
    ((-1, -2.5, -1), (1, 1)),  # 3
    ((-1, -2.5, 1), (1, 0)),  # 6
    ((1, -2.5, 1), (0, 0))  # 4
)

# Группы вершин для каждой грани
faces = [
    (0, 1, 2, 3),  # Передняя
    (4, 5, 6, 7),  # Задняя
    (8, 9, 10, 11),  # Правая
    (12, 13, 14, 15),  # Левая
    (16, 17, 18, 19),  # Верх
    (20, 21, 22, 23)  # Низ
]


def draw_building(textures):
    for i, face in enumerate(faces):
        texture = textures.get(i)

        if texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, texture)
            glBegin(GL_QUADS)
            for vertex_idx in face:
                glTexCoord2fv(vertices[vertex_idx][1])
                glVertex3fv(vertices[vertex_idx][0])
            glEnd()
            glDisable(GL_TEXTURE_2D)
        else:
            glBegin(GL_QUADS)
            glColor3fv((0.5, 0.5, 0.5))
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx][0])
            glEnd()


def main():
    pygame.init()
    display = (1000, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Загрузка текстур (0:front, 1:back, 2:right, 3:left, 4:top, 5:bottom)
    textures = {
        0: load_texture("front.jpg"),
        1: load_texture("back.jpg"),
        2: load_texture("right.jpg"),
        3: load_texture("left.jpg"),
        4: load_texture("top.jpg"),  # Опционально
        5: load_texture("bottom.jpg")  # Опционально
    }

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -15)
    glEnable(GL_DEPTH_TEST)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

        glRotatef(0.6, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Первое здание
        glPushMatrix()
        glTranslatef(-3, 0, 0)
        draw_building(textures)
        glPopMatrix()

        # Второе здание
        glPushMatrix()
        glTranslatef(0, 0, 0)
        draw_building(textures)
        glPopMatrix()

        # Третье здание
        glPushMatrix()
        glTranslatef(3, 0, 0)
        draw_building(textures)
        glPopMatrix()

        # Четвертое здание
        glPushMatrix()
        glTranslatef(0, 0, -3)
        draw_building(textures)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()