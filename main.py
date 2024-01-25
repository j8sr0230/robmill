import time
import itertools

import numpy as np

import FreeCAD as App
import FreeCADGui as Gui
import Part


def animate_spindle(wires: list[Part.Wire], normals: Part.Face, dist: int = 1, step: int = 1) -> None:
    # noinspection PyUnresolvedReferences
    target_pos: list[App.Vector] = list(
        itertools.chain.from_iterable([w.discretize(Distance=dist) for w in wires])
    )

    # noinspection PyUnresolvedReferences
    normal_srf: Part.Face.Surface = normals.Surface
    target_placement: App.Placement = App.Placement()
    for i in np.arange(0, len(target_pos), step):
        # noinspection PyUnresolvedReferences
        uv: tuple[float, float] = normal_srf.parameter(target_pos[i])
        # noinspection PyUnresolvedReferences
        normal: App.Vector = normal_face.normalAt(uv[0], uv[1])

        target_placement.Base = target_pos[i]
        target_placement.Rotation = App.Rotation(tool_normal, -normal)
        tool_obj.Placement = target_placement
        Gui.updateGui()
        time.sleep(0.0005)


def animate_fixture(wires: list[Part.Wire], normals: Part.Face, dist: int = 1, step: int = 1) -> None:
    fixed_tool_pos: App.Vector = App.Vector(1850, -370, 490)
    fixed_tool_normal: App.Vector = App.Vector(-1, 0, 0)
    # fixed_tool_x: App.Vector = App.Vector(0, 1, 0)

    # noinspection PyUnresolvedReferences
    fixture_zero_vertex: Part.Vertex = fixture_obj.Shape.Vertexes[1]
    fixture_zero_vect: App.Vector = App.Vector(fixture_zero_vertex.X, fixture_zero_vertex.Y, fixture_zero_vertex.Z)

    # noinspection PyUnresolvedReferences
    target_pos: list[App.Vector] = list(
        itertools.chain.from_iterable([w.discretize(Distance=dist) for w in wires])
    )

    # noinspection PyUnresolvedReferences
    normal_srf: Part.Face.Surface = normals.Surface
    for i in np.arange(0, len(target_pos), step):
        # noinspection PyUnresolvedReferences
        uv: tuple[float, float] = normal_srf.parameter(target_pos[i])
        # noinspection PyUnresolvedReferences
        normal: App.Vector = normal_face.normalAt(uv[0], uv[1])

        target_placement: App.Placement = App.Placement()
        target_placement.Base = fixed_tool_pos - target_pos[i]

        rot: App.Rotation = App.Rotation(fixed_tool_normal, -normal)
        target_placement.rotate(tuple(target_pos[i]), rot.Axis, float(np.degrees(-rot.Angle)))
        target_obj.Placement = target_placement

        Gui.updateGui()

        # noinspection PyUnresolvedReferences
        p = App.Placement()
        p.Base = target_placement.Base
        # p.rotate(tuple(target_placement.Base), rot.Axis, float(np.degrees(rot.Angle)))
        box.Placement = p

        print(p*fixture_zero_vect)

        time.sleep(0.0005)


doc: App.Document = App.ActiveDocument

# tool and target
target_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_target")[0]
fixture_obj: App.DocumentObject = doc.getObjectsByLabel("fixture")[0]
box: App.DocumentObject = doc.getObjectsByLabel("Quader")[0]


# target_obj: App.DocumentObject = doc.getObjectsByLabel("target_simplified")[0]

tool_obj: App.DocumentObject = doc.getObjectsByLabel("5mm_endmill")[0]
tool_normal: App.Vector = App.Vector(0, 0, -1)
tool_x: App.Vector = App.Vector(1, 0, 0)

#####################################
# feature_1_clearing job
path_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_clearing_path")[0]
# noinspection PyUnresolvedReferences
wires_list: list[Part.Wire] = path_obj.Shape.Wires
# noinspection PyUnresolvedReferences
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_clearing_top")[0].Shape.Faces[0]

# animate_spindle(wires_list, normal_face, dist=2, step=2)
animate_fixture(wires_list, normal_face, dist=3, step=3)

#####################################
# feature_1_hor_finishing job
path_obj_1: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_1")[0]
path_obj_2: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_2")[0]
path_obj_3: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_3")[0]
path_obj_4: App.DocumentObject = doc.getObjectsByLabel("feature_1_hor_finishing_path_4")[0]
# noinspection PyUnresolvedReferences
wires_list: list[Part.Wire] = [
    path_obj_1.Shape.Wires[0], path_obj_2.Shape.Wires[0], path_obj_3.Shape.Wires[0], path_obj_4.Shape.Wires[0]
]
# noinspection PyUnresolvedReferences
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_hor_finishing_srf")[0].Shape.Faces[0]

# animate_spindle(wires_list, normal_face, dist=1, step=1)
animate_fixture(wires_list, normal_face, dist=2, step=2)

#####################################
# feature_1_ver_finishing job
path_obj: App.DocumentObject = doc.getObjectsByLabel("feature_1_ver_finishing_path")[0]
# noinspection PyUnresolvedReferences
wires_list: list[Part.Wire] = path_obj.Shape.Wires
# noinspection PyUnresolvedReferences
normal_face: Part.Face = doc.getObjectsByLabel("feature_1_ver_finishing_srf")[0].Shape.Faces[0]

# animate_spindle(wires_list, normal_face, dist=1, step=1)
animate_fixture(wires_list, normal_face, dist=2, step=2)
