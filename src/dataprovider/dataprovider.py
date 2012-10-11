import dbprovider


# TODO: Confirm there's not some implementation detail I've missed, then
# ditch the classes here.
class EC2SpotInstancePriceProvider(object):

    @staticmethod
    def get_provider():
        """Returns a data provider based on the settings file.

        Valid providers are currently Redis and SQLite.
        """
        # FIXME: Should use a global variable for "redis" here.
        return dbprovider.EC2SpotInstancePriceProvider()
