# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 09:47:07 2019

@author: student
"""

import numpy as np

robot_params = {}


robot_params['solo'] ={'dt': 0.002,
                       'kp': [5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5., 5.],
                       'kd': [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1],
                       'q_0':  np.array([0,  np.pi/4, -np.pi/2,    0, -np.pi/4,  np.pi/2, -0,  np.pi/4, -np.pi/2, -0, -np.pi/4,  np.pi/2]),
                       'q_fold': np.array([0,  1.57, -3.13, 0,    1.57, -3.13, 0, -1.57, 3.13, 0, -1.57, 3.13]),
                       'joint_names': ['lf_haa_joint', 'lf_hfe_joint', 'lf_kfe_joint',
                                       'lh_haa_joint', 'lh_hfe_joint', 'lh_kfe_joint',
                                       'rf_haa_joint', 'rf_hfe_joint', 'rf_kfe_joint',
                                       'rh_haa_joint', 'rh_hfe_joint', 'rh_kfe_joint'],
                       'ee_frames': ['lf_foot', 'lh_foot', 'rf_foot','rh_foot'],
                       'real_robot': False,
                       'force_th': 2,
                       'spawn_x': 0.0,
                       'spawn_y': 0.0,
                       'spawn_z': 0.3,
                        'buffer_size': 1501} # note the frames are all aligned with base for joints = 0

robot_params['aliengo'] ={'dt': 0.002,
                          'kp': np.array([60., 90., 60.]*4),
                          'kd': np.array([10., 10., 10.]*4),
                          'ki': np.array([0., 0., 0.]*4),

                          'kp_nominal': np.array([21.5, 21.5, 21.5]*4),
                          'kd_nominal': np.array([3.5, 3.5, 3.5]*4),
                          'ki_nominal': np.array([0., 0., 0.]*4),
                          'kp_backup':  np.array([100., 100., 100.]*4),
                          'kd_backup':  np.array([3., 3., 3.]*4),
                          'ki_backup':  np.array([0., 0., 0.]*4),

                          # 'kp': np.array([25., 25., 25.]*4),
                          # 'kd': np.array([2., 2., 2.]*4),
                          # 'ki': np.array([0., 0., 0.]*4),

                          'kp_swing':  np.array([20., 30., 20.]*4),
                          'kd_swing':  np.array([1., 1., 1.]*4),
                          'ki_swing':  np.array([0., 0., 0.]*4),

                          'kp_land': np.array([60., 90., 60.]*4),
                          'kd_land': np.array([10., 10., 10.]*4),
                          'ki_land': np.array([0., 0., 0.]*4),

                          'kp_real': np.array([20., 30., 30.]*4),
                          'kd_real': np.array([1., 1., 1.]*4),
                          'ki_real': np.array([1., 1., 1.]*4),

                          'kp_real_swing':  np.array([15., 20., 20]*4),
                          'kd_real_swing':  np.array([1., 1., 1.]*4),
                          'ki_real_swing':  np.array([0., 0., 0.]*4),

                          'kp_real_land': np.array([15., 15., 15]*4),
                          'kd_real_land': np.array([1., 1., 1.]*4),
                          'ki_real_land': np.array([0., 0., 0.]*4),

                          # SIM ---------------------------

                          # joint pid + wbc (optional)
                          'kp_wbc': np.array([60., 60., 60.]*4),
                          'kd_wbc': np.array([10., 10., 10.]*4),
                          'ki_wbc': np.array([0., 0., 0.]*4),
                          # virtual impedance wrench control
                          'kp_lin': np.array([1000., 1000., 800.]),
                          'kd_lin': np.array([150., 150., 100.]),
                          'kp_ang': np.array([200., 200., 100.]),
                          'kd_ang': np.array([10., 20., 20.]),

                          # REAL---------------------------
                          # joint pid for landing contoller after td + wbc (optional)
                          'kp_wbc_real': np.array([10., 10., 10.]*4),
                          'kd_wbc_real': np.array([1., 1., 1.]*4),
                          'ki_wbc_real': np.array([0., 0., 0.]*4),

                        'kp_lin_real': np.array([1000., 1000., 1000.]),
                        'kd_lin_real': np.array([200., 150., 200.]),
                        'kp_ang_real': np.array([300., 300., 200.]),
                        'kd_ang_real': np.array([10., 20., 20.]),

                          #joint configuration
                          #default
                          #'q_0': np.array([0.2, 0.78, -1.7, 0.20, 0.78, -1.7, -0.20, 0.78, -1.7, -0.20, 0.78, -1.7]),  # this is to set the desired heigth for the startup phase
                          #orbit
                          'q_0': np.array([0.0951, 0.8303,-1.5419,
                                           0.0980, 0.9864, -1.4778,
                                           -0.0948, 0.8305,-1.5420,
                                           -0.0979,0.9864, -1.4779]),

                         'q_retraction': np.array([0.2867, 1.48, -2.6,
                                0.2867, 1.8, -2.48,
                                -0.2867, 1.48, -2.6,
                                -0.2867, 1.8, -2.48]),
                          # default
                          #'q_final': np.array([0.2, 1.1, -1.8, 0.2, 1.1, -1.8, -0.2, 1.1, -1.8, -0.2, 1.1, -1.8]),
                          # orbit
                          'q_final': np.array([0.1, 0.8, -1.6,  # lf
                                               0.1, 1.0, -1.6,  # lh
                                               -0.1, 0.8, -1.6,  # rf
                                               -0.1, 1.0, -1.6]),  # rh


                        #forward
                        'q_land_fwd':  np.array([0.1, 0.6, -1.8,  0.1, 0.6, -1.8, -0.1, 0.6, -1.8, -0.1, 0.6, -1.8]),
                        #backward
                        'q_land_bwd':  np.array([0.1, 1., -1.8,  0.1, 1., -1.8, -0.1, 1., -1.8, -0.1, 1., -1.8]),
                        'landing_duration': 1.4,
                        'com_z0_training' : 0.375,
                        'q_0_td': np.array([0.1789, 1.2234, -2.2329, 0.1867, 1.4733, -2.1055, -0.1784, 1.2230, -2.2327, -0.1861, 1.4733, -2.1053]),
                        'q_fold': np.array([0.2, 1.7, -2.7, 0.2,  1.7, -2.7, -0.2, 1.7,  -2.7, -0.2, 1.7, -2.7]),  #thjis is for the startup phase
                        'joint_names': ['lf_haa_joint', 'lf_hfe_joint', 'lf_kfe_joint',
                                       'lh_haa_joint', 'lh_hfe_joint', 'lh_kfe_joint',
                                       'rf_haa_joint', 'rf_hfe_joint', 'rf_kfe_joint',
                                       'rh_haa_joint', 'rh_hfe_joint', 'rh_kfe_joint'],
                        'ee_frames': ['lf_foot', 'lh_foot', 'rf_foot','rh_foot'],
                        'real_robot': False,
                        'force_th': 10.,
                        'spawn_x': 0.0,
                        'spawn_y': 0.0,
                        'spawn_z': 0.37,
                        'ip': "192.168.123.220",
                        'buffer_size': 50001} # note the frames are all aligned with base for joints = 0

robot_params['go2'] ={'dt': 0.002,
                      'buffer_size': 25001, # 120 seconds
                      # simulation gains

                      # default config
                      # 'kp': np.array([30., 30., 30.]*4),
                      # 'kd': np.array([3., 3., 3.]*4),
                      # 'ki': np.array([0., 0., 0.]*4),
                      #Orbit
                      'kp': np.array([60., 60., 60.] * 4),
                      'kd': np.array([0.8, 0.8, 0.8] * 4),
                      'ki': np.array([0., 0., 0.] * 4),

                      #default config
                      # 'kp_swing':  np.array([30., 30.,30]*4),
                      # 'kd_swing':  np.array([.2, .2, .24]*4),
                      # 'ki_swing':  np.array([2., 2., 2.]*4),
                      #orbit
                      'kp_swing': np.array([30., 30., 30.] * 4),
                      'kd_swing': np.array([0.4, 0.4, 0.4] * 4),
                      'ki_swing': np.array([0., 0., 0.] * 4),

                      'kp_land': np.array([30., 30., 30.] * 4),
                      'kd_land': np.array([0.8, 0.8, 0.8] * 4),
                      'ki_land': np.array([0., 0., 0.] * 4),

                      # joint pid + wbc (optional)
                      'kp_wbc': np.array([15., 15., 15.]*4),#np.array([10., 10., 10.]*4),
                      'kd_wbc': np.array([1., 1., 1.]*4),#np.array([1., 1., 1.]*4),
                      'ki_wbc': np.array([0., 0., 0.]*4),#np.array([0.3, 0.3, 0.3]*4),
                      # virtual impedance wrench control
                      'kp_lin': np.array([800, 500., 900.]),  # x y z
                      'kd_lin': np.array([100, 100., 100.]),
                      'kp_ang': np.array([40., 40., 40.]),  # R P Y
                      'kd_ang': np.array([1.51, 1.51, 1.51]),                      
                      # real robot gains
                      # stand alone joint pid
                      'kp_real': np.array([30., 30.,30.]*4),
                      'kd_real': np.array([1., 1., 1.]*4),
                      'ki_real': np.array([0., 0., 0.]*4),

                      'kp_real_swing':  np.array([30., 30, 30]*4),
                      'kd_real_swing':  np.array([1, 1, 1]*4),
                      'ki_real_swing':  np.array([0, 0, 0]*4),

                      'kp_real_land': np.array([20., 20.,20.]*4),
                      'kd_real_land': np.array([1, 1, 1]*4),
                      'ki_real_land': np.array([0, 0, 0]*4),
                       # joint pid + wbc (optional)
                      'kp_wbc_real': np.array([20., 30., 40.]*4),
                      'kd_wbc_real': np.array([.3, .3, .3]*4),
                      'ki_wbc_real': np.array([1.5, 1.5, 1.5]*4),
                      # virtual impedance wrench control
                      # 'kp_lin_real': np.array([300, 300., 300.]), # x y z
                      # 'kd_lin_real': np.array([30., 30., 30.]),
                      # 'kp_ang_real': np.array([50, 50., 50.]), # R P Y
                      # 'kd_ang_real': np.array([10., 10., 10.]),
                      'kp_lin_real': np.array([650., 300., 450.]), #np.array([300., 300., 400.]), # x y z
                      'kd_lin_real': np.array([40., 40., 40.]), #np.array([30., 20., 60.]),
                      'kp_ang_real': np.array([20., 35., 20.]), # #np.array([30., 50., 30.]), # R P Y
                      'kd_ang_real': np.array([1.5, 2.5, 1.5]), #np.array([2., 4., 2.]),
                      # joint configuration
                      #default configuration
                      #'q_0':  np.array([0.2, 0.78, -1.7,  0.2, 0.78, -1.7, -0.2, 0.78, -1.7, -0.2, 0.78, -1.7]),
                      # q0 orbit
                       'q_0':  np.array([0.1, 0.8, -1.5,#lf
                                         0.1, 1.0, -1.5,#lh
                                         -0.1, 0.8, -1.5,#rf
                                         -0.1, 1.0, -1.5]),#rh
                      'q_retraction': np.array([0.23, 1.38, -2.46, 0.23, 1.68, -2.31, -0.23, 1.38, -2.46, -0.23, 1.68, -2.31]),

                      #default configuration
                      #'q_final': np.array([0.1, 0.9, -1.8, 0.1, 0.9, -1.8, -0.1, 0.9, -1.8, -0.1, 0.9, -1.8]),
                      #q final orbit
                      'q_final': np.array([0.1, 0.8, -1.5,#lf
                                         0.1, 1.0, -1.5,#lh
                                         -0.1, 0.8, -1.5,#rf
                                         -0.1, 1.0, -1.5]),#rh
                      #Forward
                      'q_land_fwd':  np.array([0.1, 0.75, -1.8,  0.1, 0.75, -1.8, -0.1, 0.75, -1.8, -0.1, 0.75, -1.8]),
                      #backward
                      'q_land_bwd':  np.array([0.1, 1., -1.8,  0.1, 1., -1.8, -0.1, 1., -1.8, -0.1, 1., -1.8]),




                      'q_fold': np.array([0.2, 1.7, -2.7, 0.2,  1.7, -2.7, -0.2, 1.7,  -2.7, -0.2, 1.7, -2.7]),
                      'q_0_td': np.array([0.1789, 1.2234, -2.2329, 0.1867, 1.4733, -2.1055, -0.1784, 1.2230, -2.2327, -0.1861, 1.4733, -2.1053]),
                      'landing_duration': 1.4,
                      'com_z0_training': 0.32,
                        # 'q_0_lo': np.array([0.3430, 1.5495, -2.6620, 0.3433, 1.9171, -2.4902, -0.3425, 1.5490, -2.6620, -0.3424, 1.9171, -2.4901]),
                      'joint_names': ['lf_haa_joint',  'lf_hfe_joint', 'lf_kfe_joint',
                                      'lh_haa_joint',  'lh_hfe_joint', 'lh_kfe_joint',
                                      'rf_haa_joint',  'rf_hfe_joint', 'rf_kfe_joint',
                                      'rh_haa_joint',  'rh_hfe_joint', 'rh_kfe_joint'],
                      # ee params
                      'ee_frames': ['lf_foot', 'lh_foot', 'rf_foot','rh_foot'],
                     #  'force_th': 18.,
                      'force_th': 7.,
                      'contact_th': 0.01, # tolerance understand when /knee base is touching the ground
                      # simulation spawn [m] and [rad]
                      'spawn_x': 0.0,
                      'spawn_y': 0.0,
                      'spawn_z': .32,
                      'spawn_R': 0.0,
                      'spawn_P': 0.0,
                      'spawn_Y': 0.0,
                      'ip': "192.168.123.161",
                      # use real robot or simulation
                      'real_robot': False} # note the frames are all aligned with base for joints = 0
verbose = False
plotting = True

