from BaseController import BaseController

class CategoryListController(BaseController):

    def get(self):
        categories = {"categories": self.read_server_config() }
        self.write(categories)

    def read_server_config(self):
        """Returns a list of servers with the 'id' field added.
        """
        # TODO: Move this into the settings module so everything benefits.
        category_list = []
        categories = self.stats_provider.get_category_info()

        prev = ""
        for category in categories:
            if( prev == category.name ):
                continue

            s = dict(id=category.name)
            category_list.append(s)
            prev = category.name

        return category_list

