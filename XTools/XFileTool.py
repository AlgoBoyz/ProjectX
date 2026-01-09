import json
import os
import enum
import time


def is_subset(subset, parent):
    return all(key in parent and parent[key] == value for key, value in subset.items())


def get_path_parent(path):
    if not isinstance(path, str):
        raise KeyError(f"Not a path{path}")
    if not os.path.exists(path):
        raise KeyError(f"Not a valid path:{path}")
    return os.path.dirname(path)


class PathType(enum.Enum):
    Directory = enum.auto()
    File = enum.auto()


class FileIO(object):

    def __init__(self, work_dir):
        self.work_dir = work_dir

        self._validate_work_dir()

    def _validate_work_dir(self):
        if not os.path.exists(self.work_dir):
            raise RuntimeError("Work directory: {} do not exist".format(self.work_dir))

    def save_in_json(self, data, file_name, force=True):
        file_path = os.path.join(self.work_dir, file_name + ".json")
        if not force:
            if os.path.exists(file_path):
                print("File: {} already exists,enable -force to overwrite".format(file_path))
                return False
        with open(file_path, "w") as f:
            data = json.dumps(data, indent=4)
            f.write(data)
            return True

    def update_json_dict(self, new_item, file_name):
        file_path = os.path.join(self.work_dir, file_name + ".json")
        old_items: dict = self.load_from_json(file_name)
        old_items.update(new_item)
        with open(file_path, "w") as f:
            json.dump(old_items, f, indent=4, ensure_ascii=False)

    def load_from_json(self, file_name):
        file_path = os.path.join(self.work_dir, file_name + ".json")
        if not os.path.exists(file_path):
            raise RuntimeError("File: {} do not exist!".format(file_name + ".json"))
        with open(file_path, "r") as f:
            data = json.loads(f.read())
        return data

    def load_from_py(self, file_name):
        file_path = os.path.join(self.work_dir, file_name + ".py")
        if not os.path.exists(file_path):
            raise RuntimeError("File: {} do not exist!".format(file_name + ".json"))
        with open(file_path, "r") as f:
            data = f.read()
        return data

    @classmethod
    def get_path_instance(cls, file_path):
        path_type = Directory if os.path.isdir(file_path) else File
        instance = path_type(file_path)
        instance.check_exist()
        return instance


class Node(object):

    def __init__(self, node_path):
        self.path = os.path.abspath(node_path)

    def __repr__(self):
        file_type = "Directory" if self.is_directory else "File"
        description = f"{file_type}: {self.abs_path}"
        return description

    @property
    def abs_path(self):
        self.check_exist()
        return os.path.abspath(self.path)

    @property
    def exist(self):
        return os.path.exists(self.path)

    @property
    def parent(self):
        self.check_exist()
        return Directory(os.path.dirname(self.path))

    @property
    def name(self):
        self.check_exist()
        return os.path.basename(self.path)

    @property
    def is_directory(self):
        self.check_exist()
        return True if os.path.isdir(self.path) else False

    @property
    def is_file(self):
        self.check_exist()
        return True if os.path.isfile(self.path) else False

    @property
    def type(self):
        if self.is_directory:
            return PathType.Directory
        elif self.is_file:
            return PathType.File
        else:
            raise KeyError(f"Wrong path:{self.path}")

    def check_exist(self):
        if not self.exist:
            raise RuntimeError(f"Path do not exist:{self.path}")
        return True


class Directory(Node):

    def __init__(self, dir_path):
        super().__init__(dir_path)

    @property
    def children(self):
        self.check_exist()
        children_names = os.listdir(self.path)
        children = []
        if not children_names:
            return None
        for child_name in children_names:
            child_path = os.path.join(self.path, child_name)
            instance = FileIO.get_path_instance(child_path)
            children.append(instance)
        return children


class File(Node):

    def __init__(self, file_path):
        super().__init__(file_path)

    @property
    def ext(self):
        ext = self.path.split('.')[-1]
        return ext

    @classmethod
    def create(cls, file_path, override=False):
        if os.path.exists(file_path):
            if override:
                return cls(file_path)
            else:
                raise FileExistsError(f"File{file_path} already exist!Use -override=True to override")
        with open(file_path, 'w', encoding='utf-8') as f:
            pass
        return cls(file_path)


class JsonFile(File):

    def __init__(self, file_path):
        super().__init__(file_path)
        self.data = {}

    def load(self):
        self.check_exist()
        with open(self.path, 'r', encoding='utf-8') as f:
            file_str = f.read()
            data = json.loads(file_str)
        self.data = data
        return self.data

    def dump(self, data):
        self.check_exist()
        with open(self.path, 'w', encoding='utf-8') as f:
            json_data = json.dumps(data, indent=4)
            f.write(json_data)





if __name__ == "__main__":
    path = r'D:\Work\Code\Python\OneShotRig\oneshotrig\Data\body.json'
    path2 = r"E:\Software\ShareFolderForVMWare\Ubantu\system_fs_config"
    with open(path2, encoding='utf-8') as f:
        for line in f:
            print(line)
