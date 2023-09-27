# -*- coding: utf-8 -*-

#----------------------------------
from OpenGL.GL import *
from OpenGL.GL import shaders

#----------------------------------

#----------------------------------

def load_shader(shader_file):
    shader_source = ""
    with open(shader_file) as f:
        shader_source = f.read()
    f.close()
    return str.encode(shader_source)

def compile_shader(vertex_shader, fragment_shader):
    vert_shader = load_shader(vertex_shader)
    frag_shader = load_shader(fragment_shader)
    
    shader_program = shaders.compileProgram(
            shaders.compileShader(vert_shader, GL_VERTEX_SHADER),
            shaders.compileShader(frag_shader, GL_FRAGMENT_SHADER))
    return shader_program


