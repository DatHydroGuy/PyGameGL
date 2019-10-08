#version 130
in vec3 position;
in vec2 inTexCoords;
uniform mat4 transformation;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 outTexCoords;

void main()
{
   gl_Position = projection * view * model * transformation * vec4(position, 1.0);
   outTexCoords = inTexCoords;
}
