from BaseController import BaseController

class RegionListController(BaseController):

    def get(self):
        regions = {"regions": self.read_server_config() }
        self.write(regions)

    def read_server_config(self):
        """Returns a list of servers with the 'id' field added.
        """
        # TODO: Move this into the settings module so everything benefits.
        region_list = []
        regions = self.stats_provider.get_region_info()

        for region in regions:
            s = dict(id=region.name)
            region_list.append(s)

        return region_list

