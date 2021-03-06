from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
from pathlib import Path
import ctypes
import pygame
import numpy
import pyrr
from PIL import Image
from ShaderLoader import compile_shader
from ObjLoader import ObjLoader


def init_gl():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.1, 1.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glDepthFunc(GL_LEQUAL)


def window_resize(width, height):
    # pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
    # glViewport(0, 0, width, height)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def create_object(shader):
    obj = ObjLoader()
    obj.load_model(Path('res', 'cube.obj'))
    texture_offset = len(obj.vertex_index) * len(obj.vert_coords[0]) * obj.model.itemsize
    normal_offset = texture_offset + len(obj.texture_index) * len(obj.text_coords[0]) * obj.model.itemsize

    # Create a new VAO (Vertex Array Object) and bind it
    vertex_array_object = glGenVertexArrays(1)
    glBindVertexArray(vertex_array_object)

    # Generate buffers to hold our vertices
    vertex_buffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

    # Generate buffers to hold our texture
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Set the position of the 'position' in parameter of our shader and bind it.
    position = 0
    glBindAttribLocation(shader, position, 'position')
    glEnableVertexAttribArray(position)
    # Describe the position data layout in the buffer
    glVertexAttribPointer(position, 3, GL_FLOAT, False, obj.model.itemsize * 3, ctypes.c_void_p(0))

    # Set the position of the 'inTexCoords' in parameter of our shader and bind it.
    texture_coords = 1
    glBindAttribLocation(shader, texture_coords, 'inTexCoords')
    glEnableVertexAttribArray(texture_coords)
    # Describe the texture data layout in the buffer
    glVertexAttribPointer(texture_coords, 2, GL_FLOAT, False, obj.model.itemsize * 2, ctypes.c_void_p(texture_offset))

    # Set the position of the 'inTexCoords' in parameter of our shader and bind it.
    normals = 2
    glBindAttribLocation(shader, normals, 'inNormals')
    glEnableVertexAttribArray(normals)
    # Describe the texture data layout in the buffer
    glVertexAttribPointer(normals, 3, GL_FLOAT, False, obj.model.itemsize * 3, ctypes.c_void_p(normal_offset))

    # Texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # Load and convert Texture
    image = Image.open(Path('res', 'cube_texture.jpg'))
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = numpy.array(list(flipped_image.getdata()), numpy.uint8)

    # Send the data over to the buffers
    glBufferData(GL_ARRAY_BUFFER, obj.model.itemsize * len(obj.model), obj.model, GL_STATIC_DRAW)    # Vertices array
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

    # Unbind the VAO first (Important)
    glBindVertexArray(0)

    # Unbind other stuff
    glDisableVertexAttribArray(position)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return vertex_array_object, obj


def display(shader, vertex_array_object, aspect_ratio, obj):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.matrix44.create_from_x_rotation(0.5 * pygame.time.get_ticks() / 1000, dtype=numpy.float32)
    rot_y = pyrr.matrix44.create_from_y_rotation(0.8 * pygame.time.get_ticks() / 1000, dtype=numpy.float32)
    rot_z = pyrr.matrix44.create_from_y_rotation(0.2 * pygame.time.get_ticks() / 1000, dtype=numpy.float32)
    view = pyrr.matrix44.create_from_translation(pyrr.Vector3([0.0, -0.5, -6.0]))
    projection = pyrr.matrix44.create_perspective_projection_matrix(45.0, aspect_ratio, 0.1, 100.0)
    vp = pyrr.matrix44.multiply(view, projection)
    cube_positions = [(1.0, 0.0, 0.0), (2.0, 5.0, -15.0), (-1.5, -1.2, -2.5), (-8.8, -2.0, -12.3),
                      (-2.0, 2.0, -5.5), (-4.0, 2.0, -3.0)]

    # transform_location = glGetUniformLocation(shader, 'transformation')
    model_loc = glGetUniformLocation(shader, 'model')
    vp_loc = glGetUniformLocation(shader, 'vp')
    light_loc = glGetUniformLocation(shader, 'lightPosition')

    # glUniformMatrix4fv(transform_location, 1, GL_FALSE, rot_x @ rot_y)
    glUniformMatrix4fv(vp_loc, 1, GL_FALSE, vp)
    glUniformMatrix4fv(light_loc, 1, GL_FALSE, rot_x @ rot_y)

    glBindVertexArray(vertex_array_object)

    for cube_position in cube_positions:
        model = pyrr.matrix44.create_from_translation(pyrr.Vector3(cube_position))

        if cube_positions.index(cube_position) < 2:
            model = pyrr.matrix44.multiply(rot_x, model)
        elif cube_positions.index(cube_position) < 4:
            model = pyrr.matrix44.multiply(rot_y, model)
        else:
            model = pyrr.matrix44.multiply(rot_z, model)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        # glDrawElements(GL_TRIANGLES, len(obj.vertex_index), GL_UNSIGNED_INT, None)
        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertex_index))

    glBindVertexArray(0)


def main():
    window_width = 1024
    window_height = 512

    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)
    window_resize(window_width, window_height)
    init_gl()

    shader = compile_shader(Path('shaders', 'multi_cube_vertex.glsl'),
                            Path('shaders', 'multi_cube_fragment.glsl'))

    vertex_array_object, obj = create_object(shader)
    glUseProgram(shader)

    clock = pygame.time.Clock()
    looping = True

    while looping:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                looping = False
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.size
                window_resize(window_width, window_height)
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                looping = False

        display(shader, vertex_array_object, window_width / window_height, obj)
        pygame.display.set_caption("FPS: %.2f" % clock.get_fps())
        pygame.display.flip()

    glUseProgram(0)


if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
