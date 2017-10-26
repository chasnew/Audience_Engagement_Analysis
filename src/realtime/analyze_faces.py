import realtime.comman_utils as comman_utils
import os, time
import subprocess

#### CONSTANTS ##############
path_capture_dir = comman_utils.PATH_CAPTURE_DIR
path_output_dir = comman_utils.PATH_ANALYSIS_DIR
path_openface_featureextraction = os.path.join(comman_utils.PATH_OPENFACE_BIN, "FeatureExtraction")
DEBUG = comman_utils.DEBUG
FNULL = open(os.devnull, 'w')
#############################

def run_featureextraction(capture_dir_name):
    subprocess.call(
        [path_openface_featureextraction,
         '-au_static',
         '-fdir', os.path.join(path_capture_dir, capture_dir_name),
         '-of', os.path.join(path_output_dir, capture_dir_name + '.csv'),
         '-no2Dfp', '-no3Dfp', '-noMparams', '-noPose', '-q'],
        stdout=FNULL)


current_milli_time = lambda: int(round(time.time() * 1000))

# Cleanup output directory
comman_utils.clean_dir(path_output_dir)

if not os.path.exists(path_output_dir):
    os.makedirs(path_output_dir)

# wait till init directory is created by facial recognizer and tracker
while os.path.exists(os.path.join(path_capture_dir, comman_utils.INIT_DIR_NAME)) is False:
    time.sleep(1)

# process init directory
run_featureextraction(comman_utils.INIT_DIR_NAME)

while True:
    dir_list = sorted(os.listdir(path_capture_dir))
    for dir in dir_list:
        run_featureextraction(dir)

    # Hit 'q' on the keyboard to quit!
    if 0xFF == ord('q'):
        break

