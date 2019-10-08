#version 130
in vec3 position;
in vec2 inTexCoords;
in vec3 inNormals;

uniform mat4 transformation;
uniform mat4 mvp;
uniform mat4 lightPosition;

out vec2 outTexCoords;
out vec3 fragNormals;

void main()
{
   gl_Position = mvp * transformation * vec4(position, 1.0);
   outTexCoords = inTexCoords;
   fragNormals = (lightPosition * vec4(inNormals, 0.0f)).xyz;
}
