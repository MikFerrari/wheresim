# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 18:07:44 2020

@author: mfocchi
"""
import numpy as np

class CollisionCheck:
    def __init__(self, robot):
        self.robot = robot
        half_lenght = self.robot.collision_model.geometryObjects[0].geometry.halfSide[0]
        half_width = self.robot.collision_model.geometryObjects[0].geometry.halfSide[1]
        half_height = self.robot.collision_model.geometryObjects[0].geometry.halfSide[2]
        self.bControlPoints = [np.array([half_lenght, half_width, -half_height]),  # lf_bottom
                               np.array([-half_lenght, half_width, -half_height]),  # lh_bottom
                               np.array([half_lenght, -half_width, -half_height]),  # rf_bottom
                               np.array([-half_lenght, -half_width, -half_height]),  # rf_bottom
                               np.array([half_lenght, half_width, half_height]),  # lf_top
                               np.array([-half_lenght, half_width, half_height]),  # lh_top
                               np.array([half_lenght, -half_width, half_height]),  # rf_top
                               np.array([-half_lenght, -half_width, half_height])]  # rf_top

        self.kfe_idx = [self.robot.model.getFrameId(leg + '_kfe_joint') for leg in ['lf', 'lh', 'rf', 'rh']]

    def checkBaseCollisions(self):
        # base control points
        for i, pt in enumerate(self.bControlPoints):
            wControlPoint = self.mapBaseToWorld(pt)
            if wControlPoint[2] < self.contact_th:
                return True
        return False

    def checkKFECollisions(self):
        # kfe collision
        for i, id in enumerate(self.kfe_idx):
            wKfe_pos = self.mapBaseToWorld(self.robot.data.oMf[id].translation)  # update kin computes quantity in base frame
            if wKfe_pos[2] < self.contact_th:
                return True
        return False

    def checkGroundCollisions(self):
        # retrun codes
        # -1 no collisions
        # base collisions
        # 0 lf_bottom
        # 1 lh_bottom
        # 2 rf_bottom
        # 3 rf_bottom
        # 4 lf_top
        # 5 lh_top
        # 6 rf_top
        # 7 rf_top
        # kfe collisions
        # 8 lf_kfe
        # 9 lf_kfe
        # 10 lf_kfe
        # 11 lf_kfe

        # return True/False

        # base control points
        for i, pt in enumerate(self.bControlPoints):
            wControlPoint = self.mapBaseToWorld(pt)
            if wControlPoint[2] < self.contact_th:
                # return i
                return True

        # kfe collision
        for i, id in enumerate(self.kfe_idx):
            wKfe_pos = self.mapBaseToWorld(self.robot.data.oMf[id].translation)  # update kin computes quantity in base frame
            if wKfe_pos[2] < self.contact_th:
                # return self.bControlPoints+i
                return True

        # return -1
        return False
