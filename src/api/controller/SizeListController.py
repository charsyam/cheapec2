from BaseController import BaseController

class SizeListController(BaseController):

    def get(self):
        category = self.get_argument("category")
        sizes = {"sizes": self.read_server_config(category) }
        self.write(sizes)

    def read_server_config(self, category):
        """Returns a list of servers with the 'id' field added.
        """
        # TODO: Move this into the settings module so everything benefits.
        size_list = []
        sizes = self.stats_provider.get_size_info(category)

        for size in sizes:
            s = dict(id=size.size)
            size_list.append(s)

        return size_list

