
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftGUION2FS 3FS ADD CADENA_DIR_PATH CADENA_FILE_PATH CADENA_SIMPLE CAT CONT COPY DELETE DIR_PATH EDIT ENTERO EXECUTE FDISK FILE_PATH FIND FIT FS GRP GUION ID ID_PAR ID_WORD IGUAL LOGIN LOGOUT MKDIR MKDISK MKFILE MKFS MKGRP MKUSR MOUNT MOUNT_LIST MOVE NAME NAME_2 PASS PATH PAUSE R REMOVE RENAME REP RMDISK RMGRP RMUSR RUTA SIZE TYPE UNIT UNMOUNT USERcomandos : comando_mkdisk\n                | comando_execute\n                | comando_rep\n                | empty_production\n                | comando_fdisk\n                | comando_rmdisk\n                | comando_mount\n                | comando_mountlist\n                | comando_unmount\n                | comando_mkfs\n                | comando_pause\n                | comando_login\n                | comando_logout\n                | comando_mkgrp\n                | comando_rmgrp\n                | comando_rmusr\n                | comando_mkusr\n                | comando_mkfile\n                | comando_cat\n                | comando_mkdir\n                | comando_remove\n                | comando_edit\n                | comando_rename\n    empty_production : \n    comando_mkdisk : MKDISK lista_mkdisklista_mkdisk : lista_mkdisk parametros_mkdisk\n                | parametros_mkdiskparametros_mkdisk : param_size\n                | param_unit\n                | param_path\n                | param_fitcomando_rmdisk : RMDISK lista_rmdisklista_rmdisk : lista_rmdisk parametros_rmdisk\n                | parametros_rmdiskparametros_rmdisk : param_pathcomando_execute : EXECUTE lista_executelista_execute : lista_execute parametros_execute\n                | parametros_executeparametros_execute : param_pathcomando_mount : MOUNT lista_mountlista_mount : lista_mount parametros_mount\n                | parametros_mountparametros_mount : param_path\n                | param_namecomando_rep : REP lista_replista_rep : lista_rep parametros_rep\n                | parametros_repparametros_rep : param_path\n                | param_name\n                | param_id\n                | param_ruta\n                | param_ruta2comando_fdisk : FDISK lista_fdisklista_fdisk : lista_fdisk parametros_fdisk\n                | parametros_fdiskparametros_fdisk : param_size\n                | param_path\n                | param_name\n                | param_unit\n                | param_type\n                | param_fit\n                | param_delete\n                | param_addcomando_mountlist : MOUNT_LISTcomando_unmount : UNMOUNT lista_unmountlista_unmount : lista_unmount parametros_unmount\n                | parametros_unmountparametros_unmount : param_idcomando_mkfs : MKFS lista_mkfslista_mkfs : lista_mkfs parametros_mkfs\n                | parametros_mkfsparametros_mkfs : param_id\n                | param_type\n                | param_fscomando_pause : PAUSEcomando_login : LOGIN lista_loginlista_login : lista_login parametros_login\n                | parametros_loginparametros_login : param_id\n                | param_user\n                | param_passcomando_logout : LOGOUTcomando_mkgrp : MKGRP lista_mkgrplista_mkgrp : lista_mkgrp parametros_mkgrp\n                | parametros_mkgrpparametros_mkgrp : param_name\n                        | param_name__cadenacomando_rmgrp : RMGRP lista_rmgrplista_rmgrp : lista_rmgrp parametros_rmgrp\n                | parametros_rmgrpparametros_rmgrp : param_name\n                        | param_name__cadenacomando_mkusr : MKUSR lista_mkusrlista_mkusr : lista_mkusr parametros_mkusr\n                | parametros_mkusrparametros_mkusr : param_user\n                        | param_grp\n                        | param_passcomando_rmusr : RMUSR lista_rmusrlista_rmusr : lista_rmusr parametros_rmusr\n                | parametros_rmusrparametros_rmusr : param_usercomando_mkfile : MKFILE lista_mkfilelista_mkfile : lista_mkfile parametros_mkfile\n                | parametros_mkfileparametros_mkfile : param_path\n                        | param_size\n                        | param_cont\n                        | param_rcomando_cat : CAT lista_catlista_cat : lista_cat parametros_cat\n                | parametros_catparametros_cat : param_filencomando_mkdir : MKDIR lista_mkdirlista_mkdir : lista_mkdir parametros_mkdir\n                | parametros_mkdirparametros_mkdir : param_path2\n                        | param_rcomando_remove : REMOVE lista_removelista_remove : lista_remove parametros_remove\n                | parametros_removeparametros_remove : param_path\n                        | param_path2comando_edit : EDIT lista_editlista_edit : lista_edit parametros_edit\n                | parametros_editparametros_edit : param_path\n                    | param_contcomando_rename : RENAME lista_renamelista_rename : lista_rename parametros_rename\n                | parametros_renameparametros_rename : param_name_2\n                    | param_name\n                    | param_path\n                    | param_path2param_size : GUION SIZE IGUAL ENTEROparam_path : GUION PATH IGUAL CADENA_FILE_PATH\n                |  GUION PATH IGUAL FILE_PATHparam_unit : GUION UNIT IGUAL IDparam_name : GUION NAME IGUAL IDparam_fit : GUION FIT IGUAL IDparam_type : GUION TYPE IGUAL IDparam_delete : GUION DELETE IGUAL IDparam_add : GUION ADD IGUAL ENTERO\n                | GUION ADD IGUAL entero_negativoparam_id : GUION ID_WORD IGUAL ID_PARparam_fs : GUION FS IGUAL 2FS\n                | GUION FS IGUAL 3FSparam_user : GUION USER IGUAL ID\n                    | GUION USER IGUAL CADENA_SIMPLEparam_pass : GUION PASS IGUAL ID\n                  | GUION PASS IGUAL ENTEROparam_grp : GUION GRP IGUAL ID\n                | GUION GRP IGUAL CADENA_SIMPLEparam_r : GUION Rparam_cont : GUION CONT IGUAL CADENA_FILE_PATH\n                |  GUION CONT IGUAL FILE_PATHparam_filen : GUION ID IGUAL CADENA_FILE_PATH\n                    | GUION ID IGUAL FILE_PATHparam_path2 : GUION PATH IGUAL CADENA_DIR_PATH\n                |  GUION PATH IGUAL DIR_PATHparam_name_2 : GUION NAME IGUAL NAME_2param_ruta : GUION RUTA IGUAL CADENA_FILE_PATH\n                |  GUION RUTA IGUAL FILE_PATHparam_ruta2 : GUION RUTA IGUAL CADENA_DIR_PATH\n                |  GUION RUTA IGUAL DIR_PATHparam_name__cadena : GUION NAME IGUAL CADENA_SIMPLEentero_negativo : GUION ENTERO %prec GUION'
    
_lr_action_items = {'MKDISK':([0,],[25,]),'EXECUTE':([0,],[26,]),'REP':([0,],[27,]),'$end':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,31,34,36,47,48,49,50,51,52,54,55,56,58,59,60,61,62,63,64,66,67,68,69,70,71,72,73,74,75,77,78,79,80,81,82,83,85,86,87,89,90,91,92,93,95,96,97,98,99,101,102,103,104,106,107,108,109,110,111,112,114,115,116,117,118,120,121,122,123,124,125,127,128,129,131,132,133,134,136,137,138,139,141,142,143,144,146,147,148,149,150,151,153,158,159,163,167,168,169,170,172,175,177,178,179,181,183,184,186,188,190,191,213,214,215,216,217,218,219,220,221,222,223,224,225,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,],[-24,0,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,-22,-23,-64,-75,-82,-25,-27,-28,-29,-30,-31,-36,-38,-39,-45,-47,-48,-49,-50,-51,-52,-53,-55,-56,-57,-58,-59,-60,-61,-62,-63,-32,-34,-35,-40,-42,-43,-44,-65,-67,-68,-69,-71,-72,-73,-74,-76,-78,-79,-80,-81,-83,-85,-86,-87,-88,-90,-91,-92,-99,-101,-102,-93,-95,-96,-97,-98,-103,-105,-106,-107,-108,-109,-110,-112,-113,-114,-116,-117,-118,-119,-121,-122,-123,-124,-126,-127,-128,-129,-131,-132,-133,-134,-135,-26,-37,-46,-54,-33,-41,-66,-70,-77,-84,-89,-100,-94,-104,-155,-111,-115,-120,-125,-130,-136,-139,-137,-138,-141,-140,-146,-163,-164,-165,-166,-142,-143,-144,-145,-147,-148,-149,-150,-151,-152,-167,-153,-154,-156,-157,-158,-159,-160,-161,-162,-168,]),'FDISK':([0,],[28,]),'RMDISK':([0,],[29,]),'MOUNT':([0,],[30,]),'MOUNT_LIST':([0,],[31,]),'UNMOUNT':([0,],[32,]),'MKFS':([0,],[33,]),'PAUSE':([0,],[34,]),'LOGIN':([0,],[35,]),'LOGOUT':([0,],[36,]),'MKGRP':([0,],[37,]),'RMGRP':([0,],[38,]),'RMUSR':([0,],[39,]),'MKUSR':([0,],[40,]),'MKFILE':([0,],[41,]),'CAT':([0,],[42,]),'MKDIR':([0,],[43,]),'REMOVE':([0,],[44,]),'EDIT':([0,],[45,]),'RENAME':([0,],[46,]),'GUION':([25,26,27,28,29,30,32,33,35,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,54,55,56,58,59,60,61,62,63,64,66,67,68,69,70,71,72,73,74,75,77,78,79,80,81,82,83,85,86,87,89,90,91,92,93,95,96,97,98,99,101,102,103,104,106,107,108,109,110,111,112,114,115,116,117,118,120,121,122,123,124,125,127,128,129,131,132,133,134,136,137,138,139,141,142,143,144,146,147,148,149,150,151,153,158,159,163,167,168,169,170,172,175,177,178,179,181,183,184,186,188,190,191,202,213,214,215,216,217,218,219,220,221,222,223,224,225,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,],[53,57,65,76,57,84,88,94,100,105,105,113,119,126,130,135,140,145,152,53,-27,-28,-29,-30,-31,57,-38,-39,65,-47,-48,-49,-50,-51,-52,76,-55,-56,-57,-58,-59,-60,-61,-62,-63,57,-34,-35,84,-42,-43,-44,88,-67,-68,94,-71,-72,-73,-74,100,-78,-79,-80,-81,105,-85,-86,-87,105,-90,-91,-92,113,-101,-102,119,-95,-96,-97,-98,126,-105,-106,-107,-108,-109,130,-112,-113,135,-116,-117,-118,140,-121,-122,-123,145,-126,-127,-128,152,-131,-132,-133,-134,-135,-26,-37,-46,-54,-33,-41,-66,-70,-77,-84,-89,-100,-94,-104,-155,-111,-115,-120,-125,-130,226,-136,-139,-137,-138,-141,-140,-146,-163,-164,-165,-166,-142,-143,-144,-145,-147,-148,-149,-150,-151,-152,-167,-153,-154,-156,-157,-158,-159,-160,-161,-162,-168,]),'SIZE':([53,76,126,],[154,154,154,]),'UNIT':([53,76,],[155,155,]),'PATH':([53,57,65,76,84,126,135,140,145,152,],[156,156,156,156,156,156,187,189,156,189,]),'FIT':([53,76,],[157,157,]),'NAME':([65,76,84,105,152,],[160,160,160,176,192,]),'ID_WORD':([65,88,94,100,],[161,161,161,161,]),'RUTA':([65,],[162,]),'TYPE':([76,94,],[164,164,]),'DELETE':([76,],[165,]),'ADD':([76,],[166,]),'FS':([94,],[171,]),'USER':([100,113,119,],[173,173,173,]),'PASS':([100,119,],[174,174,]),'GRP':([119,],[180,]),'CONT':([126,145,],[182,182,]),'R':([126,135,],[183,183,]),'ID':([130,194,196,197,200,201,204,205,206,207,212,],[185,214,217,218,224,225,231,233,218,236,218,]),'IGUAL':([154,155,156,157,160,161,162,164,165,166,171,173,174,176,180,182,185,187,189,192,],[193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,]),'ENTERO':([193,202,205,226,],[213,227,234,245,]),'CADENA_FILE_PATH':([195,199,208,209,211,],[215,220,238,240,215,]),'FILE_PATH':([195,199,208,209,211,],[216,221,239,241,216,]),'ID_PAR':([198,],[219,]),'CADENA_DIR_PATH':([199,210,211,],[222,242,242,]),'DIR_PATH':([199,210,211,],[223,243,243,]),'2FS':([203,],[229,]),'3FS':([203,],[230,]),'CADENA_SIMPLE':([204,206,207,],[232,235,237,]),'NAME_2':([212,],[244,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'comandos':([0,],[1,]),'comando_mkdisk':([0,],[2,]),'comando_execute':([0,],[3,]),'comando_rep':([0,],[4,]),'empty_production':([0,],[5,]),'comando_fdisk':([0,],[6,]),'comando_rmdisk':([0,],[7,]),'comando_mount':([0,],[8,]),'comando_mountlist':([0,],[9,]),'comando_unmount':([0,],[10,]),'comando_mkfs':([0,],[11,]),'comando_pause':([0,],[12,]),'comando_login':([0,],[13,]),'comando_logout':([0,],[14,]),'comando_mkgrp':([0,],[15,]),'comando_rmgrp':([0,],[16,]),'comando_rmusr':([0,],[17,]),'comando_mkusr':([0,],[18,]),'comando_mkfile':([0,],[19,]),'comando_cat':([0,],[20,]),'comando_mkdir':([0,],[21,]),'comando_remove':([0,],[22,]),'comando_edit':([0,],[23,]),'comando_rename':([0,],[24,]),'lista_mkdisk':([25,],[47,]),'parametros_mkdisk':([25,47,],[48,153,]),'param_size':([25,28,41,47,66,120,],[49,68,123,49,68,123,]),'param_unit':([25,28,47,66,],[50,71,50,71,]),'param_path':([25,26,27,28,29,30,41,44,45,46,47,54,58,66,77,80,120,136,141,146,],[51,56,60,69,79,82,122,138,143,150,51,56,60,69,79,82,122,138,143,150,]),'param_fit':([25,28,47,66,],[52,73,52,73,]),'lista_execute':([26,],[54,]),'parametros_execute':([26,54,],[55,158,]),'lista_rep':([27,],[58,]),'parametros_rep':([27,58,],[59,159,]),'param_name':([27,28,30,37,38,46,58,66,80,101,106,146,],[61,70,83,103,108,149,61,70,83,103,108,149,]),'param_id':([27,32,33,35,58,85,89,95,],[62,87,91,97,62,87,91,97,]),'param_ruta':([27,58,],[63,63,]),'param_ruta2':([27,58,],[64,64,]),'lista_fdisk':([28,],[66,]),'parametros_fdisk':([28,66,],[67,163,]),'param_type':([28,33,66,89,],[72,92,72,92,]),'param_delete':([28,66,],[74,74,]),'param_add':([28,66,],[75,75,]),'lista_rmdisk':([29,],[77,]),'parametros_rmdisk':([29,77,],[78,167,]),'lista_mount':([30,],[80,]),'parametros_mount':([30,80,],[81,168,]),'lista_unmount':([32,],[85,]),'parametros_unmount':([32,85,],[86,169,]),'lista_mkfs':([33,],[89,]),'parametros_mkfs':([33,89,],[90,170,]),'param_fs':([33,89,],[93,93,]),'lista_login':([35,],[95,]),'parametros_login':([35,95,],[96,172,]),'param_user':([35,39,40,95,110,114,],[98,112,116,98,112,116,]),'param_pass':([35,40,95,114,],[99,118,99,118,]),'lista_mkgrp':([37,],[101,]),'parametros_mkgrp':([37,101,],[102,175,]),'param_name__cadena':([37,38,101,106,],[104,109,104,109,]),'lista_rmgrp':([38,],[106,]),'parametros_rmgrp':([38,106,],[107,177,]),'lista_rmusr':([39,],[110,]),'parametros_rmusr':([39,110,],[111,178,]),'lista_mkusr':([40,],[114,]),'parametros_mkusr':([40,114,],[115,179,]),'param_grp':([40,114,],[117,117,]),'lista_mkfile':([41,],[120,]),'parametros_mkfile':([41,120,],[121,181,]),'param_cont':([41,45,120,141,],[124,144,124,144,]),'param_r':([41,43,120,131,],[125,134,125,134,]),'lista_cat':([42,],[127,]),'parametros_cat':([42,127,],[128,184,]),'param_filen':([42,127,],[129,129,]),'lista_mkdir':([43,],[131,]),'parametros_mkdir':([43,131,],[132,186,]),'param_path2':([43,44,46,131,136,146,],[133,139,151,133,139,151,]),'lista_remove':([44,],[136,]),'parametros_remove':([44,136,],[137,188,]),'lista_edit':([45,],[141,]),'parametros_edit':([45,141,],[142,190,]),'lista_rename':([46,],[146,]),'parametros_rename':([46,146,],[147,191,]),'param_name_2':([46,146,],[148,148,]),'entero_negativo':([202,],[228,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> comandos","S'",1,None,None,None),
  ('comandos -> comando_mkdisk','comandos',1,'p_comandos','interprete.py',168),
  ('comandos -> comando_execute','comandos',1,'p_comandos','interprete.py',169),
  ('comandos -> comando_rep','comandos',1,'p_comandos','interprete.py',170),
  ('comandos -> empty_production','comandos',1,'p_comandos','interprete.py',171),
  ('comandos -> comando_fdisk','comandos',1,'p_comandos','interprete.py',172),
  ('comandos -> comando_rmdisk','comandos',1,'p_comandos','interprete.py',173),
  ('comandos -> comando_mount','comandos',1,'p_comandos','interprete.py',174),
  ('comandos -> comando_mountlist','comandos',1,'p_comandos','interprete.py',175),
  ('comandos -> comando_unmount','comandos',1,'p_comandos','interprete.py',176),
  ('comandos -> comando_mkfs','comandos',1,'p_comandos','interprete.py',177),
  ('comandos -> comando_pause','comandos',1,'p_comandos','interprete.py',178),
  ('comandos -> comando_login','comandos',1,'p_comandos','interprete.py',179),
  ('comandos -> comando_logout','comandos',1,'p_comandos','interprete.py',180),
  ('comandos -> comando_mkgrp','comandos',1,'p_comandos','interprete.py',181),
  ('comandos -> comando_rmgrp','comandos',1,'p_comandos','interprete.py',182),
  ('comandos -> comando_rmusr','comandos',1,'p_comandos','interprete.py',183),
  ('comandos -> comando_mkusr','comandos',1,'p_comandos','interprete.py',184),
  ('comandos -> comando_mkfile','comandos',1,'p_comandos','interprete.py',185),
  ('comandos -> comando_cat','comandos',1,'p_comandos','interprete.py',186),
  ('comandos -> comando_mkdir','comandos',1,'p_comandos','interprete.py',187),
  ('comandos -> comando_remove','comandos',1,'p_comandos','interprete.py',188),
  ('comandos -> comando_edit','comandos',1,'p_comandos','interprete.py',189),
  ('comandos -> comando_rename','comandos',1,'p_comandos','interprete.py',190),
  ('empty_production -> <empty>','empty_production',0,'p_empty_production','interprete.py',195),
  ('comando_mkdisk -> MKDISK lista_mkdisk','comando_mkdisk',2,'p_comando_mkdisk','interprete.py',201),
  ('lista_mkdisk -> lista_mkdisk parametros_mkdisk','lista_mkdisk',2,'p_lista_mkdisk','interprete.py',206),
  ('lista_mkdisk -> parametros_mkdisk','lista_mkdisk',1,'p_lista_mkdisk','interprete.py',207),
  ('parametros_mkdisk -> param_size','parametros_mkdisk',1,'p_parametros_mkdisk','interprete.py',215),
  ('parametros_mkdisk -> param_unit','parametros_mkdisk',1,'p_parametros_mkdisk','interprete.py',216),
  ('parametros_mkdisk -> param_path','parametros_mkdisk',1,'p_parametros_mkdisk','interprete.py',217),
  ('parametros_mkdisk -> param_fit','parametros_mkdisk',1,'p_parametros_mkdisk','interprete.py',218),
  ('comando_rmdisk -> RMDISK lista_rmdisk','comando_rmdisk',2,'p_comando_rmdisk','interprete.py',223),
  ('lista_rmdisk -> lista_rmdisk parametros_rmdisk','lista_rmdisk',2,'p_lista_rmdisk','interprete.py',228),
  ('lista_rmdisk -> parametros_rmdisk','lista_rmdisk',1,'p_lista_rmdisk','interprete.py',229),
  ('parametros_rmdisk -> param_path','parametros_rmdisk',1,'p_parametros_rmdisk','interprete.py',237),
  ('comando_execute -> EXECUTE lista_execute','comando_execute',2,'p_comando_execute','interprete.py',242),
  ('lista_execute -> lista_execute parametros_execute','lista_execute',2,'p_lista_execute','interprete.py',249),
  ('lista_execute -> parametros_execute','lista_execute',1,'p_lista_execute','interprete.py',250),
  ('parametros_execute -> param_path','parametros_execute',1,'p_parametros_execute','interprete.py',258),
  ('comando_mount -> MOUNT lista_mount','comando_mount',2,'p_comando_mount','interprete.py',263),
  ('lista_mount -> lista_mount parametros_mount','lista_mount',2,'p_lista_mount','interprete.py',267),
  ('lista_mount -> parametros_mount','lista_mount',1,'p_lista_mount','interprete.py',268),
  ('parametros_mount -> param_path','parametros_mount',1,'p_parametros_mount','interprete.py',276),
  ('parametros_mount -> param_name','parametros_mount',1,'p_parametros_mount','interprete.py',277),
  ('comando_rep -> REP lista_rep','comando_rep',2,'p_comando_rep','interprete.py',282),
  ('lista_rep -> lista_rep parametros_rep','lista_rep',2,'p_lista_rep','interprete.py',286),
  ('lista_rep -> parametros_rep','lista_rep',1,'p_lista_rep','interprete.py',287),
  ('parametros_rep -> param_path','parametros_rep',1,'p_parametros_rep','interprete.py',295),
  ('parametros_rep -> param_name','parametros_rep',1,'p_parametros_rep','interprete.py',296),
  ('parametros_rep -> param_id','parametros_rep',1,'p_parametros_rep','interprete.py',297),
  ('parametros_rep -> param_ruta','parametros_rep',1,'p_parametros_rep','interprete.py',298),
  ('parametros_rep -> param_ruta2','parametros_rep',1,'p_parametros_rep','interprete.py',299),
  ('comando_fdisk -> FDISK lista_fdisk','comando_fdisk',2,'p_comando_fdisk','interprete.py',304),
  ('lista_fdisk -> lista_fdisk parametros_fdisk','lista_fdisk',2,'p_lista_fdisk','interprete.py',308),
  ('lista_fdisk -> parametros_fdisk','lista_fdisk',1,'p_lista_fdisk','interprete.py',309),
  ('parametros_fdisk -> param_size','parametros_fdisk',1,'p_parametros_fdisk','interprete.py',317),
  ('parametros_fdisk -> param_path','parametros_fdisk',1,'p_parametros_fdisk','interprete.py',318),
  ('parametros_fdisk -> param_name','parametros_fdisk',1,'p_parametros_fdisk','interprete.py',319),
  ('parametros_fdisk -> param_unit','parametros_fdisk',1,'p_parametros_fdisk','interprete.py',320),
  ('parametros_fdisk -> param_type','parametros_fdisk',1,'p_parametros_fdisk','interprete.py',321),
  ('parametros_fdisk -> param_fit','parametros_fdisk',1,'p_parametros_fdisk','interprete.py',322),
  ('parametros_fdisk -> param_delete','parametros_fdisk',1,'p_parametros_fdisk','interprete.py',323),
  ('parametros_fdisk -> param_add','parametros_fdisk',1,'p_parametros_fdisk','interprete.py',324),
  ('comando_mountlist -> MOUNT_LIST','comando_mountlist',1,'p_comando_mountlist','interprete.py',329),
  ('comando_unmount -> UNMOUNT lista_unmount','comando_unmount',2,'p_comando_unmount','interprete.py',334),
  ('lista_unmount -> lista_unmount parametros_unmount','lista_unmount',2,'p_lista_unmount','interprete.py',338),
  ('lista_unmount -> parametros_unmount','lista_unmount',1,'p_lista_unmount','interprete.py',339),
  ('parametros_unmount -> param_id','parametros_unmount',1,'p_parametros_unmount','interprete.py',347),
  ('comando_mkfs -> MKFS lista_mkfs','comando_mkfs',2,'p_comando_mkfs','interprete.py',352),
  ('lista_mkfs -> lista_mkfs parametros_mkfs','lista_mkfs',2,'p_lista_mkfs','interprete.py',356),
  ('lista_mkfs -> parametros_mkfs','lista_mkfs',1,'p_lista_mkfs','interprete.py',357),
  ('parametros_mkfs -> param_id','parametros_mkfs',1,'p_parametros_mkfs','interprete.py',365),
  ('parametros_mkfs -> param_type','parametros_mkfs',1,'p_parametros_mkfs','interprete.py',366),
  ('parametros_mkfs -> param_fs','parametros_mkfs',1,'p_parametros_mkfs','interprete.py',367),
  ('comando_pause -> PAUSE','comando_pause',1,'p_comando_pause','interprete.py',372),
  ('comando_login -> LOGIN lista_login','comando_login',2,'p_comando_login','interprete.py',377),
  ('lista_login -> lista_login parametros_login','lista_login',2,'p_lista_login','interprete.py',381),
  ('lista_login -> parametros_login','lista_login',1,'p_lista_login','interprete.py',382),
  ('parametros_login -> param_id','parametros_login',1,'p_parametros_login','interprete.py',390),
  ('parametros_login -> param_user','parametros_login',1,'p_parametros_login','interprete.py',391),
  ('parametros_login -> param_pass','parametros_login',1,'p_parametros_login','interprete.py',392),
  ('comando_logout -> LOGOUT','comando_logout',1,'p_comando_logout','interprete.py',397),
  ('comando_mkgrp -> MKGRP lista_mkgrp','comando_mkgrp',2,'p_comando_mkgrp','interprete.py',402),
  ('lista_mkgrp -> lista_mkgrp parametros_mkgrp','lista_mkgrp',2,'p_lista_mkgrp','interprete.py',406),
  ('lista_mkgrp -> parametros_mkgrp','lista_mkgrp',1,'p_lista_mkgrp','interprete.py',407),
  ('parametros_mkgrp -> param_name','parametros_mkgrp',1,'p_parametros_mkgrp','interprete.py',415),
  ('parametros_mkgrp -> param_name__cadena','parametros_mkgrp',1,'p_parametros_mkgrp','interprete.py',416),
  ('comando_rmgrp -> RMGRP lista_rmgrp','comando_rmgrp',2,'p_comando_rmgrp','interprete.py',421),
  ('lista_rmgrp -> lista_rmgrp parametros_rmgrp','lista_rmgrp',2,'p_lista_rmgrp','interprete.py',425),
  ('lista_rmgrp -> parametros_rmgrp','lista_rmgrp',1,'p_lista_rmgrp','interprete.py',426),
  ('parametros_rmgrp -> param_name','parametros_rmgrp',1,'p_parametros_rmgrp','interprete.py',434),
  ('parametros_rmgrp -> param_name__cadena','parametros_rmgrp',1,'p_parametros_rmgrp','interprete.py',435),
  ('comando_mkusr -> MKUSR lista_mkusr','comando_mkusr',2,'p_comando_mkusr','interprete.py',440),
  ('lista_mkusr -> lista_mkusr parametros_mkusr','lista_mkusr',2,'p_lista_mkusr','interprete.py',444),
  ('lista_mkusr -> parametros_mkusr','lista_mkusr',1,'p_lista_mkusr','interprete.py',445),
  ('parametros_mkusr -> param_user','parametros_mkusr',1,'p_parametros_mkusr','interprete.py',453),
  ('parametros_mkusr -> param_grp','parametros_mkusr',1,'p_parametros_mkusr','interprete.py',454),
  ('parametros_mkusr -> param_pass','parametros_mkusr',1,'p_parametros_mkusr','interprete.py',455),
  ('comando_rmusr -> RMUSR lista_rmusr','comando_rmusr',2,'p_comando_rmusr','interprete.py',460),
  ('lista_rmusr -> lista_rmusr parametros_rmusr','lista_rmusr',2,'p_lista_rmusr','interprete.py',464),
  ('lista_rmusr -> parametros_rmusr','lista_rmusr',1,'p_lista_rmusr','interprete.py',465),
  ('parametros_rmusr -> param_user','parametros_rmusr',1,'p_parametros_rmusr','interprete.py',473),
  ('comando_mkfile -> MKFILE lista_mkfile','comando_mkfile',2,'p_comando_mkfile','interprete.py',478),
  ('lista_mkfile -> lista_mkfile parametros_mkfile','lista_mkfile',2,'p_lista_mkfile','interprete.py',482),
  ('lista_mkfile -> parametros_mkfile','lista_mkfile',1,'p_lista_mkfile','interprete.py',483),
  ('parametros_mkfile -> param_path','parametros_mkfile',1,'p_parametros_mkfile','interprete.py',491),
  ('parametros_mkfile -> param_size','parametros_mkfile',1,'p_parametros_mkfile','interprete.py',492),
  ('parametros_mkfile -> param_cont','parametros_mkfile',1,'p_parametros_mkfile','interprete.py',493),
  ('parametros_mkfile -> param_r','parametros_mkfile',1,'p_parametros_mkfile','interprete.py',494),
  ('comando_cat -> CAT lista_cat','comando_cat',2,'p_comando_cat','interprete.py',499),
  ('lista_cat -> lista_cat parametros_cat','lista_cat',2,'p_lista_cat','interprete.py',503),
  ('lista_cat -> parametros_cat','lista_cat',1,'p_lista_cat','interprete.py',504),
  ('parametros_cat -> param_filen','parametros_cat',1,'p_parametros_cat','interprete.py',512),
  ('comando_mkdir -> MKDIR lista_mkdir','comando_mkdir',2,'p_comando_mkdir','interprete.py',517),
  ('lista_mkdir -> lista_mkdir parametros_mkdir','lista_mkdir',2,'p_lista_mkdir','interprete.py',521),
  ('lista_mkdir -> parametros_mkdir','lista_mkdir',1,'p_lista_mkdir','interprete.py',522),
  ('parametros_mkdir -> param_path2','parametros_mkdir',1,'p_parametros_mkdir','interprete.py',530),
  ('parametros_mkdir -> param_r','parametros_mkdir',1,'p_parametros_mkdir','interprete.py',531),
  ('comando_remove -> REMOVE lista_remove','comando_remove',2,'p_comando_remove','interprete.py',536),
  ('lista_remove -> lista_remove parametros_remove','lista_remove',2,'p_lista_remove','interprete.py',540),
  ('lista_remove -> parametros_remove','lista_remove',1,'p_lista_remove','interprete.py',541),
  ('parametros_remove -> param_path','parametros_remove',1,'p_parametros_remove','interprete.py',549),
  ('parametros_remove -> param_path2','parametros_remove',1,'p_parametros_remove','interprete.py',550),
  ('comando_edit -> EDIT lista_edit','comando_edit',2,'p_comando_edit','interprete.py',555),
  ('lista_edit -> lista_edit parametros_edit','lista_edit',2,'p_lista_edit','interprete.py',559),
  ('lista_edit -> parametros_edit','lista_edit',1,'p_lista_edit','interprete.py',560),
  ('parametros_edit -> param_path','parametros_edit',1,'p_parametros_edit','interprete.py',568),
  ('parametros_edit -> param_cont','parametros_edit',1,'p_parametros_edit','interprete.py',569),
  ('comando_rename -> RENAME lista_rename','comando_rename',2,'p_comando_rename','interprete.py',574),
  ('lista_rename -> lista_rename parametros_rename','lista_rename',2,'p_lista_rename','interprete.py',578),
  ('lista_rename -> parametros_rename','lista_rename',1,'p_lista_rename','interprete.py',579),
  ('parametros_rename -> param_name_2','parametros_rename',1,'p_parametros_rename','interprete.py',587),
  ('parametros_rename -> param_name','parametros_rename',1,'p_parametros_rename','interprete.py',588),
  ('parametros_rename -> param_path','parametros_rename',1,'p_parametros_rename','interprete.py',589),
  ('parametros_rename -> param_path2','parametros_rename',1,'p_parametros_rename','interprete.py',590),
  ('param_size -> GUION SIZE IGUAL ENTERO','param_size',4,'p_param_size','interprete.py',595),
  ('param_path -> GUION PATH IGUAL CADENA_FILE_PATH','param_path',4,'p_param_path','interprete.py',599),
  ('param_path -> GUION PATH IGUAL FILE_PATH','param_path',4,'p_param_path','interprete.py',600),
  ('param_unit -> GUION UNIT IGUAL ID','param_unit',4,'p_param_unit','interprete.py',604),
  ('param_name -> GUION NAME IGUAL ID','param_name',4,'p_param_name','interprete.py',608),
  ('param_fit -> GUION FIT IGUAL ID','param_fit',4,'p_param_fit','interprete.py',612),
  ('param_type -> GUION TYPE IGUAL ID','param_type',4,'p_param_type','interprete.py',616),
  ('param_delete -> GUION DELETE IGUAL ID','param_delete',4,'p_param_delete','interprete.py',620),
  ('param_add -> GUION ADD IGUAL ENTERO','param_add',4,'p_param_add','interprete.py',624),
  ('param_add -> GUION ADD IGUAL entero_negativo','param_add',4,'p_param_add','interprete.py',625),
  ('param_id -> GUION ID_WORD IGUAL ID_PAR','param_id',4,'p_param_id','interprete.py',629),
  ('param_fs -> GUION FS IGUAL 2FS','param_fs',4,'p_param_fs','interprete.py',633),
  ('param_fs -> GUION FS IGUAL 3FS','param_fs',4,'p_param_fs','interprete.py',634),
  ('param_user -> GUION USER IGUAL ID','param_user',4,'p_param_user','interprete.py',638),
  ('param_user -> GUION USER IGUAL CADENA_SIMPLE','param_user',4,'p_param_user','interprete.py',639),
  ('param_pass -> GUION PASS IGUAL ID','param_pass',4,'p_param_pass','interprete.py',643),
  ('param_pass -> GUION PASS IGUAL ENTERO','param_pass',4,'p_param_pass','interprete.py',644),
  ('param_grp -> GUION GRP IGUAL ID','param_grp',4,'p_param_grp','interprete.py',648),
  ('param_grp -> GUION GRP IGUAL CADENA_SIMPLE','param_grp',4,'p_param_grp','interprete.py',649),
  ('param_r -> GUION R','param_r',2,'p_param_r','interprete.py',653),
  ('param_cont -> GUION CONT IGUAL CADENA_FILE_PATH','param_cont',4,'p_param_cont','interprete.py',657),
  ('param_cont -> GUION CONT IGUAL FILE_PATH','param_cont',4,'p_param_cont','interprete.py',658),
  ('param_filen -> GUION ID IGUAL CADENA_FILE_PATH','param_filen',4,'p_param_filen','interprete.py',662),
  ('param_filen -> GUION ID IGUAL FILE_PATH','param_filen',4,'p_param_filen','interprete.py',663),
  ('param_path2 -> GUION PATH IGUAL CADENA_DIR_PATH','param_path2',4,'p_param_path2','interprete.py',667),
  ('param_path2 -> GUION PATH IGUAL DIR_PATH','param_path2',4,'p_param_path2','interprete.py',668),
  ('param_name_2 -> GUION NAME IGUAL NAME_2','param_name_2',4,'p_param_name_2','interprete.py',672),
  ('param_ruta -> GUION RUTA IGUAL CADENA_FILE_PATH','param_ruta',4,'p_param_ruta','interprete.py',676),
  ('param_ruta -> GUION RUTA IGUAL FILE_PATH','param_ruta',4,'p_param_ruta','interprete.py',677),
  ('param_ruta2 -> GUION RUTA IGUAL CADENA_DIR_PATH','param_ruta2',4,'p_param_ruta2','interprete.py',681),
  ('param_ruta2 -> GUION RUTA IGUAL DIR_PATH','param_ruta2',4,'p_param_ruta2','interprete.py',682),
  ('param_name__cadena -> GUION NAME IGUAL CADENA_SIMPLE','param_name__cadena',4,'p_param_name__cadena','interprete.py',686),
  ('entero_negativo -> GUION ENTERO','entero_negativo',2,'p_entero_negativo','interprete.py',692),
]
