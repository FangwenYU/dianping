drop table dianping_pop_shop;

create table dianping_pop_shop
(
    city_id int,
    shop_type varchar(50),
    primary_tag varchar(50),
    shop_id int,
    shop_add_date varchar(50),
    shop_group_id int,
    name varchar(50),
    power varchar(50),
    shop_power varchar(50),
    shop_power_title varchar(50),
    address varchar(200),
    avg_price int,
    price_level varchar(50),
    price_info varchar(50),
    hits int,
    today_hits int,
    weekly_hits int,
    monthly_hits int,
    prev_weekly_hits int,
    vote_total int,
    main_category_id int,
    main_category_name varchar(50),
    region_id int,
    main_region_id int,
    main_region_name varchar(50),
    phone_no varchar(50),
    phone_no_2 varchar(50),
    popularity int,
    shop_taste_point float,
    shop_environment_point float,
    shop_service_point float,
    business_hour varchar(50),
    url varchar(100),
    category_id int,
    data_load_time timestamp default current_timestamp,
    primary key(shop_id)
);


--create table dianping_shop_id
--(
--    shop_id int,
--    city_id int,
--    category_id int,
--    shop_url varchar(200),
--    data_load_time timestamp default current_timestamp,
--    primary key(shop_id)
--)
--;



create table dianping_shop_id
(
    shop_id int,
    city_id int,
    category_id int,
    sub_category_id varchar(100),
    shop_url varchar(200),
    data_load_time timestamp default current_timestamp,
    primary key(shop_id)
)
;

drop table dianping_shop;
create table dianping_shop
(
    shop_id int,
    shop_url varchar(100),
    shop_navigation_path varchar(100),
    shop_name varchar(100),
    shop_rank varchar(50),
    shop_review varchar(50),
    shop_price varchar(50),
    shop_taste_score varchar(50),
    shop_env_score varchar(50),
    shop_service_score varchar(50),
    shop_district varchar(50),
    shop_address varchar(200),
    shop_phone_1 varchar(50),
    shop_phone_2 varchar(50),
    city_id int,
    category_id int,
    data_load_time timestamp default current_timestamp
)
;

drop table dianping_shop_review;
create table dianping_shop_review
(
    shop_id int,
    shop_url varchar(100),
    user_id varchar(100),
    user_url varchar(100),
    shop_score varchar(100),
    shop_review varchar(1000),
    data_load_time timestamp default current_timestamp
)
;


create table dianping_shop_city
(
    city_id int,
    city varchar(50)
);

insert into dianping_shop_city values
(344, '长沙'),
(7, '深圳')
;

create table dianping_shop_category
(
    category_id int,
    category varchar(50)
);

insert into dianping_shop_category values
(10, '美食'),
(20, '购物'),
(30, '休闲娱乐'),
(45, '运动健身')
;


create table dianping_shop_subcategory
(
    category_id int,
    sub_category_id varchar(20),
    sub_category varchar(50)
);

insert into dianping_shop_subcategory values
(10, 'g104', '湘菜'),
(10, 'g117', '面包甜点'),
(10, 'g112', '小吃快餐'),
(10, 'g111', '自助餐'),
(10, 'g132', '咖啡厅'),
(10, 'g110', '火锅'),
(10, 'g508', '烧烤'),
(10, 'g116', '西餐'),
(10, 'g224', '日本料理'),
(10, 'g114', '韩国料理'),
(10, 'g103', '粤菜'),
(10, 'g251', '海鲜'),
(10, 'g102', '川菜'),
(10, 'g118', '其他'),
(10, 'g113', '日本料理'),
(10, 'g115', '东南亚菜'),
(10, 'g207', '茶餐厅'),
(10, 'g101', '江浙菜'),
(10, 'g26481', '西北菜'),
(10, 'g106', '东北菜'),
(10, 'g109', '素材'),
(10, 'g3243', '新疆菜'),
(10, 'g250', '创意菜'),
(10, 'g108', '清真菜'),
(20, 'g120', '服饰鞋包'),
(20, 'g26085', '花店'),
(20, 'g187', '超市/便利店'),
(20, 'g128', '眼镜店'),
(20, 'g119', '综合商场'),
(20, 'g184', '食品茶酒'),
(20, 'g235', '药店'),
(20, 'g121', '运动户外'),
(20, 'g123', '化妆品'),
--(20, 'g125', '亲子购物'),
(20, 'g127', '书店'),
(20, 'g124', '数码产品'),
--(20, 'g122', '珠宝饰品'),
--(20, 'g126', '家居建材'),
(20, 'g26101', '办公文化用品'),
(20, 'g131', '其他购物场所'),
(20, 'g129', '特色集市'),
(20, 'g2714', '水果生鲜'),
(30, 'g135', 'KTV'),
--(30, 'g132', '咖啡厅'),
(30, 'g133', '酒吧'),
(30, 'g136', '电影院'),
(45, 'g147', '健身中心')
;


create table dianping_shop_id_cleaned
as
select a.shop_id,
		a.city_id,
		a.category_id,
		b.sub_category_id,
		a.shop_url
from
(
select shop_id, city_id, shop_url, min(category_id) as category_id
from dianping_shop_id
where city_id=7
group by shop_id, city_id, shop_url
) a
join
(
select shop_id, city_id, category_id, min(sub_category_id) as sub_category_id
from dianping_shop_id
where city_id=7
group by shop_id, city_id, category_id
) b
on a.shop_id = b.shop_id
and a.city_id = b.city_id
and a.category_id = b.category_id
;

delete from dianping_shop_id where city_id=7;
insert into dianping_shop_id(shop_id, city_id, category_id, sub_category_id, shop_url)
select * from dianping_shop_id_cleaned;

drop table dianping_shop_id_cleaned;



create table dianping_banned_url
(spider_name varchar(20),
url varchar(200),
city_id int,
category_id int,
data_load_time timestamp default current_timestamp
)
;


delete from dianping_banned_url where spider_name = 'shopid';
update dianping_banned_url set spider_name = 'shopid' where spider_name='banned_shopid';
