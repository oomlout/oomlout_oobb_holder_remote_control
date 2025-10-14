import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    test = False
    #test = True

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
        #default
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True; test = False
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
        #default
        #filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "test"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = "holder_remote_control"
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        


        holders = []
        #electronic_dc_to_dc_converter_buck_style_300_watt_20_amp_52_mm_width_60_mm_length_blue_pcb_aliexpress
        if True:
            holder_current = {}
            holder_current["description_extra"] = "esc_kingmodel_10ax2"
            holder_current["part_oomp"] = "remote_control_electronic_speed_controller_brushed_style_10_amp_maximum_current_25_mm_width_45_mm_height_black_pcb_6s_22_volt_maximum_kingmodel_10ax2"
            holder_current["width"] = 4
            holder_current["height"] = 4
            holder_current["thickness"] = 3
            holder_current["holes"] = "top_and_bottom"
            holder_current["style_attachment"] = "ziptie"
            holders.append(holder_current)


            holder_current = copy.deepcopy(holder_current)
            holder_current["height"] = 3
            holder_current["shift_y"] = 7.5
            holder_current["holes"] = "top"
            holders.append(holder_current)

        for holder in holders:
            
            
            hol = holder.get("holes", "top_and_bottom")
            ex = holder["description_extra"]
            extra = ""
            extra+= f"{ex}_{hol}_holes"
            part = copy.deepcopy(part_default)
            part.update(holder)
            
            p3 = copy.deepcopy(kwargs)
            p3.update(holder)
            #p3["shift_y"] = shift_y             
            #p3["width"] = int(wid)
            #p3["height"] = int(hei)
            #p3["thickness"] = int(thi)
            #p3["holes"] = hol
            part_details = load_part(holder["part_oomp"])
            p3["part_details"] = part_details
            p3["extra"] = extra
            part["kwargs"] = p3
            nam = "holder_remote_control"
            part["name"] = nam
            if oomp_mode == "oobb":
                p3["oomp_size"] = nam
            if not test:
                pass
                parts.append(part)


    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_holder_remote_control(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    holes = kwargs.get("holes", "top_and_bottom")
    style_attachment = kwargs.get("style_attachment", "mounting_hole")
    shift_y = kwargs.get("shift_y", 0)
    #kwargs.pop("holes", None)
    if holes == "top_and_bottom":
        holes = ["left", "right"]
    elif holes == "top":
        holes = "right"
    part_details = kwargs.get("part_details", {})
    oomp_id = part_details.get("id", "")

    mounting_hole_length = part_details.get("mounting_hole_length", 100)
    mounting_hole_width = part_details.get("mounting_hole_width", 150)
    mounting_hole_size = part_details.get("mounting_hole_diameter", "m4")
    shift_y = kwargs.get("shift_y", 0)

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[1] += shift_y
    p3["pos"] = pos1

    p3.pop("holes", None)
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    pos1[1] += shift_y
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add mounting holes
    if style_attachment == "mounting_hole":    
        poss = []
        if True:
            pos1 = copy.deepcopy(pos)
            pos1[2] += 0
            pos11 = copy.deepcopy(pos1)
            pos11[0] += mounting_hole_length/2
            pos11[1] += mounting_hole_width/2
            poss.append(pos11)
            pos12 = copy.deepcopy(pos1)
            pos12[0] += -mounting_hole_length/2
            pos12[1] += mounting_hole_width/2
            poss.append(pos12)
            pos13 = copy.deepcopy(pos1)
            pos13[0] += -mounting_hole_length/2
            pos13[1] += -mounting_hole_width/2
            poss.append(pos13)
            pos14 = copy.deepcopy(pos1)
            pos14[0] += mounting_hole_length/2
            pos14[1] += -mounting_hole_width/2
            poss.append(pos14)
        for pos1 in poss:
            kwargs2 = copy.deepcopy(kwargs)
            #pos11 = copy.deepcopy(pos)
            #pos11[1] += shift_y
            #kwargs2["pos"] = pos11
            p3 = add_standoff(thing, **kwargs2, position=pos1)
    elif style_attachment == "ziptie":
        poss = []
        if oomp_id == "remote_control_electronic_speed_controller_brushed_style_10_amp_maximum_current_25_mm_width_45_mm_height_black_pcb_6s_22_volt_maximum_kingmodel_10ax2":
            shift_xx = 7.5
            shift_yy = 15

        pos1 = copy.deepcopy(pos)
        pos1[2] += 0
        pos11 = copy.deepcopy(pos1)
        pos11[0] += shift_xx
        pos11[1] += shift_yy
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -shift_xx
        pos12[1] += shift_yy
        poss.append(pos12)
        pos13 = copy.deepcopy(pos1)
        pos13[0] += shift_xx
        pos13[1] += -shift_yy
        poss.append(pos13)
        pos14 = copy.deepcopy(pos1)
        pos14[0] += -shift_xx
        pos14[1] += -shift_yy
        poss.append(pos14)
        for pos1 in poss:
            kwargs2 = copy.deepcopy(kwargs)
            #pos11 = copy.deepcopy(pos)
            #pos11[1] += shift_y
            #kwargs2["pos"] = pos11
            p3 = add_ziptie(thing, **kwargs2, position=pos1)
    
    #add_cutouts
    if True:
        cutouts = []
        if oomp_id == "remote_control_electronic_speed_controller_brushed_style_10_amp_maximum_current_25_mm_width_45_mm_height_black_pcb_6s_22_volt_maximum_kingmodel_10ax2":
            cutout = {}            
            cutout["size"] = [15, 20,3]
            cutout["pos"] = [-24, 3, 0]
            cutouts.append(cutout)
            cutout = {}
            cutout["size"] = [8, 26,3]
            cutout["pos"] = [17.5, 0, 0]
            cutouts.append(cutout)
            cutout = {}
            cutout["size"] = [5,33,1.5]
            cutout["pos"] = [7.5, 0, 1.5]
            cutouts.append(cutout)
            cutout = {}
            cutout["size"] = [5,33,1.5]
            cutout["pos"] = [-7.5, 0, 1.5]
            cutouts.append(cutout)
            
        for cutout in cutouts:
            p3 = copy.deepcopy(kwargs)
            p3["type"] = "n"
            p3["shape"] = f"oobb_cube"
            p3.update(cutout)
            #p3["m"] = "#"
            oobb_base.append_full(thing,**p3)




    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def load_part(part_id):
    folder_parts = "parts/"
    folder = f"{folder_parts}{part_id}"
    file_name = f"{folder}/working.yaml"
    details = {}
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            try:
                details = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
    else:
        print(f"Part file not found: {file_name}")
    return details

def add_standoff(thing, **kwargs):
    position = kwargs.get("position", [0,0,0]) 
    pos = kwargs.get("pos", [0, 0, 0])
    rot = kwargs.get("rot", [0, 0, 0])
    depth = kwargs.get("thickness", 3)
    mounting_hole_size = kwargs.get("part_details",{}).get("mounting_hole_size", "m4")
    lift = 3
    depth = depth + 3
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_cylinder"
    rad = (float(mounting_hole_size.replace("m", "").replace("_","."))+4)/2
    p3["radius"] = rad
    p3["depth"] = depth
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos) 
    pos1[0] += position[0]
    pos1[1] += position[1]
    pos1[2] += lift
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    #add countersunk screw
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = mounting_hole_size
    p3["depth"] = 10
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[0] += position[0]
    pos1[1] += position[1]
    pos1[2] += 0
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    rot1[0] += 180
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)

def add_ziptie(thing, **kwargs):
    position = kwargs.get("position", [0,0,0]) 
    pos = kwargs.get("pos", [0, 0, 0])
    rot = kwargs.get("rot", [0, 0, 0])
    depth = kwargs.get("thickness", 3)       
    
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "n"
    p3["shape"] = f"oobb_cube"
    wid = 5
    hei = 3
    dep = depth
    size = [wid, hei, dep]
    p3["size"] = size
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos) 
    pos1[0] += position[0]
    pos1[1] += position[1]
    pos1[2] += 0
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
     


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)
