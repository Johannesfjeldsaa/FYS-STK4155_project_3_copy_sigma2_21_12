# Import packages
from src.preproces import Preprocess_Climate_Data, Handle_Files

# Define folder path
data_dir = '/nird/projects/NS9188K/bjornhs/ACCESS-ESM1-5/'
work_dir = '/nird/home/johannef/FYS-STK4155_Project_3'
# Create file handler object and get all filenames in the folder path
file_handler = Handle_Files(work_dir)
file_names = file_handler.get_all_filenames_in_dir(data_dir)

# Get all files with the ACCESS_ESM1_5 model name in the filename
ACCESS_ESM1_5_files = [name for name in file_names if 'ACCESS-ESM1-5' in name]

# Sort the files by variable (tas or pr) and 
ACCESS_ESM1_5_tas_files = []
ACCESS_ESM1_5_pr_files = []

for file in ACCESS_ESM1_5_files:
    variable = file.split('_')[0]
    if variable == 'tas':
        ACCESS_ESM1_5_tas_files.append(file)
    elif variable == 'pr':
        ACCESS_ESM1_5_pr_files.append(file)

sorted_files = {'tas': {}, 'pr': {}}

for var, file_list in zip(['tas', 'pr'], 
                         [ACCESS_ESM1_5_tas_files, ACCESS_ESM1_5_pr_files]):
    for file in file_list:
        scenario = file.split('_')[3]
        if scenario not in sorted_files[var]:
            sorted_files[var][scenario] = []
        sorted_files[var][scenario].append(file)

# Create preprocesser object
preprocesser = Preprocess_Climate_Data(work_dir)

for var in sorted_files.keys():
    for scenario in sorted_files[var].keys():

        file_names = sorted_files[var][scenario]
        save_path = work_dir + ' DataFiles/' + var + '/' + scenario + '/'

        for file_name in file_names:
            dataset = file_handler.read_netcdf_to_xr(directory=data_dir, file_name=file_name)

            preprocesser.create_spatial_temporal_climatology(dataset=dataset,
                                                             var_name=var,
                                                             spatial_climatology_type="global",
                                                             temporal_climatology_type="yearly",
                                                             save_to_dataset=True,
                                                             file_name=file_name,
                                                             directory=save_path, 
                                                             is_original_name=True,
                                                             re_open=False)