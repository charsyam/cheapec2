from decimal import Decimal
from BaseController import BaseController
import tornado.ioloop
import tornado.web
import re
import datetime


class InfoController(BaseController):
    def change2datetime(self,str_date):
        return datetime.datetime.strptime(str_date,'%Y%m%d%H')


    def get(self):
        region = self.get_argument("region")
        category = self.get_argument("category")
        size = self.get_argument("size")
        os = self.get_argument("os")
        from_date = self.get_argument("from", None)
        to_date = self.get_argument("to", None)

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
        return_data = dict(data=[],
                           timestamp=datetime.datetime.now().isoformat())
        price_info = {}

        tmp_spot = tmp_y1 = tmp_y3 = 0

        if( item_size > 0):
            tmp_spot = float(prices[0][item_size-1].price)/1000 * 24 * 30
            tmp_y1 = float(prices[1][item_size-1].price)/1000 * 24 * 30
            tmp_y3 = float(prices[2][item_size-1].price)/1000 * 24 * 30

        price_info['spot'] = "{0:.2f}".format(tmp_spot)
        price_info['y1'] = "{0:.2f}".format(tmp_y1)
        price_info['y3'] = "{0:.2f}".format(tmp_y3)

        return_data['data'].append(price_info)
        self.write(return_data)

    def rounded_number(self, number, denominator):
        """Rounds a number.

        Args:
            number (int|float): The number to round.
            denominator (int): The denominator.
        """
        rounded = str(round(Decimal(number)/Decimal(denominator), 1))
        replace_trailing_zero = re.compile('0$')
        no_trailing_zeros = replace_trailing_zero.sub('', rounded)
        replace_trailing_period = re.compile('\.$')
        final_number = replace_trailing_period.sub('', no_trailing_zeros)
        return final_number

