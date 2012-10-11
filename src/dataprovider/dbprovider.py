import contextlib
import json

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.util import settings

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    name = Column(String(64), primary_key=True)
    size = Column(String(32), primary_key=True)

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return "<CategoryInfo(%s,%s)>"%(self.name,self.size)

class Region(Base):
    __tablename__ = 'regions'
    name = Column(String(32), primary_key=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<RegionInfo(%s)>"%(self.name) 

class Price(Base):
    __tablename__ = 'prices'
    id = Column(Integer, primary_key=True)
    date = Column(String(10))
    region = Column(String(32))
    category = Column(String(32))
    size = Column(String(32))
    price = Column(Integer)
    os = Column(String(32))

    def __init__(self, date, region, category, size, price, os):
        self.date = date
        self.region = region
        self.category = category
        self.size = size
        self.price = price
        self.os = os

    def __repr__(self):
        return "<Price('%s','%s','%s','%s','%s','%s')>"%(self.date, self.region, self.category, self.size, self.price, self.os)

class PriceRI1(Base):
    __tablename__ = 'prices_ri1'
    id = Column(Integer, primary_key=True)
    date = Column(String(10))
    region = Column(String(32))
    category = Column(String(32))
    size = Column(String(32))
    price = Column(Integer)
    os = Column(String(32))

    def __init__(self, date, region, category, size, price, os):
        self.date = date
        self.region = region
        self.category = category
        self.size = size
        self.price = price
        self.os = os

    def __repr__(self):
        return "<Price('%s','%s','%s','%s','%s','%s')>"%(self.date, self.region, self.category, self.size, self.price, self.os)

class PriceRI3(Base):
    __tablename__ = 'prices_ri3'
    id = Column(Integer, primary_key=True)
    date = Column(String(10))
    region = Column(String(32))
    category = Column(String(32))
    size = Column(String(32))
    price = Column(Integer)
    os = Column(String(32))

    def __init__(self, date, region, category, size, price, os):
        self.date = date
        self.region = region
        self.category = category
        self.size = size
        self.price = price
        self.os = os

    def __repr__(self):
        return "<Price('%s','%s','%s','%s','%s','%s')>"%(self.date, self.region, self.category, self.size, self.price, self.os)

class EC2SpotInstancePriceProvider(object):
    def make_driver_key(self):
        config = settings.get_dbdriver()
        driver = "%s://%s:%s@%s/%s"%(config['type'], config['user'],
                                    config['password'], config['server'],
                                    config['dbname'])
        return driver

    def __init__(self):
        self.engine = create_engine(self.make_driver_key())
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine, autoflush=True)
        self.session = self.Session()

    def commit(self):
        self.session.commit()

    def delete_all_metadata(self):
        self.delete_all_region_name()
        self.delete_all_category_name()
        
    def delete_all_region_name(self):
        sql = "delete from regions"
        self.engine.execute(sql)
        self.engine.execute('commit')

    def delete_all_category_name(self):
        sql = "delete from categories"
        self.engine.execute(sql)
        self.engine.execute('commit')

    def save_category_info(self, name, size):
        category = Category( name, size )
        output = self.session.query(Category).filter( "name=:name and size=:size" ).\
                params(name=name,size=size).first()
        if not output:
            self.session.add(category)

    def save_price_ri_info( self, date, region, category, size, price, term ):
        price_ri = None
        if( '1' in term ):
            price_ri = PriceRI1( date, region, category, size, price, "linux" )
        else:
            price_ri = PriceRI3( date, region, category, size, price, "linux" )

        self.session.add(price_ri)
        
    def save_price_info(self, date, region, category, size, price, os ):
        price = Price( date, region, category, size, price, os )
        self.session.add(price)

    def get_price_info(self, region, category, size, os, from_date, to_date):
        self.session.close()
        self.session = self.Session()
        price = self.session.query(Price).filter("region=:region and category=:category and size=:size and os=:os and date>=:fromdate and date<=:todate").\
                        params(region=region, category=category, size=size, os=os, fromdate=from_date, todate=to_date).all()
        price_ri1 = self.session.query(PriceRI1).filter("region=:region and category=:category and size=:size and os=:os and date>=:fromdate and date<=:todate").\
                        params(region=region, category=category, size=size, os=os, fromdate=from_date, todate=to_date).all()
        price_ri3 = self.session.query(PriceRI3).filter("region=:region and category=:category and size=:size and os=:os and date>=:fromdate and date<=:todate").\
                        params(region=region, category=category, size=size, os=os, fromdate=from_date, todate=to_date).all()
        return price, price_ri1, price_ri3

    def add_region_info(self, name):
        region = Region( name )
        output = self.session.query(Region).filter( "name=:name" ).\
                params(name=name).first()
        if not output:
            self.session.add(region)

    def get_region_info(self):
        query = self.session.query(Region);
        regions = query.all()
        return regions

    def get_category_info(self):
        query = self.session.query(Category);
        categories = query.all()
        return categories 

    def get_size_info(self, category):
        query = self.session.query(Category).filter("name=:category").\
            params(category=category)
        sizes = query.all()
        return sizes
