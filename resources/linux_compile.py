addon_id = "auto_reload"
dirs_exclude = [
    ".git",
    ".github",
    "__pycache__",
    "releases",
    "resources",
]
file_pattern_exclude = [
    ".gitignore",
    ".ffs_db",
    ".build",
    "addon_version.json",
]
deploy_path = "/home/tonton/.config/blender/4.2/extensions/user_default/"

import os, zipfile, shutil, sys

### CHECK BEHAVIOR (deploy/release)

# Missing argument
if len(sys.argv) == 1 :
    print("Missing argument")
    exit()

# Behavior selection
behavior = ""
if sys.argv[1].lower() in ["-rd", "-dr"]:
    behavior = "rd"
elif sys.argv[1].lower() == "-d":
    behavior = "d"
elif sys.argv[1].lower() == "-r":
    behavior = "r"

# Invalid argument
else:
    print("Invalid argument")
    exit()

# Dry run
dry = False
if len(sys.argv) > 2 :
    if sys.argv[2].lower() == "-dry":
        dry = True
        print("Dry run : described operations will not happen")
    else:
        print("Invalid argument")
        exit()

### GET ADDON ROOTPATH
rootpath = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
print(f"Rootpath : {rootpath}")

### GET VERSION
if "r" in behavior:
    manifest_file = os.path.join(rootpath, "blender_manifest.toml")
    with open(manifest_file) as file:
        for line in file:
            if line.startswith("version = "):
                version = line.split('"')[1]
                version = version.replace(".", "_")
    print(f"Version : {version}")

### CREATE RELEASE/DEPLOY

if "r" in behavior:
    release_path = os.path.join(os.path.join(rootpath, "releases"), f"{addon_id}_{version}.zip")

    # Remove file if existing
    if os.path.isfile(release_path):
        if not dry: 
            os.remove(release_path)
        print(f"Removed file : {release_path}")

# Get file list
file_list = []
for dirname, subdirs, files in os.walk(rootpath):
    for filename in files:

        # Exclude subdirs
        dir_components = dirname.split(os.sep)
        if len([x for x in dirs_exclude if x in dir_components])!=0:
            continue

        # Exclude files
        if len([x for x in file_pattern_exclude if x in filename])!=0:
            continue

        file_list.append(os.path.join(dirname, filename))

print("Files to treat :")
print(file_list)

# Create archive and deploy
if "r" in behavior and not dry:
    zipf = zipfile.ZipFile(release_path, "w")

for filepath in file_list:

    # Write to zip
    if "r" in behavior and not dry:
        zipf.write(
            filepath,
            os.path.basename(filepath), # Remove dir structure in zip
            )

    # Deploy
    if "d" in behavior and not dry:
        addon_deploy_path = os.path.join(deploy_path, addon_id)
        if not os.path.isdir(addon_deploy_path):
            os.makedirs(addon_deploy_path, exist_ok=True)
            print(f"Folder created : {addon_deploy_path}")
        shutil.copy(
            filepath,
            addon_deploy_path,
        )

# Recap
print()
if "r" in behavior:
    if not dry:
        zipf.close()
    print(f"Release created : {release_path}")

if "d" in behavior:
    print(f"Deploy done in : {deploy_path}")

