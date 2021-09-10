import pandas as pd, numpy as np, matplotlib.pyplot as plt

from getInput import getTasksFromJson

filename = "src\input\scheduledAppointments.json"
tasks = getTasksFromJson(filename)
standard = []
emergency = []

for task in tasks:
    if task["workType"] == "Standard":
        standard.append(task)
    elif task["workType"] == "Emergency":
        emergency.append(task)
    else:
        raise("Error")

df_std = pd.DataFrame.from_dict(standard)
X = np.array(df_std[['lng', 'lat']])

df_emg = pd.DataFrame.from_dict(emergency)
Y = np.array(df_emg[['lng', 'lat']])


plt.figure()
xs, ys = X.T
xe, ye = Y.T
plt.scatter(xs, ys, c='b')
plt.scatter(xe, ye, c='r')
plt.show()