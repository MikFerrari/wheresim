import numpy as np
from os import getenv as _getenv
from os import path as _path

# The online URDF of Aliengo has unbounded joints, which are represented using sine and cosine of the joint angle
foot_names = ["FL", "FR", "RL", "RR"]

# configuration for LIPM trajectory optimization
# ----------------------------------------------
wu = 1e1    # CoP error squared cost weight
wc = 0      # CoM position error squared cost weight
wdc = 1e-1  # CoM velocity error squared cost weight
wp = 1e-2   # footstep distance to hip cost weight
g = 9.81    # norm of the gravity vector
foot_step_0 = ["FL", "RR"]  # initial foot steps on the ground
dt_mpc = 0.1  # sampling time interval
T_step = 0.4  # time needed for every step
step_height = 0.1  # fixed step height
step_length = 0.05
nb_steps = 6  # number of desired walking steps

# configuration for controller
# ----------------------------------------------
dt = 0.002

# configuration for the TSID whole-body controller
# ----------------------------------------------
# mapping between the LIP footstep names and the urdf contact frame names
foot_frames = {"FL": "lf_foot", "FR": "rf_foot", "RL": "lh_foot", "RR": "rh_foot"}

urdf = _path.join(_getenv('LOCOSIM_DIR', ''), 'robot_urdf', 'aliengo.urdf')
path = _path.join(_getenv('LOCOSIM_DIR', ''), 'robot_urdf')

mu = 0.8                        # friction coefficient
fMin = 1.0                      # minimum normal contact force
fMax = 300.0                    # maximum normal contact force
contactNormal = np.array([0., 0., 1.])

kp_contact = 30.0               # proportional gain of the rigid contact constraint
# NOTE: with 4 simultaneous point contacts (quadruped stance) forcing an exact
# hard (rigid) equality on every contact over-constrains the system and can
# make the QP infeasible together with the unilateral force bounds; use a
# soft contact weight instead, like the walking example (romeo_conf.py) does.

#contact motion constraint (soft)
w_contact = 1e02                 # weight of the contact motion constraint (soft)
w_forceRef = 1e-5               # weight of the contact force regularization task
contact_transition_time = 0.1   # ramp-down duration [s] when a foot lifts off, to avoid an instantaneous force jump onto the remaining stance leg(s)

# CoM and posture tasks
kp_com = 50.0                   # proportional gain of the CoM task
w_com = 10.0                     # weight of the CoM task

#postural task
kp_posture = 1.0                # proportional gain of the postural task
w_posture = 1e-3                # weight of the postural task

#swing foot task
kp_foot = 300.0                 # proportional gain of the swing foot task
w_foot = 10.0                    # weight of the swing foot task

#orientation task
base_frame_name = "base_link"   # frame used to keep the trunk level (roll/pitch)
kp_base = 100.0                 # proportional gain of the base orientation task
w_base = 10.0                    # weight of the base orientation task