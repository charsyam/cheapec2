import urllib2
import json
from dataprovider.dataprovider import EC2SpotInstancePriceProvider
import datetime

class ec2_region:
    pass

class ec2_instance_type:
    def __init__(self):
        self.size = ''
        self.category= ""
        self.prices = []

def remove_unnecessary_string_for_json(string):
    first = string[9:]
    return first[:-1]

def get_config(value):
    return value['config']

def get_regions_from_config(value):
    return value['regions']

def valid2regionname(region_name):
    return region_name.replace('-','_')

def valid2price(price):
    if( price == "N/A*" ):
        price = "-1"

    return price

class RIParser(object):
    def store_regionname(self, regions, provider):
        pass

    def convert2spotname(self, region_name):
        if( region_name == "ap-northeast-1" ):
            return "apac-tokyo"
        elif( region_name == "ap-southeast-1" ):
            return "apac-sin"
        elif( region_name == "eu-west-1" ):
            return "eu-ireland"
        elif( region_name == "us-west-1" ):
            return "us-west"
        
        return region_name
    
    def convert2categoryname(self, category_name):
        return category_name.replace("ResI","Spot")

    def store_price(self, region_name, region, current_date, provider):
        for instance in region.instances:
            for price in instance["prices"]:
                spot_name = self.convert2spotname(region_name)
                category_name = self.convert2categoryname( instance["category"] )
                provider.save_price_ri_info( current_date, spot_name,
                    category_name, instance['size'], 
                    float(price['price'])*1000, price['name'] )

    def parse_region(self, value, currencies):
        region = ec2_region()
        region.name = valid2regionname(value['region'])
        region.instances = []
        for instance in value['instanceTypes']:
            for size in instance['sizes']:
                c_inst = ec2_instance_type()
                c_inst.category = instance['type']

                if( "cluster" in c_inst.category ):
                    continue

                c_inst.size = size['size']
                for values in size['valueColumns']:
                    for currency in currencies:
                        price = valid2price(values['prices'][currency])

                        if( price == '-1' ):
                            continue

                        if( "hiIoResI" in c_inst.category ):
                            continue

                        if( 'Hourly' not in values['name'] ):
                            continue

                        c_inst.prices.append( { 'name': values['name'], 
                            'price': price, 'currency': currency } )

                region.instances.append( 
                    { 'category': c_inst.category, 
                        'size': c_inst.size,
                        'prices': c_inst.prices } );

        return region

class SpotParser(object):
    def store_regionname(self, regions, provider):
#        provider.delete_all_metadata()
        for region in regions:
            provider.add_region_info(region['region'])

    def store_price(self, region_name, region, current_date, provider):
        for instance in region.instances:
            for price in instance["prices"]:
                provider.save_category_info( instance["category"], instance['size'] )
                provider.save_price_info( current_date, region_name,
                    instance["category"], instance['size'], 
                    float(price['price'])*1000, price['name'] )

    def parse_region(self, value, currencies):
        region = ec2_region()
        region.name = valid2regionname(value['region'])
        region.instances = []
        for instance in value['instanceTypes']:
            for size in instance['sizes']:
                c_inst = ec2_instance_type()
                c_inst.category = instance['type']

                c_inst.size = size['size']
                for values in size['valueColumns']:
                    for currency in currencies:
                        if( "cluster" in c_inst.category ):
                            continue

                        if( values['name'] == 'mswin' ):
                            continue

                        price = valid2price(values['prices'][currency])
                        if( price == '-1' ):
                            continue

                        c_inst.prices.append( { 'name': values['name'], 
                            'price': price, 'currency': currency } )

                region.instances.append( 
                    { 'category': c_inst.category, 
                        'size': c_inst.size,
                        'prices': c_inst.prices } );

        return region

def get_value_columns_from_config(config):
    return config['valueColumns']

def get_value_currencies_from_config(config):
    return config['currencies']

def get_date_from_url(url, validjson):
    js_page = urllib2.urlopen(url)
    prices_str = js_page.read()

    if( validjson != True ):
        prices_js = remove_unnecessary_string_for_json(prices_str)
    else:
        prices_js = prices_str
    
    prices = json.loads(prices_js)
    return prices

def parse_main_data(data, provider, current_date, parser):
    config = get_config(data)
    valueColumns = get_value_columns_from_config(config)
    currencies = get_value_currencies_from_config(config)

    regions = get_regions_from_config(config)
    parser.store_regionname(regions, provider)

    for region in regions:
        c_region = parser.parse_region(region, currencies)
        parser.store_price( region['region'], c_region, current_date, provider )

if __name__=="__main__":
    SPOT_PRICES_JSON_PAGE="http://spot-price.s3.amazonaws.com/spot.js"
    HEAVY_PRICES_JSON_PAGE="http://aws.amazon.com/ec2/pricing/ri-heavy-linux.json"
    provider = EC2SpotInstancePriceProvider.get_provider()
    current_date = datetime.datetime.now().strftime('%Y%m%d%H')

    spot_parser = SpotParser()
    spot_price = get_date_from_url( SPOT_PRICES_JSON_PAGE, False )
    parse_main_data(spot_price, provider, current_date, spot_parser)
    provider.commit()

    ri_parser = RIParser()
    heavy_price = get_date_from_url( HEAVY_PRICES_JSON_PAGE, True )
    parse_main_data(heavy_price, provider, current_date, ri_parser)
    provider.commit()

