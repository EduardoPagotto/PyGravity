#version 330
in vec2 aPosition;
void main ()
{
    gl_Position = vec4(aPosition, 0.5, 1);
}