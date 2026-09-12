"""
TSID whole-body controller for a trotting quadruped.

Structure inspired by:
 - demo_quadruped.py -> use of tsid.ContactPoint for the (point) feet contacts
 - reactive_control/tsid/tsid_biped.py & ex_4_biped_walking.py -> overall
   task/contact setup and the add_contact/remove_contact pattern used to
   switch a foot between "in contact" (rigid contact constraint) and
   "swinging" (SE3 motion task), apart from the fact that here the feet are
   modeled as point contacts (3d) instead of 6d rectangular contacts, so the
   swing foot task only tracks position (linear part of the SE3 task).
"""
import numpy as np
import pinocchio as pin
import tsid


class TsidQuadruped:
    """
    - Center of mass task (tracks the CoM trajectory coming from the LIP
      trajectory optimization + interpolation)
    - Joint posture task (regularization, keeps the robot close to q0)
    - One point (3d) rigid contact per stance foot
    - One SE3 (position only) task per swing foot
    """

    def __init__(self, conf, q0, v0):
        self.conf = conf
        self.robot = tsid.RobotWrapper(conf.urdf, [conf.path], pin.JointModelFreeFlyer(), False)
        robot = self.robot
        self.model = robot.model()

        for frame_name in conf.foot_frames.values():
            assert self.model.existFrame(frame_name), f"frame {frame_name} not found in the urdf"

        formulation = tsid.InverseDynamicsFormulationAccForce("tsid", robot, False)
        formulation.computeProblemData(0.0, q0, v0)
        data = formulation.data()

        # one point contact per foot -----------------------------------
        self.contacts, self.contact_active, self.foot_frame_id = {}, {}, {}
        for foot_name, frame_name in conf.foot_frames.items():
            frame_id = self.model.getFrameId(frame_name)
            self.foot_frame_id[foot_name] = frame_id

            contact = tsid.ContactPoint("contact_" + foot_name, robot, frame_name,
                                         conf.contactNormal, conf.mu, conf.fMin, conf.fMax)
            contact.setKp(conf.kp_contact * np.ones(3))
            contact.setKd(2.0 * np.sqrt(conf.kp_contact) * np.ones(3))
            contact.useLocalFrame(False)
            H_ref = robot.framePosition(data, frame_id)
            contact.setReference(H_ref)
            if conf.w_contact >= 0.0:
                formulation.addRigidContact(contact, conf.w_forceRef, conf.w_contact, 1)
            else:
                formulation.addRigidContact(contact, conf.w_forceRef)

            self.contacts[foot_name] = contact
            self.contact_active[foot_name] = True

        # CoM task --------------------------------------------------------
        comTask = tsid.TaskComEquality("task-com", robot)
        comTask.setKp(conf.kp_com * np.ones(3))
        comTask.setKd(2.0 * np.sqrt(conf.kp_com) * np.ones(3))
        formulation.addMotionTask(comTask, conf.w_com, 1, 0.0)

        # postural task (regularization) -----------------------------------
        postureTask = tsid.TaskJointPosture("task-posture", robot)
        postureTask.setKp(conf.kp_posture * np.ones(robot.nv - 6))
        postureTask.setKd(2.0 * np.sqrt(conf.kp_posture) * np.ones(robot.nv - 6))
        formulation.addMotionTask(postureTask, conf.w_posture, 1, 0.0)

        # base orientation task (keeps the trunk level: the LIP model says
        # nothing about roll/pitch, and during a trot the 2-point diagonal
        # support gives no static orientation stability by itself)
        baseTask = tsid.TaskSE3Equality("task-base-orientation", robot, conf.base_frame_name)
        baseTask.setKp(conf.kp_base * np.array([0., 0., 0., 1., 1., 1.]))
        baseTask.setKd(2.0 * np.sqrt(conf.kp_base) * np.array([0., 0., 0., 1., 1., 1.]))
        baseTask.setMask(np.array([0., 0., 0., 1., 1., 1.]))
        formulation.addMotionTask(baseTask, conf.w_base, 1, 0.0)
        H_base_ref = robot.framePosition(data, self.model.getFrameId(conf.base_frame_name))
        trajBase = tsid.TrajectorySE3Constant("traj-base-orientation", H_base_ref)
        baseTask.setReference(trajBase.computeNext())

        # one 3d (position only) swing task per foot -----------------------
        self.footTasks, self.footTraj, self.footSample = {}, {}, {}
        for foot_name, frame_name in conf.foot_frames.items():
            footTask = tsid.TaskSE3Equality("task-" + foot_name + "-foot", robot, frame_name)
            footTask.setKp(conf.kp_foot * np.ones(6))
            footTask.setKd(2.0 * np.sqrt(conf.kp_foot) * np.ones(6))
            footTask.setMask(np.array([1., 1., 1., 0., 0., 0.]))
            formulation.addMotionTask(footTask, conf.w_foot, 1, 0.0)

            H_ref = robot.framePosition(data, self.foot_frame_id[foot_name])
            traj = tsid.TrajectorySE3Constant("traj-" + foot_name + "-foot", H_ref)
            sample = traj.computeNext()

            self.footTasks[foot_name] = footTask
            self.footTraj[foot_name] = traj
            self.footSample[foot_name] = sample

        # trajectories/samples used as reference containers -----------------
        com_ref = robot.com(data)
        self.trajCom = tsid.TrajectoryEuclidianConstant("traj_com", com_ref)
        self.sample_com = self.trajCom.computeNext()

        q_ref = q0[7:]
        self.trajPosture = tsid.TrajectoryEuclidianConstant("traj_joint", q_ref)
        postureTask.setReference(self.trajPosture.computeNext())

        self.solver = tsid.SolverHQuadProgFast("qp solver")
        self.solver.resize(formulation.nVar, formulation.nEq, formulation.nIn)

        self.formulation = formulation
        self.comTask = comTask
        self.postureTask = postureTask
        self.baseTask = baseTask
        self.q = q0
        self.v = v0

    # ------------------------------------------------------------------
    # reference setters
    # ------------------------------------------------------------------
    def set_com_ref(self, pos, vel, acc):
        self.sample_com.value(pos)
        self.sample_com.derivative(vel)
        self.sample_com.second_derivative(acc)
        self.comTask.setReference(self.sample_com)

    def set_foot_3d_ref(self, foot_name, pos, vel, acc):
        sample = self.footSample[foot_name]
        p, v, a = sample.value(), sample.derivative(), sample.second_derivative()
        p[:3], v[:3], a[:3] = pos, vel, acc
        sample.value(p)
        sample.derivative(v)
        sample.second_derivative(a)
        self.footTasks[foot_name].setReference(sample)

    # ------------------------------------------------------------------
    # contact switching
    # ------------------------------------------------------------------
    def get_foot_placement(self, foot_name):
        return self.robot.framePosition(self.formulation.data(), self.foot_frame_id[foot_name])

    def remove_contact(self, foot_name, transition_time=0.0):
        if not self.contact_active[foot_name]:
            return
        H_ref = self.get_foot_placement(foot_name)
        self.footTraj[foot_name].setReference(H_ref)
        self.footTasks[foot_name].setReference(self.footTraj[foot_name].computeNext())
        self.formulation.removeRigidContact(self.contacts[foot_name].name, transition_time)
        self.contact_active[foot_name] = False

    def add_contact(self, foot_name):
        if self.contact_active[foot_name]:
            return
        H_ref = self.get_foot_placement(foot_name)
        self.contacts[foot_name].setReference(H_ref)
        if self.conf.w_contact >= 0.0:
            self.formulation.addRigidContact(self.contacts[foot_name], self.conf.w_forceRef, self.conf.w_contact, 1)
        else:
            self.formulation.addRigidContact(self.contacts[foot_name], self.conf.w_forceRef)
        self.contact_active[foot_name] = True

    # ------------------------------------------------------------------
    # solve
    # ------------------------------------------------------------------
    def compute_problem(self, t, q, v):
        return self.formulation.computeProblemData(t, q, v)

    def solve(self, HQPData):
        return self.solver.solve(HQPData)

    def get_torques(self, sol):
        return self.formulation.getActuatorForces(sol)

    def get_contact_force(self, foot_name, sol):
        if self.contact_active[foot_name] and self.formulation.checkContact(self.contacts[foot_name].name, sol):
            return self.formulation.getContactForce(self.contacts[foot_name].name, sol)
        return np.zeros(3)
