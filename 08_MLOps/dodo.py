""" DOIT Tasks """
from glob import glob, iglob
import tarfile
from doit.tools import Interactive
import tempfile
import os
from subprocess import run

def task_build():
    """ Zip files and start build """

    build_files = glob("*.py") + glob("app/*.py") \
                               + ["Dockerfile", "app/run.sh", "environment_ops.yml", "requirements.txt", ".dvc/config",
                               "models/model_v1.dvc"]
    def tar_build():
        with tarfile.open("build.tar.gz", "w:gz") as tar:
            for file in build_files:
                tar.add(file)
            # Wenn ds_toolset benötigt wird.
            #tar.add("../ds_toolset", arcname="deploy/ds_toolset")
            # tmpfile = tempfile.mktemp()
            # print(tmpfile)
            # with open(tmpfile, "w") as f:
            #     f.write("VERSION = \"" + version.get_version() + "\"")
            # tar.add(tmpfile, arcname="deploy_version.py")
            # os.remove(tmpfile)
    return {
        "actions": [
            tar_build
        ],
        'file_dep': build_files,
        'targets': ["build.tar.gz"],
    }

def task_start_build():
    """ Start build on oscp """
    return {
        "actions": [
            Interactive('oc start-build ha-mlops-modelapi-build -n daan-eval --from-archive build.tar.gz --follow')
        ],
        'file_dep': ["build.tar.gz"]
    }