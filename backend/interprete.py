import ply.lex as lex
import ply.yacc as yacc
from comandos.comando_mkdisk import Mkdisk
from comandos.comando_execute import Execute
from comandos.comando_rep import Rep
from comandos.comando_fdisk import Fdisk
from comandos.comando_rmdisk import Rmdisk
from comandos.comando_mount import Mount
from comandos.comando_mount_list import MountList
from comandos.comando_unmount import Unmount
from comandos.comando_mkfs import Mkfs
from comandos.comando_pause import Pausa
from comandos.comando_login import Login
from comandos.comando_logout import Logout
from comandos.comando_mkgrp import Mkgrp
from comandos.comando_rmgrp import Rmgrp
from comandos.comando_mkusr import Mkusr
from comandos.comando_rmusr import Rmusr
from comandos.comando_mkfile import Mkfile
from comandos.comando_cat import Cat
from comandos.comando_mkdir import Mkdir
from comandos.comando_remove import Remove
from comandos.comando_edit import Edit
from comandos.comando_rename import Rename
from comandos.comando_vacio import Vacio
#-------------------------------ANALIZADOR LEXICO---------------------------------------------------------------------
#errores_lexicos = []
error = ""

palabras_reservadas = {
    'execute': 'EXECUTE',
    'mkdisk': 'MKDISK',
    'rmdisk' : 'RMDISK',
    'fdisk' : 'FDISK',
    'rep': 'REP',
    'mount': 'MOUNT',
    'mountlist': 'MOUNT_LIST',
    'unmount' : 'UNMOUNT',
    'mkfs' : 'MKFS',
    'pause': 'PAUSE',
    'login' : 'LOGIN',
    'mkgrp' : 'MKGRP',
    'rmgrp' : 'RMGRP',
    'mkusr' : 'MKUSR',
    'rmusr' : 'RMUSR',
    'mkfile' : 'MKFILE',
    'mkdir' : 'MKDIR',
    'cat' : 'CAT',
    'remove' : 'REMOVE',
    'edit': 'EDIT',
    'rename' : 'RENAME',
    'copy' : 'COPY',
    'move' : 'MOVE',
    'find' : 'FIND',
    'path': 'PATH',
    'size': 'SIZE',
    'unit' : 'UNIT',
    'name' : 'NAME',
    'fit' : 'FIT',
    'type' : 'TYPE',
    'delete' : 'DELETE',
    'add' : 'ADD',
    'id' : 'ID_WORD',
    'fs' : 'FS',
    'user' : 'USER',
    'pass': 'PASS',
    'logout': 'LOGOUT',
    'grp' : 'GRP',
    'r' : 'R',
    'cont' : 'CONT',
    'ruta' : 'RUTA'
}

tokens = [
    'ENTERO',
    'ID',
    'CADENA_FILE_PATH',
    'IGUAL',
    'GUION',
    'FILE_PATH',
    'ID_PAR',
    '2FS',
    '3FS',
    'CADENA_DIR_PATH',
    'DIR_PATH',
    'NAME_2',
    'CADENA_SIMPLE'

] + list(palabras_reservadas.values())

def t_COMMENT(t):
    r'\#.*'
    #print(t.value)
    # No hacer nada en la acción para ignorar el comentario
    pass

t_IGUAL = r'\='
t_GUION = r'\-'
#t_2FS = r'2fs'
#t_3FS = r'3fs'

def t_2FS(t):
    r'2fs'
    return t

def t_3FS(t):
    r'3fs'
    return t

def t_ID_PAR(t):
    r'35[a-zA-z0-9_]+'
    return t

def t_NAME_2(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*\.[a-zA-Z0-9]+'
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_ID(t): # puede ser una letra o un nombre
    r'[a-zA-Z_][a-zA-z0-9_]*'
    c = t.value
    t.type = palabras_reservadas.get(c.lower(), 'ID')
    return t

def t_CADENA_FILE_PATH(t):
    r'"\.?(/[^/"]+)*(/[a-zA-Z0-9_][a-zA-Z0-9_\- ]*\.[a-zA-Z0-9]+)"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_FILE_PATH(t):
    r'\.?(/[a-z-A-Z_][a-zA-Z0-9_]*)*(/[a-zA-Z0-9_][a-zA-Z0-9_\-]*\.[a-zA-Z0-9]+)'
    return t

def t_CADENA_DIR_PATH(t):
    r'"\.?(/[^/]*)+"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_CADENA_SIMPLE(t):
    r'"[a-zA-Z_][a-zA-z0-9_ ]*"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t

def t_DIR_PATH(t):
    r'\.?(/[a-z-A-Z_][a-zA-Z0-9_]*)+'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# caracteres ignorados
t_ignore = ' \t'

def t_error(t):
    global error
    error = f'Error: Caracter no reconocido, {t.value[0]}\n' # {t.lexer.lineno}
    t.lexer.skip(1)

#-------------------------------ANALIZADOR SINTACTICO---------------------------------------------------------------------
def p_comandos(t):
    '''comandos : comando_mkdisk
                | comando_execute
                | comando_rep
                | empty_production
                | comando_fdisk
                | comando_rmdisk
                | comando_mount
                | comando_mountlist
                | comando_unmount
                | comando_mkfs
                | comando_pause
                | comando_login
                | comando_logout
                | comando_mkgrp
                | comando_rmgrp
                | comando_rmusr
                | comando_mkusr
                | comando_mkfile
                | comando_cat
                | comando_mkdir
                | comando_remove
                | comando_edit
                | comando_rename'''
    t[0] = t[1]

def p_empty_production(t):
    '''
    empty_production : 
    '''
    t[0] = Vacio()

#-------comando mkdisk---------
def p_comando_mkdisk(t):
    'comando_mkdisk : MKDISK lista_mkdisk'
    # t[0] : t[1] t[2] t[3]
    t[0] = Mkdisk(t[2])

def p_lista_mkdisk(t):
    '''lista_mkdisk : lista_mkdisk parametros_mkdisk
                | parametros_mkdisk'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_mkdisk(t):
    '''parametros_mkdisk : param_size
                | param_unit
                | param_path
                | param_fit'''
    t[0] = t[1]

#-------comando rmdisk---------
def p_comando_rmdisk(t):
    'comando_rmdisk : RMDISK lista_rmdisk'
    # t[0] : t[1] t[2] t[3]
    t[0] = Rmdisk(t[2])

def p_lista_rmdisk(t):
    '''lista_rmdisk : lista_rmdisk parametros_rmdisk
                | parametros_rmdisk'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_rmdisk(t):
    '''parametros_rmdisk : param_path'''
    t[0] = t[1]

#------------comando execute----------
def p_comando_execute(t):
    'comando_execute : EXECUTE lista_execute'
    # se manda el parser para ejecutar todos los comandos del archivo
    lexer2 = lex.lex()
    parser2 = yacc.yacc()
    t[0] = Execute(t[2], lexer2, parser2)

def p_lista_execute(t):
    '''lista_execute : lista_execute parametros_execute
                | parametros_execute'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_execute(t):
    '''parametros_execute : param_path'''
    t[0] = t[1]

#------------comando mount----------
def p_comando_mount(t):
    'comando_mount : MOUNT lista_mount'
    t[0] = Mount(t[2])

def p_lista_mount(t):
    '''lista_mount : lista_mount parametros_mount
                | parametros_mount'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_mount(t):
    '''parametros_mount : param_path
                | param_name'''
    t[0] = t[1]

#-------comando rep---------
def p_comando_rep(t):
    'comando_rep : REP lista_rep'
    t[0] = Rep(t[2])

def p_lista_rep(t):
    '''lista_rep : lista_rep parametros_rep
                | parametros_rep'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_rep(t):
    '''parametros_rep : param_path
                | param_name
                | param_id
                | param_ruta
                | param_ruta2'''
    t[0] = t[1]

#------------comando fdisk----------
def p_comando_fdisk(t):
    'comando_fdisk : FDISK lista_fdisk'
    t[0] = Fdisk(t[2])

def p_lista_fdisk(t):
    '''lista_fdisk : lista_fdisk parametros_fdisk
                | parametros_fdisk'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_fdisk(t):
    '''parametros_fdisk : param_size
                | param_path
                | param_name
                | param_unit
                | param_type
                | param_fit
                | param_delete
                | param_add'''
    t[0] = t[1]

#-------comando mount list---------
def p_comando_mountlist(t):
    'comando_mountlist : MOUNT_LIST'
    t[0] = MountList()

#------------comando unmount----------
def p_comando_unmount(t):
    'comando_unmount : UNMOUNT lista_unmount'
    t[0] = Unmount(t[2])

def p_lista_unmount(t):
    '''lista_unmount : lista_unmount parametros_unmount
                | parametros_unmount'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_unmount(t):
    '''parametros_unmount : param_id'''
    t[0] = t[1]

#------------comando mkfs----------
def p_comando_mkfs(t):
    'comando_mkfs : MKFS lista_mkfs'
    t[0] = Mkfs(t[2])

def p_lista_mkfs(t):
    '''lista_mkfs : lista_mkfs parametros_mkfs
                | parametros_mkfs'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_mkfs(t):
    '''parametros_mkfs : param_id
                | param_type
                | param_fs'''
    t[0] = t[1]

#-------comando pause---------
def p_comando_pause(t):
    'comando_pause : PAUSE'
    t[0] = Pausa()

#------------comando login----------
def p_comando_login(t):
    'comando_login : LOGIN lista_login'
    t[0] = Login(t[2])

def p_lista_login(t):
    '''lista_login : lista_login parametros_login
                | parametros_login'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_login(t):
    '''parametros_login : param_id
                | param_user
                | param_pass'''
    t[0] = t[1]

#-------comando logout---------
def p_comando_logout(t):
    'comando_logout : LOGOUT'
    t[0] = Logout()

#------------comando mkgrp----------
def p_comando_mkgrp(t):
    'comando_mkgrp : MKGRP lista_mkgrp'
    t[0] = Mkgrp(t[2])

def p_lista_mkgrp(t):
    '''lista_mkgrp : lista_mkgrp parametros_mkgrp
                | parametros_mkgrp'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_mkgrp(t):
    '''parametros_mkgrp : param_name
                        | param_name__cadena'''
    t[0] = t[1]

#------------comando rmgrp----------
def p_comando_rmgrp(t):
    'comando_rmgrp : RMGRP lista_rmgrp'
    t[0] = Rmgrp(t[2])

def p_lista_rmgrp(t):
    '''lista_rmgrp : lista_rmgrp parametros_rmgrp
                | parametros_rmgrp'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_rmgrp(t):
    '''parametros_rmgrp : param_name
                        | param_name__cadena'''
    t[0] = t[1]

#------------comando mkusr----------
def p_comando_mkusr(t):
    'comando_mkusr : MKUSR lista_mkusr'
    t[0] = Mkusr(t[2])

def p_lista_mkusr(t):
    '''lista_mkusr : lista_mkusr parametros_mkusr
                | parametros_mkusr'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_mkusr(t):
    '''parametros_mkusr : param_user
                        | param_grp
                        | param_pass'''
    t[0] = t[1]

#------------comando rmusr----------
def p_comando_rmusr(t):
    'comando_rmusr : RMUSR lista_rmusr'
    t[0] = Rmusr(t[2])

def p_lista_rmusr(t):
    '''lista_rmusr : lista_rmusr parametros_rmusr
                | parametros_rmusr'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_rmusr(t):
    '''parametros_rmusr : param_user'''
    t[0] = t[1]

#------------comando mkfile----------
def p_comando_mkfile(t):
    'comando_mkfile : MKFILE lista_mkfile'
    t[0] = Mkfile(t[2])

def p_lista_mkfile(t):
    '''lista_mkfile : lista_mkfile parametros_mkfile
                | parametros_mkfile'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_mkfile(t):
    '''parametros_mkfile : param_path
                        | param_size
                        | param_cont
                        | param_r'''
    t[0] = t[1]

#------------comando cat----------
def p_comando_cat(t):
    'comando_cat : CAT lista_cat'
    t[0] = Cat(t[2])

def p_lista_cat(t):
    '''lista_cat : lista_cat parametros_cat
                | parametros_cat'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_cat(t):
    '''parametros_cat : param_filen'''
    t[0] = t[1]

#------------comando mkdir----------
def p_comando_mkdir(t):
    'comando_mkdir : MKDIR lista_mkdir'
    t[0] = Mkdir(t[2])

def p_lista_mkdir(t):
    '''lista_mkdir : lista_mkdir parametros_mkdir
                | parametros_mkdir'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_mkdir(t):
    '''parametros_mkdir : param_path2
                        | param_r'''
    t[0] = t[1]

#------------comando remove----------
def p_comando_remove(t):
    'comando_remove : REMOVE lista_remove'
    t[0] = Remove(t[2])

def p_lista_remove(t):
    '''lista_remove : lista_remove parametros_remove
                | parametros_remove'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_remove(t):
    '''parametros_remove : param_path
                        | param_path2'''
    t[0] = t[1]

#------------comando edit----------
def p_comando_edit(t):
    'comando_edit : EDIT lista_edit'
    t[0] = Edit(t[2])

def p_lista_edit(t):
    '''lista_edit : lista_edit parametros_edit
                | parametros_edit'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_edit(t):
    '''parametros_edit : param_path
                    | param_cont'''
    t[0] = t[1]

#------------comando rename----------
def p_comando_rename(t):
    'comando_rename : RENAME lista_rename'
    t[0] = Rename(t[2])

def p_lista_rename(t):
    '''lista_rename : lista_rename parametros_rename
                | parametros_rename'''
    if len(t) != 2:
        t[1].update(t[2])
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_parametros_rename(t):
    '''parametros_rename : param_name_2
                    | param_name
                    | param_path
                    | param_path2'''
    t[0] = t[1]

#-----------------------------Parametros-----------------------------------------------
def p_param_size(t):
    'param_size : GUION SIZE IGUAL ENTERO'
    t[0] = {'size': t[4]}

def p_param_path(t):
    '''param_path : GUION PATH IGUAL CADENA_FILE_PATH
                |  GUION PATH IGUAL FILE_PATH'''
    t[0] = {'path': t[4]}

def p_param_unit(t):
    '''param_unit : GUION UNIT IGUAL ID'''
    t[0] = {'unit': t[4]}

def p_param_name(t):
    '''param_name : GUION NAME IGUAL ID'''
    t[0] = {'name': t[4]}

def p_param_fit(t):
    '''param_fit : GUION FIT IGUAL ID'''
    t[0] = {'fit': t[4]}

def p_param_type(t):
    '''param_type : GUION TYPE IGUAL ID'''
    t[0] = {'type': t[4]}

def p_param_delete(t):
    '''param_delete : GUION DELETE IGUAL ID'''
    t[0] = {'delete': t[4]}

def p_param_add(t):
    '''param_add : GUION ADD IGUAL ENTERO
                | GUION ADD IGUAL entero_negativo'''
    t[0] = {'add': t[4]}

def p_param_id(t):
    '''param_id : GUION ID_WORD IGUAL ID_PAR'''
    t[0] = {'id': t[4]}

def p_param_fs(t):
    '''param_fs : GUION FS IGUAL 2FS
                | GUION FS IGUAL 3FS'''
    t[0] = {'fs': t[4]}

def p_param_user(t):
    '''param_user : GUION USER IGUAL ID
                    | GUION USER IGUAL CADENA_SIMPLE'''
    t[0] = {'user': t[4]}

def p_param_pass(t):
    '''param_pass : GUION PASS IGUAL ID
                  | GUION PASS IGUAL ENTERO'''
    t[0] = {'pass': t[4]}

def p_param_grp(t):
    '''param_grp : GUION GRP IGUAL ID
                | GUION GRP IGUAL CADENA_SIMPLE'''
    t[0] = {'grp': t[4]}

def p_param_r(t):
    '''param_r : GUION R'''
    t[0] = {'r': True}

def p_param_cont(t):
    '''param_cont : GUION CONT IGUAL CADENA_FILE_PATH
                |  GUION CONT IGUAL FILE_PATH'''
    t[0] = {'cont': t[4]}

def p_param_filen(t):
    '''param_filen : GUION ID IGUAL CADENA_FILE_PATH
                    | GUION ID IGUAL FILE_PATH'''
    t[0] = {t[2]: t[4]}

def p_param_path2(t):
    '''param_path2 : GUION PATH IGUAL CADENA_DIR_PATH
                |  GUION PATH IGUAL DIR_PATH'''
    t[0] = {'path': t[4]}

def p_param_name_2(t):
    '''param_name_2 : GUION NAME IGUAL NAME_2'''
    t[0] = {'name': t[4]}

def p_param_ruta(t):
    '''param_ruta : GUION RUTA IGUAL CADENA_FILE_PATH
                |  GUION RUTA IGUAL FILE_PATH'''
    t[0] = {'ruta': t[4]}

def p_param_ruta2(t):
    '''param_ruta2 : GUION RUTA IGUAL CADENA_DIR_PATH
                |  GUION RUTA IGUAL DIR_PATH'''
    t[0] = {'ruta': t[4]}
    
def p_param_name__cadena(t):
    '''param_name__cadena : GUION NAME IGUAL CADENA_SIMPLE'''
    t[0] = {'name': t[4]}

# gramaticas extra

def p_entero_negativo(t):
    'entero_negativo : GUION ENTERO %prec GUION'
    t[0] = -t[2]

# Definición de precedencia
precedence = (
    ('left', 'GUION'),
)

# Regla de manejo de errores
def p_error(p):
    global error
    if p:
        error = f"Error: token no esperado '{p.value}'\n" # {p.lineno} {p.lexpos}
    else:
        error = "Error: sintaxis incorrecta\n"

lexer = lex.lex()

# llevarla al main
def parse(input):
    global parser
    parser = yacc.yacc()
    lexer.lineno = 1
    return parser.parse(input)

def errores():
    global error
    valor = error
    error = ""
    return valor