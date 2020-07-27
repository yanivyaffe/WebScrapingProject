# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YahoofinanceItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    ticker_name = scrapy.Field()
    
    e_score = scrapy.Field()
    g_score = scrapy.Field()
    s_score = scrapy.Field()
    c_level = scrapy.Field()
    tot_esg_score = scrapy.Field()

    industry = scrapy.Field()
    sector = scrapy.Field()
    employees = scrapy.Field()
    hq = scrapy.Field()
    
    market_cap = scrapy.Field()
    enterprise_value = scrapy.Field()
    trailing_pe = scrapy.Field()
    forward_pe = scrapy.Field()
    peg_ratio = scrapy.Field()

    profit_margin = scrapy.Field()
    return_on_assets = scrapy.Field()
    return_on_equity = scrapy.Field()
    revenue = scrapy.Field()
    ebitda = scrapy.Field()
    tot_cash = scrapy.Field()
    tot_debt = scrapy.Field()
    fifty_day_moving_avg = scrapy.Field()
    twohundred_day_moving_avg = scrapy.Field()
    avg_vol_3month = scrapy.Field()
    held_by_insiders = scrapy.Field()
    held_by_institutions = scrapy.Field()
