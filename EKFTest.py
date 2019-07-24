import numpy as np
from StateEstimator import EKFVelocityStateEstimator
from WooferConfig import WOOFER_CONFIG
import pdb
import quaternion

L = 5

x0 = np.zeros(L)

ekf_state_est = EKFVelocityStateEstimator(x0, 0.001)

data = np.load('woofer_numpy_log.npz')

n = np.shape(data['state_history'])[1]

n = 4500

state_est = np.zeros((L+12, n))

state_est[:L,0] = x0

for i in range(1, n):
	accel_meas = data['accelerometer_history'][:, i]
	gyro_meas = data['gyro_history'][:, i]

	joint_pos_meas = data['joint_pos_sensor_hist'][:, i]
	joint_vel_meas = data['joint_vel_sensor_hist'][:, i]

	z_meas = np.concatenate([accel_meas, gyro_meas, joint_pos_meas, joint_vel_meas])

	contacts = data['contacts_history'][:,i]

	(state_i, kinematic_vel) = ekf_state_est.update(z_meas, contacts)

	state_est[:L, i] = state_i
	state_est[L:, i] = kinematic_vel

np.savez('woofer_ekf_state_est_log', state_est)