import wmi
c = wmi.WMI()


class Node:

    def __init__(self, content, parent=None, str_func=None):

        self.content = content
        self._parent = None
        self.parent = parent

        self.children = []
        self.str_func = str_func

    @property
    def depth(self):

        result = 0
        active_node = self

        while active_node.parent:
            result += 1
            active_node = active_node.parent

        return result

    @property
    def parent(self):

        return self._parent

    @parent.setter
    def parent(self, value):

        self._parent = value

        if self._parent:
            self._parent.children.append(self)

    def draw(self):

        print(f"{4*self.depth*' '}{self}")

        for child in self.children:
            child.draw()

    def __str__(self):

        if self.str_func:
            return self.str_func(self.content)
        else:
            content = str(self.content).strip().replace("\n", " ")
            content = f"{content[:100]}..." if len(content) > 100 else content
            return f"Node(depth: {self.depth}, content: {content})"


def formater(thing):

    return f"{thing.Caption} ({thing.ProcessId})"


def main():

    processes = c.Win32_Process(
        "Caption CreationDate CommandLine ParentProcessId ProcessId".split()
    )
    process_nodes = [Node(p, str_func=formater) for p in processes]

    top_level_nodes = []

    for node in process_nodes:
        process = node.content

        if process.ProcessId == 0:
            top_level_nodes.append(node)
            continue

        parent_id = process.ParentProcessId

        parent_node = next((x for x in process_nodes if x.content.ProcessId == parent_id), None)

        if not parent_node:
            top_level_nodes.append(node)
            continue

        parent = parent_node.content

        if parent.CreationDate > process.CreationDate:
            top_level_nodes.append(node)
            continue

        node.parent = parent_node

    for node in top_level_nodes:
        node.draw()


if __name__ == '__main__':
    main()
