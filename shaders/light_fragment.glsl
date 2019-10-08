#version 130
in vec2 outTexCoords;  // needs to have the same name as the output from vertex shader
in vec3 fragNormals;
out vec4 outColour;
uniform sampler2D samplerTex;

void main()
{
   vec3 ambientLightIntensity = vec3(0.3f, 0.2f, 0.4f);
   vec3 sunlightIntensity = vec3(0.9f, 0.9f, 0.9f);
   vec3 sunlightPosition = normalize(vec3(2.0f, 1.0f, 0.5f));
   vec3 lightIntensity = ambientLightIntensity + sunlightIntensity * max(dot(fragNormals, sunlightPosition), 0.0f);

   vec4 texel = texture(samplerTex, outTexCoords);
   outColour = vec4(texel.rgb * lightIntensity, texel.a);
}
