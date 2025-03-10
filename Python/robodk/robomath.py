# Copyright 2015-2021 - RoboDK Inc. - https://robodk.com/
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# --------------------------------------------
# --------------- DESCRIPTION ----------------
#
# This is a robotics toolbox for RoboDK robot post processors and RoboDK API for Python
# This toolbox includes a simple matrix class for pose transofmrations (Mat)
# This toolbox has been inspired from Peter Corke's Robotics Toolbox:
# http://petercorke.com/wordpress/toolboxes/robotics-toolbox
#
# In this document: pose = transformation matrix = homogeneous matrix = 4x4 matrix
#
# More information about the RoboDK API for Python here:
#     https://robodk.com/doc/en/RoboDK-API.html
#     https://robodk.com/doc/en/PythonAPI/index.html
#
# Visit the Matrix and Quaternions FAQ for more information about pose/homogeneous transformations
#     http://www.j3d.org/matrix_faq/matrfaq_latest.html
# --------------------------------------------

import math
import time

#----------------------------------------------------
#--------      Generic math usage     ---------------

pi = math.pi  #: PI


def pause(seconds):
    """Pause in seconds

    :param pause: time in seconds
    :type pause: float"""
    time.sleep(seconds)


def sqrt(value):
    """Returns the square root of a value"""
    return math.sqrt(value)


def sqrtA(value):
    """Returns the square root of a value if it's greater than 0, else 0 (differs from IEEE-754)."""
    if value <= 0:
        return 0
    return sqrt(value)


def sin(value):
    """Returns the sine of an angle in radians"""
    return math.sin(value)


def cos(value):
    """Returns the cosine of an angle in radians"""
    return math.cos(value)


def tan(value):
    """Returns the tangent of an angle in radians"""
    return math.tan(value)


def asin(value):
    """Returns the arc sine in radians"""
    return math.asin(value)


def acos(value):
    """Returns the arc cosinus in radians"""
    return math.acos(value)


def atan2(y, x):
    """Returns angle of a 2D coordinate in the XY plane"""
    return math.atan2(y, x)


def name_2_id(str_name_id):
    """Returns the number of a numbered object. For example: "Frame 3", "Frame3", "Fram3 3" returns 3."""
    import re
    numbers = re.findall(r'[0-9]+', str_name_id)
    if len(numbers) > 0:
        return float(numbers[-1])
    return -1


#----------------------------------------------------
#--------     Generic matrix usage    ---------------


def rotx(rx):
    r"""Returns a rotation matrix around the X axis (radians)

    .. math::

        R_x(\theta) = \begin{bmatrix} 1 & 0 & 0 & 0 \\
        0 & c_\theta & -s_\theta & 0 \\
        0 & s_\theta & c_\theta & 0 \\
        0 & 0 & 0 & 1
        \end{bmatrix}

    :param float rx: rotation around X axis in radians

    .. seealso:: :func:`~robodk.robomath.transl`, :func:`~robodk.robomath.roty`, :func:`~robodk.robomath.roty`
    """
    ct = math.cos(rx)
    st = math.sin(rx)
    return Mat([[1, 0, 0, 0], [0, ct, -st, 0], [0, st, ct, 0], [0, 0, 0, 1]])


def roty(ry):
    r"""Returns a rotation matrix around the Y axis (radians)

    .. math::

        R_y(\theta) = \begin{bmatrix} c_\theta & 0 & s_\theta & 0 \\
        0 & 1 & 0 & 0 \\
        -s_\theta & 0 & c_\theta & 0 \\
        0 & 0 & 0 & 1
        \end{bmatrix}

    :param float ry: rotation around Y axis in radians

    .. seealso:: :func:`~robodk.robomath.transl`, :func:`~robodk.robomath.rotx`, :func:`~robodk.robomath.rotz`
    """
    ct = math.cos(ry)
    st = math.sin(ry)
    return Mat([[ct, 0, st, 0], [0, 1, 0, 0], [-st, 0, ct, 0], [0, 0, 0, 1]])


def rotz(rz):
    r"""Returns a rotation matrix around the Z axis (radians)

    .. math::

        R_x(\theta) = \begin{bmatrix} c_\theta & -s_\theta & 0 & 0 \\
        s_\theta & c_\theta & 0 & 0 \\
        0 & 0 & 1 & 0 \\
        0 & 0 & 0 & 1
        \end{bmatrix}

    :param float ry: rotation around Y axis in radians

    .. seealso:: :func:`~robodk.robomath.transl`, :func:`~robodk.robomath.rotx`, :func:`~robodk.robomath.roty`
    """
    ct = math.cos(rz)
    st = math.sin(rz)
    return Mat([[ct, -st, 0, 0], [st, ct, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def transl(tx, ty=None, tz=None):
    r"""Returns a translation matrix (mm)

    .. math::

        T(t_x, t_y, t_z) = \begin{bmatrix} 1 & 0 & 0 & t_x \\
        0 & 1 & 0 & t_y \\
        0 & 0 & 1 & t_z \\
        0 & 0 & 0 & 1
        \end{bmatrix}

    :param float tx: translation along the X axis
    :param float ty: translation along the Y axis
    :param float tz: translation along the Z axis

    .. seealso:: :func:`~robodk.robomath.rotx`, :func:`~robodk.robomath.roty`, :func:`~robodk.robomath.rotz`
    """
    if ty is None:
        xx = tx[0]
        yy = tx[1]
        zz = tx[2]
    else:
        xx = tx
        yy = ty
        zz = tz
    return Mat([[1, 0, 0, xx], [0, 1, 0, yy], [0, 0, 1, zz], [0, 0, 0, 1]])


def RelTool(target_pose, x, y, z, rx=0, ry=0, rz=0):
    """Calculates a relative target with respect to the tool coordinates. This procedure has exactly the same behavior as ABB's RelTool instruction.
    X,Y,Z are in mm, RX,RY,RZ are in degrees.

    :param :class:`.Mat` target_pose: Reference pose
    :param float x: translation along the Tool X axis (mm)
    :param float y: translation along the Tool Y axis (mm)
    :param float z: translation along the Tool Z axis (mm)
    :param float rx: rotation around the Tool X axis (deg) (optional)
    :param float ry: rotation around the Tool Y axis (deg) (optional)
    :param float rz: rotation around the Tool Z axis (deg) (optional)

    .. seealso:: :func:`~robodk.robomath.Offset`, :func:`~robodk.robomath.transl`, :func:`~robodk.robomath.rotx`, :func:`~robodk.robomath.roty`, :func:`~robodk.robomath.rotz`
    """
    if type(target_pose) != Mat:
        target_pose = target_pose.Pose()
    new_target = target_pose * transl(x, y, z) * rotx(rx * pi / 180) * roty(ry * pi / 180) * rotz(rz * pi / 180)
    return new_target


def Offset(target_pose, x, y, z, rx=0, ry=0, rz=0):
    """Calculates a relative target with respect to the reference frame coordinates.
    X,Y,Z are in mm, RX,RY,RZ are in degrees.

    :param :class:`.Mat` target_pose: Reference pose
    :param float x: translation along the Reference X axis (mm)
    :param float y: translation along the Reference Y axis (mm)
    :param float z: translation along the Reference Z axis (mm)
    :param float rx: rotation around the Reference X axis (deg) (optional)
    :param float ry: rotation around the Reference Y axis (deg) (optional)
    :param float rz: rotation around the Reference Z axis (deg) (optional)

    .. seealso:: :func:`~robodk.robomath.RelTool`, :func:`~robodk.robomath.transl`, :func:`~robodk.robomath.rotx`, :func:`~robodk.robomath.roty`, :func:`~robodk.robomath.rotz`
    """
    if type(target_pose) != Mat:
        # item object assumed:
        target_pose = target_pose.Pose()
    if not target_pose.isHomogeneous():
        raise Exception(MatrixError, "Pose matrix is not homogeneous!")
    new_target = transl(x, y, z) * rotx(rx * pi / 180.0) * roty(ry * pi / 180.0) * rotz(rz * pi / 180.0) * target_pose
    return new_target


def point_Xaxis_2_pose(point, xaxis, zaxis_hint1=[0, 0, -1], zaxis_hint2=[0, -1, 0]):
    """Returns a pose given the origin as a point, a X axis and a preferred orientation for the Z axis"""
    pose = eye(4)
    pose.setPos(point)
    pose.setVX(xaxis)
    zaprox = zaxis_hint1
    delta = abs(angle3(xaxis, zaprox))
    if delta < 0.03 or abs(delta - pi) < 0.03:
        zaprox = zaxis_hint2
    yaxis = normalize3(cross(zaprox, xaxis))
    zaxis = cross(xaxis, yaxis)
    pose.setVY(yaxis)
    pose.setVZ(zaxis)
    return pose


def point_Yaxis_2_pose(point, yaxis, zaxis_hint1=[0, 0, -1], zaxis_hint2=[-1, 0, 0]):
    """Returns a pose given the origin as a point, a Y axis and a preferred orientation for the Z axis"""
    pose = eye(4)
    pose.setPos(point)
    pose.setVY(yaxis)
    zaprox = zaxis_hint1
    delta = abs(angle3(yaxis, zaprox))
    if delta < 0.03 or abs(delta - pi) < 0.03:
        zaprox = zaxis_hint2
    xaxis = normalize3(cross(yaxis, zaprox))
    zaxis = cross(xaxis, yaxis)
    pose.setVX(xaxis)
    pose.setVZ(zaxis)
    return pose


def point_Zaxis_2_pose(point, zaxis, yaxis_hint1=[0, 0, 1], yaxis_hint2=[0, 1, 1]):
    """Returns a pose given the origin as a point, a Z axis and a preferred orientation for the Y axis"""
    pose = eye(4)
    pose.setPos(point)
    pose.setVZ(zaxis)
    yaprox = yaxis_hint1
    delta = abs(angle3(zaxis, yaprox))
    if delta < 0.03 or abs(delta - pi) < 0.03:
        yaprox = yaxis_hint2
    xaxis = normalize3(cross(yaprox, zaxis))
    yaxis = cross(zaxis, xaxis)
    pose.setVX(xaxis)
    pose.setVY(yaxis)
    return pose


def eye(size=4):
    r"""Returns the identity matrix

    .. math::

        T(t_x, t_y, t_z) = \begin{bmatrix} 1 & 0 & 0 & 0 \\
        0 & 1 & 0 & 0 \\
        0 & 0 & 1 & 0 \\
        0 & 0 & 0 & 1
        \end{bmatrix}

    :param int size: square matrix size (4x4 Identity matrix by default, otherwise it is initialized to 0)

    .. seealso:: :func:`~robodk.robomath.transl`, :func:`~robodk.robomath.rotx`, :func:`~robodk.robomath.roty`, :func:`~robodk.robomath.rotz`
    """
    if size == 4:
        return Mat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    else:
        newmat = Mat(size, size)
        for i in range(size):
            newmat[i, i] = 1
        return newmat


def size(matrix, dim=None):
    """Returns the size of a matrix (m,n).
    Dim can be set to 0 to return m (rows) or 1 to return n (columns)

    :param matrix: pose
    :type matrix: :class:`.Mat`
    :param dim: dimension
    :type dim: int
    """
    return matrix.size(dim)


def tr(matrix):
    """Returns the transpose of the matrix

    :param matrix: pose
    :type matrix: :class:`.Mat`"""
    return matrix.tr()


def invH(matrix):
    """Returns the inverse of a homogeneous matrix

    :param matrix: pose
    :type matrix: :class:`.Mat`

    .. seealso:: :func:`~robodk.robomath.transl`, :func:`~robodk.robomath.rotx`, :func:`~robodk.robomath.roty`, :func:`~robodk.robomath.rotz`
    """
    return matrix.invH()


def catV(mat1, mat2):
    """Concatenate 2 matrices (vertical concatenation)"""
    return mat1.catV(mat2)


def catH(mat1, mat2):
    """Concatenate 2 matrices (horizontal concatenation)"""
    return mat1.catH(mat2)


def tic():
    """Start a stopwatch timer"""
    import time
    global TICTOC_START_TIME
    TICTOC_START_TIME = time.time()


def toc():
    """Read the stopwatch timer"""
    import time
    if 'TICTOC_START_TIME' in globals():
        elapsed = time.time() - TICTOC_START_TIME
        #print("Elapsed time is " + str(elapsed) + " seconds.")
        return elapsed
    else:
        print("Toc: start time not set")
        return -1


#----------------------------------------------------
#------ Pose to xyzrpw and xyzrpw to pose------------
def PosePP(x, y, z, r, p, w):
    """Create a pose from XYZRPW coordinates. The pose format is the one used by KUKA (XYZABC coordinates). This is function is the same as KUKA_2_Pose (with the difference that the input values are not a list). This function is used as "p" by the intermediate file when generating a robot program.

    .. seealso:: :func:`~robodk.robomath.KUKA_2_Pose`, :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    a = r * math.pi / 180.0
    b = p * math.pi / 180.0
    c = w * math.pi / 180.0
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    return Mat([[cb * ca, ca * sc * sb - cc * sa, sc * sa + cc * ca * sb, x], [cb * sa, cc * ca + sc * sb * sa, cc * sb * sa - ca * sc, y], [-sb, cb * sc, cc * cb, z], [0.0, 0.0, 0.0, 1.0]])


def pose_2_xyzrpw(H):
    """Calculates the equivalent position (mm) and Euler angles (deg) as an [x,y,z,r,p,w] array, given a pose.
    It returns the values that correspond to the following operation:
    transl(x,y,z)*rotz(w*pi/180)*roty(p*pi/180)*rotx(r*pi/180)

    :param H: pose
    :type H: :class:`.Mat`
    :return: [x,y,z,r,p,w] in mm and deg

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    x = H[0, 3]
    y = H[1, 3]
    z = H[2, 3]
    if (H[2, 0] > (1.0 - 1e-10)):
        p = -pi / 2
        r = 0
        w = math.atan2(-H[1, 2], H[1, 1])
    elif H[2, 0] < -1.0 + 1e-10:
        p = pi / 2
        r = 0
        w = math.atan2(H[1, 2], H[1, 1])
    else:
        p = math.atan2(-H[2, 0], sqrt(H[0, 0] * H[0, 0] + H[1, 0] * H[1, 0]))
        w = math.atan2(H[1, 0], H[0, 0])
        r = math.atan2(H[2, 1], H[2, 2])
    return [x, y, z, r * 180 / pi, p * 180 / pi, w * 180 / pi]


def xyzrpw_2_pose(xyzrpw):
    """Calculates the pose from the position (mm) and Euler angles (deg), given a [x,y,z,r,p,w] array.
    The result is the same as calling: H = transl(x,y,z)*rotz(w*pi/180)*roty(p*pi/180)*rotx(r*pi/180)

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    [x, y, z, r, p, w] = xyzrpw
    a = r * pi / 180
    b = p * pi / 180
    c = w * pi / 180
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    H = Mat([[cb * cc, cc * sa * sb - ca * sc, sa * sc + ca * cc * sb, x], [cb * sc, ca * cc + sa * sb * sc, ca * sb * sc - cc * sa, y], [-sb, cb * sa, ca * cb, z], [0, 0, 0, 1]])
    return H


def Pose(x, y, z, rxd, ryd, rzd):
    """Returns the pose (:class:`.Mat`) given the position (mm) and Euler angles (deg) as an array [x,y,z,rx,ry,rz].
    The result is the same as calling: H = transl(x,y,z)*rotx(rx*pi/180)*roty(ry*pi/180)*rotz(rz*pi/180)
    This pose format is printed for homogeneous poses automatically. This Pose is the same representation used by Mecademic or Staubli robot controllers.

    :param float tx: position (X coordinate)
    :param float ty: position (Y coordinate)
    :param float tz: position (Z coordinate)
    :param float rxd: first rotation in deg (X coordinate)
    :param float ryd: first rotation in deg (Y coordinate)
    :param float rzd: first rotation in deg (Z coordinate)

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`
    """
    rx = rxd * pi / 180
    ry = ryd * pi / 180
    rz = rzd * pi / 180
    srx = math.sin(rx)
    crx = math.cos(rx)
    sry = math.sin(ry)
    cry = math.cos(ry)
    srz = math.sin(rz)
    crz = math.cos(rz)
    return Mat([[cry * crz, -cry * srz, sry, x], [crx * srz + crz * srx * sry, crx * crz - srx * sry * srz, -cry * srx, y], [srx * srz - crx * crz * sry, crz * srx + crx * sry * srz, crx * cry, z], [0, 0, 0, 1]])


def TxyzRxyz_2_Pose(xyzrpw):
    """Returns the pose given the position (mm) and Euler angles (rad) as an array [x,y,z,rx,ry,rz].
    The result is the same as calling: H = transl(x,y,z)*rotx(rx)*roty(ry)*rotz(rz)

    :param xyzrpw: [x,y,z,rx,ry,rz] in mm and radians
    :type xyzrpw: list of float

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    [x, y, z, rx, ry, rz] = xyzrpw
    srx = math.sin(rx)
    crx = math.cos(rx)
    sry = math.sin(ry)
    cry = math.cos(ry)
    srz = math.sin(rz)
    crz = math.cos(rz)
    H = Mat([[cry * crz, -cry * srz, sry, x], [crx * srz + crz * srx * sry, crx * crz - srx * sry * srz, -cry * srx, y], [srx * srz - crx * crz * sry, crz * srx + crx * sry * srz, crx * cry, z], [0, 0, 0, 1]])
    return H


def Pose_2_TxyzRxyz(H):
    """Retrieve the position (mm) and Euler angles (rad) as an array [x,y,z,rx,ry,rz] given a pose.
    It returns the values that correspond to the following operation:
    H = transl(x,y,z)*rotx(rx)*roty(ry)*rotz(rz).

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    x = H[0, 3]
    y = H[1, 3]
    z = H[2, 3]
    a = H[0, 0]
    b = H[0, 1]
    c = H[0, 2]
    d = H[1, 2]
    e = H[2, 2]
    if c > (1.0 - 1e-10):
        ry1 = pi / 2
        rx1 = 0
        rz1 = atan2(H[1, 0], H[1, 1])
    elif c < (-1.0 + 1e-10):
        ry1 = -pi / 2
        rx1 = 0
        rz1 = atan2(H[1, 0], H[1, 1])
    else:
        sy = c
        cy1 = +sqrt(1 - sy * sy)
        sx1 = -d / cy1
        cx1 = e / cy1
        sz1 = -b / cy1
        cz1 = a / cy1
        rx1 = atan2(sx1, cx1)
        ry1 = atan2(sy, cy1)
        rz1 = atan2(sz1, cz1)
    return [x, y, z, rx1, ry1, rz1]


def Pose_2_Staubli(H):
    """Converts a pose (4x4 matrix) to a Staubli XYZWPR target

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    xyzwpr = Pose_2_TxyzRxyz(H)
    xyzwpr[3] = xyzwpr[3] * 180.0 / pi
    xyzwpr[4] = xyzwpr[4] * 180.0 / pi
    xyzwpr[5] = xyzwpr[5] * 180.0 / pi
    return xyzwpr


def Pose_2_Motoman(H):
    """Converts a pose (4x4 matrix) to a Motoman XYZWPR target (mm and deg)

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    xyzwpr = pose_2_xyzrpw(H)
    return xyzwpr


def Pose_2_Fanuc(H):
    """Converts a pose (4x4 matrix) to a Fanuc XYZWPR target (mm and deg)

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    xyzwpr = pose_2_xyzrpw(H)
    return xyzwpr


def Pose_2_Techman(H):
    """Converts a pose (4x4 matrix) to a Techman XYZWPR target (mm and deg)

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    xyzwpr = pose_2_xyzrpw(H)
    return xyzwpr


def Motoman_2_Pose(xyzwpr):
    """Converts a Motoman target to a pose (4x4 matrix)

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    return xyzrpw_2_pose(xyzwpr)


def Fanuc_2_Pose(xyzwpr):
    """Converts a Fanuc target to a pose (4x4 matrix)

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    return xyzrpw_2_pose(xyzwpr)


def Techman_2_Pose(xyzwpr):
    """Converts a Techman target to a pose (4x4 matrix)

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    return xyzrpw_2_pose(xyzwpr)


def Pose_2_KUKA(H):
    """Converts a pose (4x4 matrix) to an XYZABC KUKA target (Euler angles), required by KUKA KRC controllers.

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    x = H[0, 3]
    y = H[1, 3]
    z = H[2, 3]
    if (H[2, 0]) > (1.0 - 1e-10):
        p = -pi / 2
        r = 0
        w = atan2(-H[1, 2], H[1, 1])
    elif (H[2, 0]) < (-1.0 + 1e-10):
        p = pi / 2
        r = 0
        w = atan2(H[1, 2], H[1, 1])
    else:
        p = atan2(-H[2, 0], sqrt(H[0, 0] * H[0, 0] + H[1, 0] * H[1, 0]))
        w = atan2(H[1, 0], H[0, 0])
        r = atan2(H[2, 1], H[2, 2])
    return [x, y, z, w * 180 / pi, p * 180 / pi, r * 180 / pi]


def KUKA_2_Pose(xyzrpw):
    """Converts a KUKA XYZABC target to a pose (4x4 matrix), required by KUKA KRC controllers.

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    [x, y, z, r, p, w] = xyzrpw
    a = r * math.pi / 180.0
    b = p * math.pi / 180.0
    c = w * math.pi / 180.0
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    return Mat([[cb * ca, ca * sc * sb - cc * sa, sc * sa + cc * ca * sb, x], [cb * sa, cc * ca + sc * sb * sa, cc * sb * sa - ca * sc, y], [-sb, cb * sc, cc * cb, z], [0.0, 0.0, 0.0, 1.0]])


def Adept_2_Pose(xyzrpw):
    """Converts an Adept XYZRPW target to a pose (4x4 matrix)

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    [x, y, z, r, p, w] = xyzrpw
    a = r * math.pi / 180.0
    b = p * math.pi / 180.0
    c = w * math.pi / 180.0
    ca = math.cos(a)
    sa = math.sin(a)
    cb = math.cos(b)
    sb = math.sin(b)
    cc = math.cos(c)
    sc = math.sin(c)
    return Mat([[ca * cb * cc - sa * sc, -cc * sa - ca * cb * sc, ca * sb, x], [ca * sc + cb * cc * sa, ca * cc - cb * sa * sc, sa * sb, y], [-cc * sb, sb * sc, cb, z], [0.0, 0.0, 0.0, 1.0]])


def Pose_2_Adept(H):
    """Converts a pose to an Adept target

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    x = H[0, 3]
    y = H[1, 3]
    z = H[2, 3]
    if H[2, 2] > (1.0 - 1e-10):
        r = 0
        p = 0
        w = atan2(H[1, 0], H[0, 0])
    elif H[2, 2] < (-1.0 + 1e-10):
        r = 0
        p = pi
        w = atan2(H[1, 0], H[1, 1])
    else:
        cb = H[2, 2]
        sb = +sqrt(1 - cb * cb)
        sc = H[2, 1] / sb
        cc = -H[2, 0] / sb
        sa = H[1, 2] / sb
        ca = H[0, 2] / sb
        r = atan2(sa, ca)
        p = atan2(sb, cb)
        w = atan2(sc, cc)
    return [x, y, z, r * 180 / pi, p * 180 / pi, w * 180 / pi]


def Comau_2_Pose(xyzrpw):
    """Converts a Comau XYZRPW target to a pose (4x4 matrix), the same representation required by PDL Comau programs.

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    return Adept_2_Pose(xyzrpw)


def Pose_2_Comau(H):
    """Converts a pose to a Comau target, the same representation required by PDL Comau programs.

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`"""
    return Pose_2_Adept(H)


def Pose_2_Nachi(pose):
    """Converts a pose to a Nachi XYZRPW target

    :param pose: pose
    :type pose: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    [x, y, z, r, p, w] = pose_2_xyzrpw(pose)
    return [x, y, z, w, p, r]


def Nachi_2_Pose(xyzwpr):
    """Converts a Nachi XYZRPW target to a pose (4x4 matrix)

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    return xyzrpw_2_pose(xyzwpr)


def pose_2_quaternion(Ti):
    """Returns the quaternion orientation vector of a pose (4x4 matrix)

    :param Ti: pose
    :type Ti: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    TOLERANCE_0 = 1e-9
    TOLERANCE_180 = 1e-7

    cosangle = min(max(((Ti[0, 0] + Ti[1, 1] + Ti[2, 2] - 1.0) * 0.5), -1.0), 1.0)  # Calculate the rotation angle
    if cosangle > 1.0 - TOLERANCE_0:
        # Identity matrix
        q1 = 1.0
        q2 = 0.0
        q3 = 0.0
        q4 = 0.0

    elif cosangle < -1.0 + TOLERANCE_180:
        # 180 rotation around an axis
        diag = [Ti[0, 0], Ti[1, 1], Ti[2, 2]]
        k = diag.index(max(diag))
        col = [Ti[0, k], Ti[1, k], Ti[2, k]]
        col[k] = col[k] + 1.0
        rotvector = [n / sqrtA(2.0 * (1.0 + diag[k])) for n in col]

        q1 = 0.0
        q2 = rotvector[0]
        q3 = rotvector[1]
        q4 = rotvector[2]

    else:
        # No edge case, normal calculation
        a = Ti[0, 0]
        b = Ti[1, 1]
        c = Ti[2, 2]
        sign2 = 1.0
        sign3 = 1.0
        sign4 = 1.0
        if Ti[2, 1] - Ti[1, 2] < 0.0:
            sign2 = -1.0
        if Ti[0, 2] - Ti[2, 0] < 0.0:
            sign3 = -1.0
        if Ti[1, 0] - Ti[0, 1] < 0.0:
            sign4 = -1.0
        q1 =         sqrt(max( a + b + c + 1.0, 0.0)) / 2.0
        q2 = sign2 * sqrt(max( a - b - c + 1.0, 0.0)) / 2.0
        q3 = sign3 * sqrt(max(-a + b - c + 1.0, 0.0)) / 2.0
        q4 = sign4 * sqrt(max(-a - b + c + 1.0, 0.0)) / 2.0

    return [q1, q2, q3, q4]


def Pose_Split(pose1, pose2, delta_mm=1.0):
    """Create a sequence of poses that transitions from pose1 to pose2 by steps of delta_mm in mm (the first and last pose are not included in the list)"""
    pose_delta = invH(pose1) * pose2
    distance = norm(pose_delta.Pos())
    if distance <= delta_mm:
        return [pose2]

    pose_list = []

    x, y, z, w, p, r = Pose_2_UR(pose_delta)

    steps = max(1, int(distance / delta_mm))

    xd = x / steps
    yd = y / steps
    zd = z / steps
    wd = w / steps
    pd = p / steps
    rd = r / steps
    for i in range(steps - 1):
        factor = i + 1
        pose_list.append(pose1 * UR_2_Pose([xd * factor, yd * factor, zd * factor, wd * factor, pd * factor, rd * factor]))

    return pose_list


def quaternion_2_pose(qin):
    """Returns the pose orientation matrix (4x4 matrix) given a quaternion orientation vector

    :param list qin: quaternions as 4 float values

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    qnorm = sqrt(qin[0] * qin[0] + qin[1] * qin[1] + qin[2] * qin[2] + qin[3] * qin[3])
    q = qin
    q[0] = q[0] / qnorm
    q[1] = q[1] / qnorm
    q[2] = q[2] / qnorm
    q[3] = q[3] / qnorm
    pose = Mat([[1 - 2*q[2]*q[2] - 2*q[3]*q[3], 2*q[1]*q[2] - 2*q[3]*q[0],     2*q[1]*q[3] + 2*q[2]*q[0],     0],
                [2*q[1]*q[2] + 2*q[3]*q[0],     1 - 2*q[1]*q[1] - 2*q[3]*q[3], 2*q[2]*q[3] - 2*q[1]*q[0],     0],
                [2*q[1]*q[3] - 2*q[2]*q[0],     2*q[2]*q[3] + 2*q[1]*q[0],     1 - 2*q[1]*q[1] - 2*q[2]*q[2], 0],
                [0,                             0,                             0,                             1]])
    return pose


def Pose_2_ABB(H):
    """Converts a pose to an ABB target (using quaternion representation).

    :param H: pose
    :type H: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    q = pose_2_quaternion(H)
    return [H[0, 3], H[1, 3], H[2, 3], q[0], q[1], q[2], q[3]]


def print_pose_ABB(pose):
    """Displays an ABB RAPID target (the same way it is displayed in IRC5 controllers).

    :param pose: pose
    :type pose: :class:`.Mat`

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    q = pose_2_quaternion(pose)
    print('[[%.3f,%.3f,%.3f],[%.6f,%.6f,%.6f,%.6f]]' % (pose[0, 3], pose[1, 3], pose[2, 3], q[0], q[1], q[2], q[3]))


def Pose_2_UR(pose):
    """Calculate the p[x,y,z,u,v,w] position with rotation vector for a pose target. This is the same format required by Universal Robot controllers.

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`
    """
    NUMERIC_TOLERANCE = 1e-8

    def saturate_1(value):
        return min(max(value, -1.0), 1.0)

    angle = acos(saturate_1((pose[0, 0] + pose[1, 1] + pose[2, 2] - 1) * 0.5))
    rxyz = [pose[2, 1] - pose[1, 2], pose[0, 2] - pose[2, 0], pose[1, 0] - pose[0, 1]]
    if angle < NUMERIC_TOLERANCE:
        rxyz = [0, 0, 0]
    else:
        sin_angle = sin(angle)
        if abs(sin_angle) < NUMERIC_TOLERANCE or norm(rxyz) < NUMERIC_TOLERANCE:
            d3 = [pose[0, 0], pose[1, 1], pose[2, 2]]
            mx = max(d3)
            mx_id = d3.index(mx)
            if mx_id == 0:
                rxyz = [pose[0, 0] + 1, pose[1, 0], pose[2, 0]]
            elif mx_id == 1:
                rxyz = [pose[0, 1], pose[1, 1] + 1, pose[2, 1]]
            else:
                rxyz = [pose[0, 2], pose[1, 2], pose[2, 2] + 1]

            rxyz = mult3(rxyz, angle / (sqrt(max(0, 2 * (1 + mx)))))
        else:
            rxyz = normalize3(rxyz)
            rxyz = mult3(rxyz, angle)
    return [pose[0, 3], pose[1, 3], pose[2, 3], rxyz[0], rxyz[1], rxyz[2]]


def UR_2_Pose(xyzwpr):
    """Calculate the pose target given a p[x,y,z,u,v,w] cartesian target with rotation vector. This is the same format required by Universal Robot controllers.

    .. seealso:: :class:`.Mat`, :func:`~robodk.robomath.TxyzRxyz_2_Pose`
    """
    x, y, z, w, p, r = xyzwpr
    wpr = [w, p, r]
    angle = norm(wpr)
    cosang = cos(0.5 * angle)

    if angle == 0.0:
        q234 = [0.0, 0.0, 0.0]
    else:
        ratio = sin(0.5 * angle) / angle
        q234 = mult3(wpr, ratio)

    q1234 = [cosang, q234[0], q234[1], q234[2]]
    pose = quaternion_2_pose(q1234)
    pose.setPos([x, y, z])
    return pose


#----------------------------------------------------
#-------- ROBOT MODEL (D-H and D-H M) ---------------


def dh(rz, tx=None, tz=None, rx=None):
    """Returns the Denavit-Hartenberg 4x4 matrix for a robot link.
    calling dh(rz,tx,tz,rx) is the same as using rotz(rz)*transl(tx,0,tz)*rotx(rx)
    calling dh(rz,tx,tz,rx) is the same as calling dh([rz,tx,tz,rx])
    """
    if tx is None:
        [rz, tx, tz, rx] = rz

    crx = math.cos(rx)
    srx = math.sin(rx)
    crz = math.cos(rz)
    srz = math.sin(rz)
    return Mat( [[crz, -srz*crx,  srz*srx, tx*crz],
                 [srz,  crz*crx, -crz*srx, tx*srz],
                 [  0,      srx,      crx,     tz],
                 [  0,        0,        0,      1]])

def dhm(rx, tx=None, tz=None, rz=None):
    """Returns the Denavit-Hartenberg Modified 4x4 matrix for a robot link (Craig 1986).

    calling dhm(rx,tx,tz,rz) is the same as using rotx(rx)*transl(tx,0,tz)*rotz(rz)

    calling dhm(rx,tx,tz,rz) is the same as calling dhm([rx,tx,tz,rz])
    """
    if tx is None:
        [rx, tx, tz, rz] = rx

    crx = math.cos(rx)
    srx = math.sin(rx)
    crz = math.cos(rz)
    srz = math.sin(rz)
    return Mat([[crz,        -srz,    0,      tx],
                [crx*srz, crx*crz, -srx, -tz*srx],
                [srx*srz, crz*srx,  crx,  tz*crx],
                [      0,       0,    0,       1]])

def joints_2_angles(jin, type):
    """Converts the robot encoders into angles between links depending on the type of the robot."""
    jout = jin
    if type == 2:
        jout[2] = -jin[1] - jin[2]
        jout[3] = -jin[3]
        jout[4] = -jin[4]
        jout[5] = -jin[5]
    elif type == 3:
        jout[2] = -jin[2]
        jout[3] = -jin[3]
        jout[4] = -jin[4]
        jout[5] = -jin[5]
    elif type == 4:
        jout[2] = +jin[1] + jin[2]
    elif type == 11:
        jout[2] = -jin[1] - jin[2]
        jout[0] = -jin[0]
        jout[3] = -jin[3]
        jout[5] = -jin[5]
    return jout


def angles_2_joints(jin, type):
    """Converts the angles between links into the robot motor space depending on the type of the robot."""
    jout = jin
    if type == 2:
        jout[2] = -jin[1] - jin[2]
        jout[3] = -jin[3]
        jout[4] = -jin[4]
        jout[5] = -jin[5]
    elif type == 3:
        jout[2] = -jin[2]
        jout[3] = -jin[3]
        jout[4] = -jin[4]
        jout[5] = -jin[5]
    elif type == 11:
        jout[2] = -jin[1] - jin[2]
        jout[0] = -jin[0]
        jout[3] = -jin[3]
        jout[5] = -jin[5]
    return jout


#----------------------------------------------------
#-------- Useful geometric tools ---------------


def norm(p):
    """Returns the norm of a 3D vector"""
    return sqrt(p[0] * p[0] + p[1] * p[1] + p[2] * p[2])


def normalize3(a):
    """Returns the unitary vector"""
    norminv = 1.0 / norm(a)
    return [a[0] * norminv, a[1] * norminv, a[2] * norminv]


def cross(a, b):
    """Returns the cross product of two 3D vectors"""
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]
    return c


def dot(a, b):
    """Returns the dot product of two 3D vectors"""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def angle3(a, b):
    """Returns the angle in radians of two 3D vectors"""
    cos_angle = dot(normalize3(a), normalize3(b))
    cos_angle = min(1.0, max(-1.0, cos_angle))
    return acos(cos_angle)


def pose_angle(pose):
    """Returns the angle in radians of a 4x4 matrix pose

    :param pose: pose
    :type pose: :class:`.Mat`"""
    cos_ang = (pose[0, 0] + pose[1, 1] + pose[2, 2] - 1) / 2
    cos_ang = min(max(cos_ang, -1), 1)
    return acos(cos_ang)


def pose_angle_between(pose1, pose2):
    """Returns the angle in radians between two poses (4x4 matrix pose)"""
    return pose_angle(invH(pose1) * pose2)


def mult3(v, d):
    """Multiplies a 3D vector to a scalar"""
    return [v[0] * d, v[1] * d, v[2] * d]


def subs3(a, b):
    """Subtracts two 3D vectors c=a-b"""
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]


def add3(a, b):
    """Adds two 3D vectors c=a+b"""
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]


def distance(a, b):
    """Calculates the distance between two points"""
    return norm(subs3(a, b))


def pose_is_similar(a, b, tolerance=0.1):
    """Check if the pose is similar. Returns True if both poses are less than 0.1 mm or 0.1 deg appart. Optionally provide the tolerance in mm+deg"""
    if distance(a.Pos(), b.Pos()) + pose_angle_between(a, b) * 180 / pi < tolerance:
        return True
    return False


def intersect_line_2_plane(pline, vline, pplane, vplane):
    """Calculates the intersection betweeen a line and a plane"""
    D = -dot(vplane, pplane)
    k = -(D + dot(vplane, pline)) / dot(vplane, vline)
    p = add3(pline, mult3(vline, k))
    return p


def proj_pt_2_plane(point, planepoint, planeABC):
    """Projects a point to a plane"""
    return intersect_line_2_plane(point, planeABC, planepoint, planeABC)


def proj_pt_2_line(point, paxe, vaxe):
    """Projects a point to a line"""
    vpaxe2point = subs3(point, paxe)
    dist = dot(vaxe, vpaxe2point) / dot(vaxe, vaxe)
    return add3(paxe, mult3(vaxe, dist))


def fitPlane(points):
    """Best fits a plane to a cloud of points"""
    import numpy as np
    XYZ = np.array(points)
    [rows, cols] = XYZ.shape
    # Set up constraint equations of the form  AB = 0,
    # where B is a column vector of the plane coefficients
    # in the form b(1)*X + b(2)*Y +b(3)*Z + b(4) = 0.
    p = (np.ones((rows, 1)))
    AB = np.hstack([XYZ, p])
    [u, d, v] = np.linalg.svd(AB, 0)
    B = v[3, :]  # Solution is last column of v.
    nn = np.linalg.norm(B[0:3])
    B = B / nn
    #pplane = [0, 0, -(B[3] / B[2])]
    pplane = np.average(XYZ, 0)
    vplane = B[0:3].tolist()
    return pplane, vplane


#----------------------------------------------------
#--------       Mat matrix class      ---------------


class MatrixError(Exception):
    """ An exception class for Matrix """
    pass


class Mat(object):
    """Mat is a matrix object. The main purpose of this object is to represent a pose in the 3D space (position and orientation).

    A pose is a 4x4 matrix that represents the position and orientation of one reference frame with respect to another one, in the 3D space.

    Poses are commonly used in robotics to place objects, reference frames and targets with respect to each other.

    .. seealso:: :func:`~robodk.robomath.TxyzRxyz_2_Pose`, :func:`~robodk.robomath.Pose_2_TxyzRxyz`, :func:`~robodk.robomath.Pose_2_ABB`, :func:`~robodk.robomath.Pose_2_Adept`, :func:`~robodk.robomath.Adept_2_Pose`, :func:`~robodk.robomath.Pose_2_Comau`, :func:`~robodk.robomath.Pose_2_Fanuc`, :func:`~robodk.robomath.Pose_2_KUKA`, :func:`~robodk.robomath.KUKA_2_Pose`, :func:`~robodk.robomath.Pose_2_Motoman`, :func:`~robodk.robomath.Pose_2_Nachi`, :func:`~robodk.robomath.Pose_2_Staubli`, :func:`~robodk.robomath.Pose_2_UR`, :func:`~robodk.robomath.quaternion_2_pose`

    Example:

        .. code-block:: python

            from robodk.robolink import *           # import the robolink library
            from robodk.robomath import *           # import the robomath library

            RDK = Robolink()                        # connect to the RoboDK API
            robot  = RDK.Item('', ITEM_TYPE_ROBOT)  # Retrieve a robot available in RoboDK
            #target  = RDK.Item('Target 1')         # Retrieve a target (example)


            pose = robot.Pose()                     # retrieve the current robot position as a pose (position of the active tool with respect to the active reference frame)
            # target = target.Pose()                # the same can be applied to targets (taught position)

            # Read the 4x4 pose matrix as [X,Y,Z , A,B,C] Euler representation (mm and deg): same representation as KUKA robots
            XYZABC = Pose_2_KUKA(pose)
            print(XYZABC)

            # Read the 4x4 pose matrix as [X,Y,Z, q1,q2,q3,q4] quaternion representation (position in mm and orientation in quaternion): same representation as ABB robots (RAPID programming)
            xyzq1234 = Pose_2_ABB(pose)
            print(xyzq1234)

            # Read the 4x4 pose matrix as [X,Y,Z, u,v,w] representation (position in mm and orientation vector in radians): same representation as Universal Robots
            xyzuvw = Pose_2_UR(pose)
            print(xyzuvw)

            x,y,z,a,b,c = XYZABC                    # Use the KUKA representation (for example) and calculate a new pose based on the previous pose
            XYZABC2 = [x,y,z+50,a,b,c+45]
            pose2 = KUKA_2_Pose(XYZABC2)            # Convert the XYZABC array to a pose (4x4 matrix)

            robot.MoveJ(pose2)                      # Make a joint move to the new position
            # target.setPose(pose2)                  # We can also update the pose to targets, tools, reference frames, objects, ...
    """

    def __init__(self, rows=None, ncols=None):
        if ncols is None:
            if rows is None:
                m = 4
                n = 4
                self.rows = [[0] * n for x in range(m)]
            else:
                if isinstance(rows, Mat):
                    rows = rows.copy().rows
                m = len(rows)
                transpose = 0
                if isinstance(rows, list) and len(rows) == 0:
                    # Check empty matrix
                    self.rows = [[]]
                    n = 0
                    return

                if not isinstance(rows[0], list):
                    rows = [rows]
                    transpose = 1

                n = len(rows[0])
                if any([len(row) != n for row in rows[1:]]):  # Validity check
                    #raise Exception(MatrixError, "inconsistent row length")
                    # make the size uniform (fill blanks with zeros)
                    n = max([len(i) for i in rows])
                    for row in rows:
                        row += [0] * (n - len(row))

                self.rows = rows
                if transpose:
                    self.rows = [list(item) for item in zip(*self.rows)]
        else:
            m = max(rows, 0)
            n = max(ncols, 0)
            if m == 0:
                m = 1
                n = 0

            self.rows = [[0] * n for x in range(m)]

    def __iter__(self):
        if self.size(0) == 0 or self.size(1) == 0:
            return iter([])
        return iter(self.tr().rows)

    def copy(self):
        sz = self.size()
        newmat = Mat(sz[0], sz[1])
        for i in range(sz[0]):
            for j in range(sz[1]):
                newmat[i, j] = self[i, j]
        return newmat

    def __len__(self):
        """Return the number of columns"""
        return len(self.rows[0])

    def ColsCount(self):
        """Return the number of coumns. Same as len().

        .. seealso:: :func:`~Mat.Cols`, :func:`~Mat.Rows`, :func:`~Mat.RowsCount`
        """
        return len(self.rows[0])

    def RowsCount(self):
        """Return the number of rows

        .. seealso:: :func:`~Mat.Cols`, :func:`~Mat.Rows`, :func:`~Mat.ColsCount`

        """
        return len(self.rows[0])

    def Cols(self):
        """Retrieve the matrix as a list of columns (list of list of float).

        .. seealso:: :func:`~Mat.Rows`, :func:`~Mat.ColsCount`, :func:`~Mat.RowsCount`

        Example:

            .. code-block:: python

                >>> transl(10,20,30).Rows()
                [[1, 0, 0, 10], [0, 1, 0, 20], [0, 0, 1, 30], [0, 0, 0, 1]]

                >>> transl(10,20,30).Cols()
                [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [10, 20, 30, 1]]
        """
        return self.tr().rows

    def Rows(self):
        """Get the matrix as a list of lists

        .. seealso:: :func:`~Mat.Cols`, :func:`~Mat.ColsCount`, :func:`~Mat.RowsCount`
        """
        return self.rows

    def __getitem__(self, idx):
        if isinstance(idx, int):  #integer A[1]
            return tr(Mat(self.rows[idx]))
        elif isinstance(idx, slice):  #one slice: A[1:3]
            return Mat(self.rows[idx])
        else:  #two slices: A[1:3,1:3]
            idx1 = idx[0]
            idx2 = idx[1]
            if isinstance(idx1, int) and isinstance(idx2, int):
                return self.rows[idx1][idx2]
            matsize = self.size()
            if isinstance(idx1, slice):
                indices1 = idx1.indices(matsize[0])
                rg1 = range(*indices1)
            else:  #is int
                rg1 = range(idx1, idx1 + 1)
            if isinstance(idx2, slice):
                indices2 = idx2.indices(matsize[1])
                rg2 = range(*indices2)
            else:  #is int
                rg2 = range(idx2, idx2 + 1)
            #newm = int(abs((rg1.stop-rg1.start)/rg1.step))
            #newn = int(abs((rg2.stop-rg2.start)/rg2.step))
            newm = rg1
            newn = rg2
            newmat = Mat(len(newm), len(newn))
            cm = 0
            for i in rg1:
                cn = 0
                for j in rg2:
                    newmat.rows[cm][cn] = self.rows[i][j]
                    cn = cn + 1
                cm = cm + 1
            return newmat

    def __setitem__(self, idx, item):
        if isinstance(item, float) or isinstance(item, int):
            item = Mat([[item]])
        elif isinstance(item, list):
            item = Mat(item)

        matsize = self.size()
        if isinstance(idx, int):  #integer A[1]
            idx1 = idx
            idx2 = 0
            #raise Exception(MatrixError, "Cannot set item. Use [i,:] instead.")
            #self.rows[idx] = item
        elif isinstance(idx, slice):  #one slice: A[1:3]
            # raise Exception(MatrixError, "Cannot set item. Use [a:b,:] instead.")
            idx1 = idx
            idx2 = 0
        else:
            idx1 = idx[0]
            idx2 = idx[1]

        # at this point we have two slices: example A[1:3,1:3]
        if isinstance(idx1, slice):
            indices1 = idx1.indices(matsize[0])
            rg1 = range(*indices1)
        else:  #is int
            rg1 = range(idx1, idx1 + 1)
        if isinstance(idx2, slice):
            indices2 = idx2.indices(matsize[1])
            rg2 = range(*indices2)
        else:  #is int
            rg2 = range(idx2, idx2 + 1)
        #newm = int(abs((rg1.stop-rg1.start)/rg1.step))
        #newn = int(abs((rg2.stop-rg2.start)/rg2.step))
        newm = rg1
        newn = rg2
        itmsz = item.size()
        if len(newm) != itmsz[0] or len(newn) != itmsz[1]:
            raise Exception(MatrixError, "Submatrix indices does not match the new matrix sizes", itmsz[0], "x", itmsz[1], "<-", newm, "x", newn)
        #newmat = Mat(newm,newn)
        cm = 0
        for i in rg1:
            cn = 0
            for j in rg2:
                self.rows[i][j] = item.rows[cm][cn]
                cn = cn + 1
            cm = cm + 1

    def __str__(self):
        #s='\n [ '.join([(', '.join([str(item) for item in row])+' ],') for row in self.rows])
        str_add = ''
        if self.isHomogeneous():
            x, y, z, rx, ry, rz = Pose_2_TxyzRxyz(self)
            str_add = 'Pose(%.3f, %.3f, %.3f,  %.3f, %.3f, %.3f):\n' % (x, y, z, rx * 180 / pi, ry * 180 / pi, rz * 180 / pi)

        s = '\n [ '.join([(', '.join([('%.3f' % item if type(item) == float else str(item)) for item in row]) + ' ],') for row in self.rows])
        return str_add + '[[ ' + s[:-1] + ']\n'

    def __repr__(self):
        s = str(self)
        rank = str(self.size())
        rep = "Matrix: %s\n%s" % (rank, s)
        return rep

    def tr(self):
        """Returns the transpose of the matrix"""
        if self.size(0) == 0 or self.size(1) == 0:
            return Mat(0, 0)
        mat = Mat([list(item) for item in zip(*self.rows)])
        return mat

    def size(self, dim=None):
        """Returns the size of a matrix (m,n).
        Dim can be set to 0 to return m (rows) or 1 to return n (columns)"""
        m = len(self.rows)
        if m > 0:
            n = len(self.rows[0])
        else:
            n = 0

        if dim is None:
            return (m, n)
        elif dim == 0:
            return m
        elif dim == 1:
            return n
        else:
            raise Exception(MatrixError, "Invalid dimension!")

    def catV(self, mat2):
        """Concatenate with another matrix (vertical concatenation)"""
        if not isinstance(mat2, Mat):
            #raise Exception(MatrixError, "Concatenation must be performed with 2 matrices")
            return self.catH(Mat(mat2).tr())

        sz1 = self.size()
        sz2 = mat2.size()
        if sz1[1] != sz2[1]:
            raise Exception(MatrixError, "Horizontal size of matrices does not match")

        newmat = Mat(sz1[0] + sz2[0], sz1[1])
        newmat[0:sz1[0], :] = self
        newmat[sz1[0]:, :] = mat2
        return newmat

    def catH(self, mat2):
        """Concatenate with another matrix (horizontal concatenation)"""
        if not isinstance(mat2, Mat):
            #raise Exception(MatrixError, "Concatenation must be performed with 2 matrices")
            return self.catH(Mat(mat2))

        sz1 = self.size()
        sz2 = mat2.size()
        if sz1[0] != sz2[0]:
            raise Exception(MatrixError, "Horizontal size of matrices does not match")

        newmat = Mat(sz1[0], sz1[1] + sz2[1])
        newmat[:, :sz1[1]] = self
        newmat[:, sz1[1]:] = mat2
        return newmat

    def __eq__(self, other):
        """Test equality"""
        if other is None:
            return False
        #return (other.rows == self.rows)
        return pose_is_similar(other, self)

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, mat):
        """Add a matrix to this matrix and
        return the new matrix. It doesn't modify
        the current matrix"""
        if isinstance(mat, int) or isinstance(mat, float):
            m, n = self.size()
            result = Mat(m, n)
            for x in range(m):
                for y in range(n):
                    result.rows[x][y] = self.rows[x][y] + mat
            return result
        sz = self.size()
        m = sz[0]
        n = sz[1]
        ret = Mat(m, n)
        if sz != mat.size():
            raise Exception(MatrixError, "Can not add matrices of sifferent sizes!")
        for x in range(m):
            row = [sum(item) for item in zip(self.rows[x], mat.rows[x])]
            ret.rows[x] = row
        return ret

    def __sub__(self, mat):
        """Subtract a matrix from this matrix and
        return the new matrix. It doesn't modify
        the current matrix"""
        if isinstance(mat, int) or isinstance(mat, float):
            m, n = self.size()
            result = Mat(m, n)
            for x in range(m):
                for y in range(n):
                    result.rows[x][y] = self.rows[x][y] - mat
            return result
        sz = self.size()
        m = sz[0]
        n = sz[1]
        ret = Mat(m, n)
        if sz != mat.size():
            raise Exception(MatrixError, "Can not subtract matrices of sifferent sizes!")
        for x in range(m):
            row = [item[0] - item[1] for item in zip(self.rows[x], mat.rows[x])]
            ret.rows[x] = row
        return ret

    def __mul__(self, mat):
        """Multiply a matrix with this matrix and
        return the new matrix. It doesn't modify
        the current matrix"""
        if isinstance(mat, int) or isinstance(mat, float):
            m, n = self.size()
            mulmat = Mat(m, n)
            for x in range(m):
                for y in range(n):
                    mulmat.rows[x][y] = self.rows[x][y] * mat
            return mulmat
        if isinstance(mat, list):  #case of a matrix times a vector
            szvect = len(mat)
            m = self.size(0)
            matvect = Mat(mat)
            if szvect + 1 == m:
                vectok = catV(matvect, Mat([[1]]))
                result = self * vectok
                return (result[:-1, :]).tr().rows[0]
            elif szvect == m:
                result = self * Mat(matvect)
                return result.tr().rows[0]
            else:
                raise Exception(MatrixError, "Invalid product")
        else:
            matm, matn = mat.size()
            m, n = self.size()
            if (n != matm):
                raise Exception(MatrixError, "Matrices cannot be multipled (unexpected size)!")
            mat_t = mat.tr()
            mulmat = Mat(m, matn)
            for x in range(m):
                for y in range(mat_t.size(0)):
                    mulmat.rows[x][y] = sum([item[0] * item[1] for item in zip(self.rows[x], mat_t.rows[y])])
            return mulmat

    def eye(self, m=4):
        """Make identity matrix of size (mxm)"""
        rows = [[0] * m for x in range(m)]
        idx = 0
        for row in rows:
            row[idx] = 1
            idx += 1
        return Mat(rows)

    def isHomogeneous(self):
        """returns 1 if it is a Homogeneous matrix"""
        m, n = self.size()
        if m != 4 or n != 4:
            return False
        #if self[3,:] != Mat([[0.0,0.0,0.0,1.0]]):
        #    return False
        test = self[0:3, 0:3]
        test = test * test.tr()
        test[0, 0] = test[0, 0] - 1.0
        test[1, 1] = test[1, 1] - 1.0
        test[2, 2] = test[2, 2] - 1.0
        zero = 0.0
        for x in range(3):
            for y in range(3):
                zero = zero + abs(test[x, y])
        if zero > 1e-4:
            return False
        return True

    def RelTool(self, x, y, z, rx=0, ry=0, rz=0):
        """Calculates a relative target with respect to the tool coordinates. This procedure has exactly the same behavior as ABB's RelTool instruction.
        X,Y,Z are in mm, RX,RY,RZ are in degrees.

        :param float x: translation along the Tool X axis (mm)
        :param float y: translation along the Tool Y axis (mm)
        :param float z: translation along the Tool Z axis (mm)
        :param float rx: rotation around the Tool X axis (deg) (optional)
        :param float ry: rotation around the Tool Y axis (deg) (optional)
        :param float rz: rotation around the Tool Z axis (deg) (optional)

        .. seealso:: :func:`~Mat.Offset`
        """
        return RelTool(self, x, y, z, rx, ry, rz)

    def Offset(self, x, y, z, rx=0, ry=0, rz=0):
        """Calculates a relative target with respect to this pose.
        X,Y,Z are in mm, RX,RY,RZ are in degrees.

        :param float x: translation along the Reference X axis (mm)
        :param float y: translation along the Reference Y axis (mm)
        :param float z: translation along the Reference Z axis (mm)
        :param float rx: rotation around the Reference X axis (deg) (optional)
        :param float ry: rotation around the Reference Y axis (deg) (optional)
        :param float rz: rotation around the Reference Z axis (deg) (optional)

        .. seealso:: :func:`~Mat.RelTool`
        """
        return Offset(self, x, y, z, rx, ry, rz)

    def invH(self):
        """Returns the inverse of this pose (homogeneous matrix assumed)"""
        if not self.isHomogeneous():
            raise Exception(MatrixError, "Pose matrix is not homogeneous. invH() can only compute the inverse of a homogeneous matrix")
        Hout = self.tr()
        Hout[3, 0:3] = Mat([[0, 0, 0]])
        Hout[0:3, 3] = (Hout[0:3, 0:3] * self[0:3, 3]) * (-1)
        return Hout

    def inv(self):
        """Returns the inverse of this pose (homogeneous matrix assumed)"""
        return self.invH()

    def tolist(self):
        """Returns the first column of the matrix as a list"""
        return tr(self).rows[0]

    def list(self):
        """Returns the first column of the matrix as a list"""
        return tr(self).rows[0]

    def list2(self):
        """Returns the matrix as list of lists (one list per column)"""
        return tr(self).rows

    def Pos(self):
        """Returns the position of a pose (assumes that a 4x4 homogeneous matrix is being used)"""
        return self[0:3, 3].tolist()

    def VX(self):
        """Returns the X vector of a pose (assumes that a 4x4 homogeneous matrix is being used)"""
        return self[0:3, 0].tolist()

    def VY(self):
        """Returns the Y vector of a pose (assumes that a 4x4 homogeneous matrix is being used)"""
        return self[0:3, 1].tolist()

    def VZ(self):
        """Returns the Z vector of a pose (assumes that a 4x4 homogeneous matrix is being used)"""
        return self[0:3, 2].tolist()

    def Rot33(self):
        """Returns the sub 3x3 rotation matrix"""
        return self[0:3, 0:3]

    def setPos(self, newpos):
        """Sets the XYZ position of a pose (assumes that a 4x4 homogeneous matrix is being used)"""
        self[0, 3] = newpos[0]
        self[1, 3] = newpos[1]
        self[2, 3] = newpos[2]
        return self

    def setVX(self, v_xyz):
        """Sets the VX vector of a pose, which is the first column of a homogeneous matrix (assumes that a 4x4 homogeneous matrix is being used)"""
        v_xyz = normalize3(v_xyz)
        self[0, 0] = v_xyz[0]
        self[1, 0] = v_xyz[1]
        self[2, 0] = v_xyz[2]
        return self

    def setVY(self, v_xyz):
        """Sets the VY vector of a pose, which is the first column of a homogeneous matrix (assumes that a 4x4 homogeneous matrix is being used)"""
        v_xyz = normalize3(v_xyz)
        self[0, 1] = v_xyz[0]
        self[1, 1] = v_xyz[1]
        self[2, 1] = v_xyz[2]
        return self

    def setVZ(self, v_xyz):
        """Sets the VZ vector of a pose, which is the first column of a homogeneous matrix (assumes that a 4x4 homogeneous matrix is being used)"""
        v_xyz = normalize3(v_xyz)
        self[0, 2] = v_xyz[0]
        self[1, 2] = v_xyz[1]
        self[2, 2] = v_xyz[2]
        return self

    def translationPose(self):
        """Return the translation pose of this matrix. The rotation returned is set to identity (assumes that a 4x4 homogeneous matrix is being used)"""
        return transl(self.Pos())

    def rotationPose(self):
        """Return the rotation pose of this matrix. The position returned is set to [0,0,0] (assumes that a 4x4 homogeneous matrix is being used)"""
        mat_rotation = Mat(self)
        mat_rotation.setPos([0, 0, 0])
        return mat_rotation

    def SaveCSV(self, strfile):
        """Save the :class:`.Mat` Matrix to a CSV (Comma Separated Values) file. The file can be easily opened as a spreadsheet such as Excel.

        .. seealso:: :func:`~Mat.SaveMat`, :func:`~robodk.robomath.SaveList`, :func:`~robodk.robomath.LoadList`, :func:`~robodk.robomath.LoadMat`
        """
        self.tr().SaveMat(strfile)

    def SaveMat(self, strfile, separator=','):
        """Save the :class:`.Mat` Matrix to a CSV or TXT file

        .. seealso:: :func:`~Mat.SaveCSV`, :func:`~robodk.robomath.SaveList`, :func:`~robodk.robomath.LoadList`, :func:`~robodk.robomath.LoadMat`
        """
        sz = self.size()
        m = sz[0]
        n = sz[1]
        file = open(strfile, 'w')
        for j in range(n):
            for i in range(m):
                file.write(('%.6f' + separator) % self.rows[i][j])
            file.write('\n')
        file.close()


if __name__ == "__main__":
    pass