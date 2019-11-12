import wmi
c = wmi.WMI()

# c.classes - List of available attributes of c
# sth.properties - Dict of available properties of sth with None values


def get_property_dict_values(obj):
    """
    Returns dict with keys of obj.properties filled with coresponding values
    """

    result = {}
    for key in obj.properties.keys():
        value = getattr(obj, key)
        result[key] = value

    return result


def process_watcher_snippet():

    process_watcher = c.Win32_Process.watch_for("creation")
    while True:
        new_process = process_watcher()
        print(repr(new_process))


def create_and_terminate_process(cmd="mspaint"):

    process_id, success_code = c.Win32_Process.Create(cmd)
    print(f"process created with code {success_code}")

    import time
    for i in range(10):
        print(10 - i)
        time.sleep(1)

    # process pretends to be _wmi_object but print(process) reveals it's Win32_Process
    process = c.Win32_Process(ProcessID=process_id)[0]
    # process.methods reveals available methods
    process.Terminate()

    print("process killed")


if __name__ == "__main__":

    pass
