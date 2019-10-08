from OpenGL.GL import *
import OpenGL.GL.shaders
import ctypes
import pygame
import numpy
from PIL import Image


vertex_shader = """
#version 130
in vec4 position;
in vec4 colour;
in vec2 inTexCoords;
out vec4 newColour;
out vec2 outTexCoords;

void main()
{
   gl_Position = position;
   newColour = colour;
   outTexCoords = inTexCoords;
}
"""

fragment_shader = """
#version 130
in vec4 newColour;     // needs to have the same name as the output from vertex shader
in vec2 outTexCoords;  // needs to have the same name as the output from vertex shader
out vec4 outColour;
uniform sampler2D samplerTex;

void main()
{
   //gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
   //outColour = newColour;
   outColour = texture(samplerTex, outTexCoords);
}
"""

vertices = [-0.5, -0.5, 0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0,
            0.5, 0.5, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 1.0,
            -0.5, 0.5, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0]
vertices = numpy.array(vertices, dtype=numpy.float32)

indices = [0, 1, 2,
           0, 2, 3]
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

    # Generate buffers to hold our texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Set the position of the 'position' in parameter of our shader and bind it.
    position = 0
    glBindAttribLocation(shader, position, 'position')
    glEnableVertexAttribArray(position)
    # Describe the position data layout in the buffer
    glVertexAttribPointer(position, 4, GL_FLOAT, False, 40, ctypes.c_void_p(0))

    # Set the position of the 'colour' in parameter of our shader and bind it.
    colour = 1
    glBindAttribLocation(shader, colour, 'colour')
    glEnableVertexAttribArray(colour)
    # Describe the position data layout in the buffer
    glVertexAttribPointer(colour, 4, GL_FLOAT, False, 40, ctypes.c_void_p(16))

    # Texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # Load and convert Texture
    image = Image.open('res/crate.jpg')
    img_data = numpy.array(list(image.getdata()), numpy.uint8)

    # Set the position of the 'inTexCoords' in parameter of our shader and bind it.
    texture_coords = 2
    glBindAttribLocation(shader, texture_coords, 'inTexCoords')
    glEnableVertexAttribArray(texture_coords)
    # Describe the texture data layout in the buffer
    glVertexAttribPointer(texture_coords, 2, GL_FLOAT, False, 40, ctypes.c_void_p(32))

    # Send the data over to the buffers
    glBufferData(GL_ARRAY_BUFFER, 160, vertices, GL_STATIC_DRAW)         # Vertices array
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, 24, indices, GL_STATIC_DRAW)  # Indices array
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 512, 512, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Unbind the VAO first (Important)
    glBindVertexArray(0)

    # Unbind other stuff
    glDisableVertexAttribArray(position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

    return vertex_array_object


def display(shader, vertex_array_object):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glBindVertexArray(vertex_array_object)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)  # Replaces glDrawArrays because we're drawing indices now.
    glBindVertexArray(0)


def main():
    pygame.init()
    pygame.display.set_mode((512, 512), pygame.OPENGL | pygame.DOUBLEBUF)
    glClearColor(0.0, 0.0, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)

    shader = OpenGL.GL.shaders.compileProgram(
        OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
        OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    vertex_array_object = create_object(shader)
    glUseProgram(shader)

    clock = pygame.time.Clock()
    looping = True

    while looping:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                looping = False

        display(shader, vertex_array_object)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
        pygame.display.flip()

    glUseProgram(0)


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
