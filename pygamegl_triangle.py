from OpenGL.GL import *
import OpenGL.GL.shaders
import ctypes
import pygame
import numpy

vertex_shader = """
#version 120
attribute vec4 position;
void main()
{
   gl_Position = position;
}
"""

fragment_shader = """
#version 120
void main()
{
   gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""

vertices = [-0.58, -0.5, 0.0, 1.0,
            0.58, -0.5, 0.0, 1.0,
            0.0, 0.5, 0.0, 1.0]

vertices = numpy.array(vertices, dtype=numpy.float32)


def create_object(shader):
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

    # Get the position of the 'position' in parameter of our shader and bind it.
    position = glGetAttribLocation(shader, 'position')
    glEnableVertexAttribArray(position)

    # Describe the position data layout in the buffer
    glVertexAttribPointer(position, 4, GL_FLOAT, False, 0, ctypes.c_void_p(0))

    # Send the data over to the buffer
    glBufferData(GL_ARRAY_BUFFER, 48, vertices, GL_STATIC_DRAW)

    # Unbind the VAO first (Important)
    glBindVertexArray(0)

    # Unbind other stuff
    glDisableVertexAttribArray(position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return vertex_array_object


def display(shader, vertex_array_object):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader)

    glBindVertexArray(vertex_array_object)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glBindVertexArray(0)

    glUseProgram(0)


def main():
    pygame.init()
    pygame.display.set_mode((512, 512), pygame.OPENGL | pygame.DOUBLEBUF)
    glClearColor(0.1, 0.2, 0.3, 1.0)
    glEnable(GL_DEPTH_TEST)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    vertex_array_object = create_object(shader)

    clock = pygame.time.Clock()

    while True:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                return

        display(shader, vertex_array_object)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
        pygame.display.flip()


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
