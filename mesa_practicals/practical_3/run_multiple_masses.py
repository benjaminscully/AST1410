import os
import subprocess
import numpy as np
import shutil

path = "./mesa_codes"
results = "LOGS/history.data"
inlist_project = os.path.join(path, "inlist_project")
inlist_load = os.path.join(path, "inlist_load")
inlist = os.path.join(path, "inlist")

masses1 = np.linspace(0.1, 0.9, num=10)
masses2 = np.linspace(1, 10, num=10)
# masses = np.linspace(8, 10, num=3)
masses3 = np.linspace(11, 20, num=10)
masses = np.concatenate((masses1, masses2, masses3))

with open(inlist_project, "r") as f:
    project_read_lines = f.readlines()
with open(inlist_load, "r") as f:
    load_read_lines = f.readlines()
with open(inlist, "r") as f:
    inlist_read_lines = f.readlines()

project_write_lines = [line.strip() for line in project_read_lines]
load_write_lines = [line.strip() for line in load_read_lines]
inlist_write_lines = [line.strip() for line in inlist_read_lines]

for mass in masses:
    project_write_lines[0] = "! inlist to evolve a {:.2f} solar mass star".format(mass)
    project_write_lines[15] = "save_model_filename = '{:.2f}M_at_TAMS.mod'".format(mass)
    project_write_lines[45] = "initial_mass = {:.2f} ! in Msun units".format(mass)
    load_write_lines[5] = "load_model_filename = '{:.2f}M_at_TAMS.mod'".format(mass)

    if mass >= 8:
        load_read_lines[36] = "cool_wind_RGB_scheme = 'Dutch'"
        load_read_lines[37] = "cool_wind_AGB_scheme = 'Dutch'"
        load_read_lines[38] = "RGB_to_AGB_wind_switch = 1d-4"
        load_read_lines[39] = "Dutch_scaling_factor = 0.8"
    else:
        load_read_lines[36] = "! cool_wind_RGB_scheme = 'Dutch'"
        load_read_lines[37] = "! cool_wind_AGB_scheme = 'Dutch'"
        load_read_lines[38] = "! RGB_to_AGB_wind_switch = 1d-4"
        load_read_lines[39] = "! Dutch_scaling_factor = 0.8"

    with open(os.path.join(path, "inlist_load"), "w") as f:
        for line in load_write_lines:
            f.write(line + "\n")
    with open(os.path.join(path, "inlist_project"), "w") as f:
        for line in project_write_lines:
            f.write(line + "\n")

    inlist_write_lines[9] = "extra_star_job_inlist_name(1) = 'inlist_project'"
    inlist_write_lines[17] = "extra_eos_inlist_name(1) = 'inlist_project'"
    inlist_write_lines[25] = "extra_kap_inlist_name(1) = 'inlist_project'"
    inlist_write_lines[33] = "extra_controls_inlist_name(1) = 'inlist_project'"
    with open(os.path.join(path, "inlist"), "w") as f:
        for line in inlist_write_lines:
            f.write(line + "\n")

    subprocess.run(['./mk'], cwd='./mesa_codes')
    subprocess.run(['./rn'], cwd='./mesa_codes')

    shutil.copy(os.path.join(path, results), "./saved_files/MS_{:.2f}_Msun.data".format(mass))

    inlist_write_lines[9] = "extra_star_job_inlist_name(1) = 'inlist_load'"
    inlist_write_lines[17] = "extra_eos_inlist_name(1) = 'inlist_load'"
    inlist_write_lines[25] = "extra_kap_inlist_name(1) = 'inlist_load'"
    inlist_write_lines[33] = "extra_controls_inlist_name(1) = 'inlist_load'"
    with open(os.path.join(path, "inlist"), "w") as f:
        for line in inlist_write_lines:
            f.write(line + "\n")

    subprocess.run(['./mk'], cwd='./mesa_codes')
    subprocess.run(['./rn'], cwd='./mesa_codes')

    shutil.copy(os.path.join(path, results), "./saved_files/PMS_{:.2f}_Msun.data".format(mass))
