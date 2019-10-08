#version 130
in vec2 outTexCoords;  // needs to have the same name as the output from vertex shader
out vec4 outColour;
uniform sampler2D samplerTex;

void main()
{
   outColour = texture(samplerTex, outTexCoords);
}
