from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from scrapy.conf import settings

Base = declarative_base()


class DianpingPopShop(Base):

    __tablename__ = 'dianping_pop_shop'

    city_id = Column(Integer)
    shop_type = Column(String(50))
    primary_tag = Column(String(50))
    shop_id = Column(Integer, primary_key=True)
    shop_add_date = Column(String(50))
    shop_group_id = Column(Integer)
    name = Column(String(50))
    power = Column(String(50))
    shop_power = Column(String(50))
    shop_power_title = Column(String(50))
    address = Column(String(200))
    avg_price = Column(Integer)
    price_level = Column(String(50))
    price_info = Column(String(50))
    hits = Column(Integer)
    today_hits = Column(Integer)
    weekly_hits = Column(Integer)
    monthly_hits = Column(Integer)
    prev_weekly_hits = Column(Integer)
    vote_total = Column(Integer)
    main_category_id = Column(Integer)
    main_category_name = Column(String(50))
    region_id = Column(Integer)
    main_region_id = Column(Integer)
    main_region_name = Column(String(50))
    phone_no = Column(String(50))
    phone_no_2 = Column(String(50))
    popularity = Column(Integer)
    shop_taste_point = Column(Float)
    shop_environment_point = Column(Float)
    shop_service_point = Column(Float)
    business_hour = Column(String(100))
    url = Column(String(100))
    category_id = Column(Integer)


class DianpingShopId(Base):
    __tablename__ = 'dianping_shop_id'

    shop_id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    category_id = Column(Integer)
    sub_category_id = Column(String(100))
    shop_url = Column(String(200))


class DianpingShop(Base):
    __tablename__ = 'dianping_shop'

    shop_id = Column(Integer, primary_key=True)
    shop_url = Column(String(100))
    shop_navigation_path = Column(String(100))
    shop_name = Column(String(100))
    shop_rank = Column(String(50))
    shop_review = Column(String(50))
    shop_price = Column(String(50))
    shop_taste_score = Column(String(50))
    shop_env_score = Column(String(50))
    shop_service_score = Column(String(50))
    shop_district = Column(String(50))
    shop_address = Column(String(200))
    shop_phone_1 = Column(String(50))
    shop_phone_2 = Column(String(50))
    city_id = Column(Integer)
    category_id = Column(Integer)


class DianpingBannedUrl(Base):
    __tablename__ = 'dianping_banned_url'

    spider_name = Column(String(100))
    url = Column(String(200), primary_key=True)
    city_id = Column(Integer)
    category_id = Column(Integer)


class DianpingErrorUrl(Base):
    __tablename__ = 'dianping_error_url'

    spider_name = Column(String(100))
    url = Column(String(200), primary_key=True)
    city_id = Column(Integer)
    category_id = Column(Integer)

class DianpingShopReview(Base):
    __tablename__ = 'dianping_shop_review'

    shop_id = Column(Integer, primary_key=True)
    shop_url = Column(String(100))
    user_id = Column(String(100))
    user_url = Column(String(100))
    shop_score = Column(String(100))
    shop_review = Column(String(1000))


_mysql_config = {
            'user': settings['MYSQL_USER'],
            'password': settings['MYSQL_PASSWORD'],
            'host': settings['MYSQL_HOST'],
            'database': settings['MYSQL_DB'],
            'port': settings['MYSQL_PORT']
        }
_db_conn_str = 'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'.format(**_mysql_config)
engine = create_engine(_db_conn_str)

# engine = create_engine('mysql+mysqlconnector://ydata:ydata@127.0.0.1:3306/ydata')


DBSession = sessionmaker(bind=engine)
