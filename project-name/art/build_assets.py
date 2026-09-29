"""Original Gauntlet-inspired low-poly kit; run inside official Blender MCP."""
import bpy, math, json, os
from mathutils import Vector
ROOT = 'D:/Documents/Projects/VC/BabylonJS/babylon-lite-gauntlet-clone-3d/project-name'
OUT = ROOT + '/public/assets'
os.makedirs(OUT, exist_ok=True)
scene = bpy.data.scenes.new('Gauntlet3D_Art')
bpy.context.window.scene = scene
scene.unit_settings.system = 'METRIC'
materials = {}
def mat(name, color, metal=0, emit=0):
    m=bpy.data.materials.new('G3_'+name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.7
    if emit:p.inputs['Emission Color'].default_value=(*color,1);p.inputs['Emission Strength'].default_value=emit
    materials[name]=m
for n,c in {'stone':(.16,.20,.24),'edge':(.25,.30,.34),'dark':(.035,.05,.065),'red':(.55,.085,.065),'gold':(.8,.49,.12),'silver':(.58,.66,.72),'skin':(.67,.4,.23),'purple':(.31,.12,.50),'green':(.17,.38,.11),'wood':(.23,.11,.045),'bone':(.72,.74,.61),'ghost':(.24,.65,.66),'grunt':(.53,.29,.09),'demon':(.45,.045,.07),'bread':(.72,.36,.10)}.items():mat(n,c,.45 if n in ['gold','silver'] else 0)
mat('teal',(.06,.85,.76),emit=2);mat('fire',(1,.37,.035),emit=2)
parts=[];assets={}
def finish(o,name,m):
    o.name=name;o.data.materials.append(materials[m]);parts.append(o);return o
def box(name,pos,size,m,bevel=.04):
    bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=finish(bpy.context.object,name,m);o.scale=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        mod=o.modifiers.new('cut stone edges','BEVEL');mod.width=bevel;mod.segments=1;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=mod.name)
    return o
def orb(name,pos,scale,m,sub=1):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=sub,radius=1,location=pos);o=finish(bpy.context.object,name,m);o.scale=scale;return o
def cone(name,pos,r1,r2,depth,m,vertices=8):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices,radius1=r1,radius2=r2,depth=depth,location=pos);return finish(bpy.context.object,name,m)
def rod(name,a,b,r,m,vertices=8):
    delta=Vector(b)-Vector(a);o=cone(name,(Vector(a)+Vector(b))/2,r,r,delta.length,m,vertices);o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return o
def horn(name,a,b,r,m):
    delta=Vector(b)-Vector(a);o=cone(name,(Vector(a)+Vector(b))/2,r,0,delta.length,m,6);o.rotation_euler=delta.to_track_quat('Z','Y').to_euler();return o
def torus(name,pos,major,minor,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=12,minor_segments=4,location=pos,rotation=rot);return finish(bpy.context.object,name,m)
def export(name):
    global parts
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts:o.select_set(True)
    bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.convert(target='MESH');bpy.ops.object.join();o=bpy.context.object;o.name=name
    bpy.context.scene.cursor.location=(0,0,0);bpy.ops.object.origin_set(type='ORIGIN_CURSOR');bpy.ops.object.transform_apply(location=False,rotation=True,scale=True)
    bpy.ops.export_scene.gltf(filepath=OUT+'/'+name+'.glb',export_format='GLB',use_selection=True,use_active_scene=True,export_yup=True)
    assets[name]=o;parts=[]
def humanoid(kind,cloth,skin='skin',width=.32):
    for x in [-.18,.18]:
        box('boot',(x,-.07,.12),(.24,.39,.24),'wood')
        rod('leg',(x,0,.2),(x,0,.65),.115,cloth)
    cone('tunic',(0,0,.77),width,width*.8,.57,cloth)
    box('belt',(0,-.015,.65),(width*1.85,.43,.10),'gold')
    orb('head',(0,0,1.26),(.22,.20,.25),skin,2)
    for x in [-.36,.36]:
        orb('pauldron',(x,0,.99),(.19,.24,.18),cloth)
        rod('arm',(x,0,.98),(x*1.16,-.05,.68),.10,cloth)
        orb('hand',(x*1.16,-.05,.64),(.105,.11,.12),skin)
    for x in [-.075,.075]:box('eye',(x,-.185,1.30),(.05,.025,.045),'dark',0)
for kind in ['warrior','valkyrie','wizard','elf','grunt','demon','lobber','ghost']:
    if kind=='ghost':
        cone('spectral shroud',(0,0,.8),.34,.24,.85,'ghost');orb('hood',(0,0,1.29),(.3,.25,.34),'ghost',1)
        box('dark face',(0,-.215,1.3),(.3,.065,.28),'dark')
        for x in [-.09,.09]:orb('glowing eyes',(x,-.26,1.33),(.04,.025,.055),'teal')
        for x in [-.43,.43]:rod('reaching arm',(x*.55,0,1.0),(x,-.19,.7),.075,'ghost');horn('tattered tip',(x*.4,0,.45),(x*.6,.03,.13),.16,'ghost')
    else:
        cloth={'warrior':'red','valkyrie':'gold','wizard':'purple','elf':'green','grunt':'grunt','demon':'demon','lobber':'wood'}[kind]
        humanoid(kind,cloth,'grunt' if kind in ['grunt','lobber'] else 'demon' if kind=='demon' else 'skin',.38 if kind in ['grunt','warrior'] else .30)
        if kind=='warrior':
            cone('helmet',(0,0,1.4),.24,.19,.23,'red');box('nose guard',(0,-.22,1.30),(.05,.06,.32),'gold')
            for x in [-.2,.2]:horn('horn',(x,0,1.43),(x*1.8,0,1.69),.095,'bone')
            rod('axe handle',(-.46,0,.25),(-.46,0,1.5),.045,'wood');box('axe blade',(-.52,0,1.37),(.48,.11,.34),'silver')
        if kind=='valkyrie':
            cone('helmet',(0,0,1.45),.24,.12,.24,'gold')
            for x in [-.2,.2]:
                for i in range(3):horn('wing feather',(x,0,1.42+i*.055),(x*(2.2+i*.3),0,1.66+i*.10),.07,'silver')
            shield=cone('shield',(.47,-.13,.85),.31,.31,.10,'gold',12);shield.rotation_euler[0]=math.pi/2
            orb('shield jewel',(.47,-.20,.85),(.11,.06,.11),'teal')
            rod('sword hilt',(-.43,0,.52),(-.43,0,.83),.05,'gold');box('crossguard',(-.43,0,.79),(.3,.1,.07),'gold');horn('sword',(-.43,0,.84),(-.43,0,1.56),.10,'silver')
        if kind=='wizard':
            cone('robe',(0,0,.57),.42,.25,.90,'purple');cone('hat brim',(0,0,1.51),.4,.4,.06,'purple');cone('pointed hat',(.02,0,1.76),.25,0,.52,'purple')
            horn('beard',(0,-.17,1.18),(0,-.25,.83),.15,'bone');rod('staff',(-.46,0,.05),(-.46,0,1.57),.045,'wood');orb('staff crystal',(-.46,0,1.71),(.13,.12,.22),'teal')
        if kind=='elf':
            cone('hood',(0,.035,1.47),.27,0,.42,'green')
            for x in [-.2,.2]:horn('pointed ear',(x,0,1.3),(x*1.65,-.015,1.39),.08,'skin')
            a=[(.46,-.02,.35),(.61,-.07,.65),(.64,-.07,.95),(.46,-.02,1.27)]
            for i in range(3):rod('bow',a[i],a[i+1],.035,'gold')
            rod('bowstring',a[0],a[-1],.009,'bone');box('quiver',(0,.24,.96),(.18,.17,.58),'wood')
        if kind=='grunt':
            rod('club',(-.47,0,.40),(-.47,0,1.3),.065,'wood');orb('club head',(-.47,0,1.3),(.16,.15,.26),'stone');box('jaw',(0,-.14,1.12),(.31,.23,.16),'grunt')
            for x in [-.12,.12]:horn('tusk',(x,-.25,1.10),(x,-.27,1.25),.045,'bone')
        if kind=='demon':
            for x in [-.2,.2]:horn('black horn',(x,0,1.42),(x*1.9,.05,1.88),.13,'gold');horn('claw',(x*2,-.08,.7),(x*2,-.19,.45),.07,'dark')
            for x in [-.45,.45]:horn('wing',(x*.5,.13,.9),(x*1.8,.15,1.45),.2,'demon')
            for x in [-.075,.075]:orb('fire eye',(x,-.2,1.31),(.045,.03,.035),'fire')
        if kind=='lobber':
            orb('bomb',(-.42,-.08,1.15),(.31,.3,.31),'dark',2);rod('fuse',(-.42,-.08,1.4),(-.35,-.08,1.58),.025,'gold');orb('spark',(-.35,-.08,1.6),(.05,.05,.08),'fire');box('backpack',(0,.25,.86),(.46,.3,.52),'wood')
    export(kind)
box('slab',(0,0,-.12),(.99,.99,.24),'stone',.035);box('inset',(0,0,.006),(.85,.85,.025),'edge',.025);export('floor')
for z in range(3):
    for x in [-.245,.245]:box('masonry',(x,0,.20+z*.35),(.475,.93,.33),'stone' if z%2 else 'edge',.035)
box('cap',(0,0,1.12),(1.02,1.02,.16),'edge');export('wall')
box('base',(0,0,.12),(1.25,1.25,.24),'stone');box('altar',(0,0,.4),(.88,.88,.35),'edge');cone('rune bowl',(0,0,.65),.4,.5,.15,'gold');orb('soul crystal',(0,0,1.02),(.25,.25,.47),'teal');export('altar')
box('platter',(0,0,.04),(.72,.6,.08),'wood');orb('bread',(0,0,.20),(.3,.21,.16),'bread',2);orb('apple',(.26,.1,.19),(.13,.13,.14),'red',2);export('food')
torus('key head',(0,0,.10),.17,.055,'gold');box('key shaft',(0,-.31,.1),(.075,.45,.08),'gold');box('key tooth',(.07,-.49,.1),(.20,.075,.08),'gold');export('key')
box('chest',(0,0,.25),(.75,.55,.5),'wood');box('lid',(0,0,.53),(.79,.59,.12),'gold');box('lock',(0,-.3,.33),(.13,.08,.19),'gold');export('treasure')
for x in [-.8,.8]:box('portal pillar',(x,0,1.1),(.38,.55,2.2),'edge');orb('ward',(x,-.3,1.5),(.14,.1,.24),'teal')
box('lintel',(0,0,2.15),(2,.6,.38),'stone');box('portal surface',(0,.12,1.03),(1.3,.08,1.9),'teal');export('exit')
cone('torch base',(0,0,.15),.23,.18,.3,'stone');rod('torch',(0,0,.2),(0,0,1.3),.07,'wood');cone('brazier',(0,0,1.24),.12,.22,.2,'gold');orb('flame',(0,0,1.52),(.17,.16,.32),'fire');export('torch')
# Lay out a genuine preview of the actual source meshes.
for i,(name,o) in enumerate(assets.items()):o.location=((i%8-3.5)*2.1,(i//8)*3.2,0)
world=bpy.data.worlds.new('G3 Studio');world.use_nodes=True;world.node_tree.nodes['Background'].inputs[0].default_value=(.08,.10,.14,1);world.node_tree.nodes['Background'].inputs[1].default_value=.6;scene.world=world
box('preview ground',(0,1,-.23),(19,10,.2),'dark');parts=[]
bpy.ops.object.light_add(type='AREA',location=(-4,-5,10));bpy.context.object.data.energy=1800;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=8
bpy.ops.object.light_add(type='AREA',location=(7,3,8));bpy.context.object.data.energy=1500;bpy.context.object.data.size=7
bpy.ops.object.camera_add(location=(9,-15,17));camera=bpy.context.object;camera.rotation_euler=(Vector((0,1,0.6))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=21;scene.camera=camera
scene.render.engine='CYCLES';scene.cycles.samples=24;scene.render.resolution_x=1536;scene.render.resolution_y=1024;scene.render.resolution_percentage=100
scene.render.filepath=ROOT+'/documentation/assets-preview.png'
bpy.ops.wm.save_as_mainfile(filepath=ROOT+'/art/dungeon-kit.blend',copy=True)
bpy.ops.render.render(write_still=True)
manifest={name:{'vertices':len(o.data.vertices),'polygons':len(o.data.polygons),'file':name+'.glb'} for name,o in assets.items()}
with open(OUT+'/manifest.json','w') as f:json.dump({'blender':bpy.app.version_string,'assets':manifest,'source':'project-name/art/dungeon-kit.blend','limitations':'Static meshes; movement and attack motion are runtime transforms. Solid-color materials; no baked textures.'},f,indent=2)
result={'assets':manifest,'preview':scene.render.filepath,'source':ROOT+'/art/dungeon-kit.blend'}
