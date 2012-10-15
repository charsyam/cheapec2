from BaseController import BaseController
import tornado.ioloop
import tornado.web
import datetime

class PriceController(BaseController):
    def change2datetime(self,str_date):
        return datetime.datetime.strptime(str_date,'%Y%m%d%H')
        

    def get(self):
        region = self.get_argument("region")
        category = self.get_argument("category")
        size = self.get_argument("size")
        os = self.get_argument("os")
        from_date = self.get_argument("from", None)
        to_date = self.get_argument("to", None)

        return_data = dict(data=[],
                           timestamp=datetime.datetime.now().isoformat())

        if from_date==None or to_date==None:
            delta = datetime.timedelta(days=1)
            tmp_end = datetime.datetime.now() + delta
            tmp_start = datetime.datetime.now() - delta
            end = tmp_end.strftime("%Y%m%d%H")
            start = tmp_start.strftime("%Y%m%d%H")
        else:
            start = dateutil.parser.parse(from_date)
            end   = dateutil.parser.parse(to_date)

        combined_data = []
        # TODO: These variables aren't currently used; should they be removed?
        prev_max=0
        prev_current=0
        counter=0

        prices = self.stats_provider.get_price_info(region, category,
                            size, os, start, end)
        item_size = len(prices[0])

        for i in xrange(item_size):
            value = self.change2datetime(prices[0][i].date)
            str_date = value.strftime("%Y-%m-%d %H:%M:%S")
            return_data['data'].append([str_date,
                float(prices[0][i].price)/1000,
                float(prices[1][i].price)/1000,
                float(prices[2][i].price)/1000] )

        self.write(return_data)

