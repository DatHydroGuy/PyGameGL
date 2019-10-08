from OpenGL.GL import *
import OpenGL.GL.shaders
import ctypes
import pygame
import numpy
import pyrr


vertex_shader = """
#version 130
in vec4 position;
in vec4 colour;
uniform mat4 transformation;
out vec4 newColour;

void main()
{
   gl_Position = transformation * position;
   newColour = colour;
}
"""

fragment_shader = """
#version 130
in vec4 newColour;
out vec4 outColour;

void main()
{
   outColour = newColour;
}
"""

vertices = [
    -0.5, -0.5, 0.5, 1.0, 1.0, 0.0, 0.0, 1.0,
    0.5, -0.5, 0.5, 1.0, 1.0, 1.0, 0.0, 1.0,
    0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0,
    -0.5, 0.5, 0.5, 1.0, 1.0, 0.0, 1.0, 1.0,

    -0.5, -0.5, -0.5, 1.0, 0.0, 0.0, 0.0, 1.0,
    0.5, -0.5, -0.5, 1.0, 0.0, 1.0, 0.0, 1.0,
    0.5, 0.5, -0.5, 1.0, 0.0, 1.0, 1.0, 1.0,
    -0.5, 0.5, -0.5, 1.0, 0.0, 0.0, 1.0, 1.0
            ]
vertices = numpy.array(vertices, dtype=numpy.float32)

indices = [0, 1, 2, 0, 2, 3,    # front
           5, 4, 7, 5, 7, 6,    # back         7b    6c
           3, 2, 7, 7, 2, 6,    # top       3m    2w
           2, 1, 5, 2, 5, 6,    # right
           1, 0, 5, 5, 0, 4,    # bottom       4k    5g
           3, 7, 4, 3, 4, 0     # left      0r    1y
           ]
indices = numpy.array(indices, dtype=numpy.uint32)


def create_object(shader):
    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

    # Generate buffers to hold buffer indices
    element_buffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)

    # Get the position of the 'position' in parameter of our shader and bind it.
    position = glGetAttribLocation(shader, 'position')
    glEnableVertexAttribArray(position)

    # Describe the position data layout in the buffer
    glVertexAttribPointer(position, 4, GL_FLOAT, False, 32, ctypes.c_void_p(0))

    # Get the position of the 'colour' in parameter of our shader and bind it.
    colour = glGetAttribLocation(shader, 'colour')
    glEnableVertexAttribArray(colour)

    # Describe the colour data layout in the buffer
    glVertexAttribPointer(colour, 4, GL_FLOAT, False, 32, ctypes.c_void_p(16))

    # Send the data over to the buffers
    glBufferData(GL_ARRAY_BUFFER, 256, vertices, GL_STATIC_DRAW)         # Vertices array
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 144, indices, GL_STATIC_DRAW)  # Indices array

    # Unbind the VAO first (Important)
    glBindVertexArray(0)

    # Unbind other stuff
    glDisableVertexAttribArray(position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return vertex_array_object


def display(shader, vertex_array_object):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(shader)
    rot_x = pyrr.matrix44.create_from_x_rotation(0.5 * pygame.time.get_ticks() / 1000, dtype=numpy.float32)
    rot_y = pyrr.matrix44.create_from_y_rotation(0.8 * pygame.time.get_ticks() / 1000, dtype=numpy.float32)
    transform_location = glGetUniformLocation(shader, 'transformation')
    glUniformMatrix4fv(transform_location, 1, GL_FALSE, rot_x @ rot_y)

    glBindVertexArray(vertex_array_object)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

    glBindVertexArray(0)
    glUseProgram(0)


def main():
    display_width = 512
    display_height = 512
    pygame.init()
    pygame.display.set_mode((display_width, display_height), pygame.OPENGL | pygame.DOUBLEBUF)
    glClearColor(0.0, 0.0, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

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
