from scrapy import Spider, Request
from yahoofinance.items import YahoofinanceItem
import re



class YahooFinanceSpider(Spider):

    f = open('nyse_cleaned.csv', 'r')
    tickers = f.read().split(',')
    f.close()

# suggestion from Alex: to get the ticker iteration, import pandas to use read_csv and iterate over the series instead of a list

    name = 'yahoofinance_spider'
    allowed_urls = ['https://finance.yahoo.com/']
    #start_urls = ['https://finance.yahoo.com/quote/GOOGL/key-statistics?p=GOOGL']
    start_urls = [f'https://finance.yahoo.com/quote/{i}/key-statistics?p={i}' for i in tickers]#.values()]

    def parse(self,response):
        
        yield Request(url=response.url,callback=self.parse_stats_page)



    def parse_stats_page(self, response):

        company_name = ' '.join(response.xpath('//div[@class="D(ib) "]/h1/text()').extract_first().split()[:-1])
        ticker_name = response.xpath('//div[@class="D(ib) "]/h1/text()').extract_first().split()[-1].replace('(','').replace(')','')
        
        try:
            market_cap = response.xpath('//tr[@class="Bxz(bb) H(36px) BdY Bdc($seperatorColor) fi-row Bgc($hoverBgColor):h"]/td/text()').extract()[1]
        except:
            market_cap = None

        #top table on key_statistics page:
        valuation_measures = response.xpath('//tr[@class="Bxz(bb) H(36px) BdB Bdbc($seperatorColor) fi-row Bgc($hoverBgColor):h"]/td/text()').extract()
        #list comprehension to organize the table into item values
        stats_a = []
        [stats_a.append(valuation_measures[n+1:n+6]) for n, el in list(enumerate(valuation_measures)) if el == ' ']

        enterprise_value = stats_a[0][0]
        trailing_pe = stats_a[1][0]
        forward_pe = stats_a[2][0]
        peg_ratio = stats_a[3][0]

        #for the two tables below, place each value in a dictionary and store items by referencing that dictionary
        financial_highlights_dict ={}
        financial_highlights = response.xpath('//div[@class="Fl(start) W(50%) smartphone_W(100%)"]/div/div//table//tr')

        for row in financial_highlights:
            key = row.xpath('./td[1]//text()').extract_first()
            value = row.xpath('./td[2]//text()').extract_first()
            financial_highlights_dict[key] = value

        profit_margin = financial_highlights_dict.get('Profit Margin')
        return_on_assets = financial_highlights_dict.get('Return on Assets')
        return_on_equity = financial_highlights_dict.get('Return on Equity')
        revenue = financial_highlights_dict.get('Revenue')
        ebitda = financial_highlights_dict.get('EBITDA')
        tot_cash = financial_highlights_dict.get('Total Cash')
        tot_debt = financial_highlights_dict.get('Total Debt')


        trading_info_dict = {}
        trading_info = response.xpath('//div[@class="Fl(end) W(50%) smartphone_W(100%)"]/div/div//table//tr')

        for row in trading_info:
            key = row.xpath('./td[1]//text()').extract_first()
            value = row.xpath('./td[2]//text()').extract_first()
            trading_info_dict[key] = value

        fifty_day_moving_avg = trading_info_dict.get('50-Day Moving Average')
        twohundred_day_moving_avg = trading_info_dict.get('200-Day Moving Average')
        avg_vol_3month = trading_info_dict.get('Avg Vol (3 month)')
        held_by_insiders = trading_info_dict.get('% Held by Insiders')
        held_by_institutions = trading_info_dict.get('% Held by Institutions')


        #DNU -- data-reactid is dynamic
        # profit_margin = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="480"]/text()').extract() ##       
        # return_on_assets = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="501"]/text()').extract() ##
        # return_on_equity = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="508"]/text()').extract() ##
        # revenue = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="501"]/text()').extract()
        # ebitda = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="529"]/text()').extract()
        # tot_cash = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="564"]/text()').extract()
        # tot_debt = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="578"]/text()').extract()
        # fifty_day_moving_avg = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="245"]/text()').extract()
        # twohundred_day_moving_avg = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="252"]/text()').extract()
        # avg_vol_3month = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="266"]/text()').extract()
        # held_by_insiders = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="294"]/text()').extract()
        # held_by_institutions = response.xpath('//td[@class="Fw(500) Ta(end) Pstart(10px) Miw(60px)" and @data-reactid="301"]/text()').extract()


    

        meta = {'company_name': company_name, 'ticker_name': ticker_name, 'market_cap': market_cap, 'enterprise_value': enterprise_value,
        'trailing_pe': trailing_pe, 'forward_pe': forward_pe, 'peg_ratio': peg_ratio, 'profit_margin': profit_margin, 'return_on_assets':return_on_assets,
        'return_on_equity':return_on_equity, 'revenue':revenue, 'ebitda':ebitda, 'tot_cash':tot_cash, 'tot_debt':tot_debt, 'fifty_day_moving_avg': fifty_day_moving_avg,
        'twohundred_day_moving_avg':twohundred_day_moving_avg, 'avg_vol_3month':avg_vol_3month, 'held_by_institutions': held_by_institutions, 
        'held_by_insiders':held_by_insiders}

        yield Request(url=response.url.replace('key-statistics', 'sustainability'), callback=self.parse_sustainability_page, meta=meta)

 
    def parse_sustainability_page(self, response):


        try:
            e_score = response.xpath('//div[@class="D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)"]/text()').extract()[0]
        except:
            e_score = None

        try:
            s_score = response.xpath('//div[@class="D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)"]/text()').extract()[1] 
        except:
            s_score = None

        try:
            g_score = response.xpath('//div[@class="D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)"]/text()').extract()[2]
        except:
            g_score = None

        try:
            c_level = response.xpath('//div[@class="D(ib) Fz(36px) Fw(500)"]/text()').extract_first()   
        except:
            c_level = None

        try:
            tot_esg_score = response.xpath('//div[@class="Fz(36px) Fw(600) D(ib) Mend(5px)"]/text()').extract_first()
        except:
            tot_esg_score = None
        
        response.meta['e_score'] = e_score
        response.meta['s_score'] = s_score
        response.meta['g_score'] = g_score
        response.meta['c_level'] = c_level
        response.meta['tot_esg_score'] = tot_esg_score

        #check:
        # print('-'*50)
        # print('SUSTAINABILITY PAGE DATA')
        # print('-'*50)
        # print('e =', e_score)
        # print('s =', s_score)
        # print('g =', g_score)
        # print('c =', c_level)
        # print('total esg score =', tot_esg_score)
        # print('-'*50)
        # print('-'*50)
        # print('-'*50)
        

        yield Request(url=response.url.replace('sustainability','profile'), callback=self.parse_profile_page, meta=response.meta)

    def parse_profile_page(self,response):

        industry = response.xpath('//div[@class="asset-profile-container"]//p/span/text()').extract()[3]
        sector = response.xpath('//div[@class="asset-profile-container"]//p/span/text()').extract()[1]
        employees = response.xpath('//div[@class="asset-profile-container"]//p/span/span/text()').extract_first()
        hq = ' '.join(response.xpath('//div[@class="asset-profile-container"]/div/div/p/text()').extract()[0:2])

        response.meta['industry']=industry
        response.meta['sector']=sector
        response.meta['employees']=employees
        response.meta['hq']=hq

        # print('-'*50)
        # print('PROFILE PAGE DATA')
        # print('-'*50)
        # print('industry =', industry)
        # print('sector =', sector)
        # print('employees =', employees)
        # print('hq =', hq)

        item = YahoofinanceItem()
        item['company_name'] = response.meta['company_name']
        item['ticker_name'] = response.meta['ticker_name']
        item['e_score'] = response.meta['e_score']
        item['s_score'] = response.meta['s_score']
        item['g_score'] = response.meta['g_score']
        item['c_level'] = response.meta['c_level']
        item['tot_esg_score'] = response.meta['tot_esg_score']
        item['industry'] = response.meta['industry']
        item['sector'] = response.meta['sector']
        item['employees'] = response.meta['employees']
        item['hq'] = response.meta['hq']
        item['market_cap'] = response.meta['market_cap']
        item['enterprise_value'] = response.meta['enterprise_value']
        item['trailing_pe'] = response.meta['trailing_pe']
        item['forward_pe'] = response.meta['forward_pe']
        item['peg_ratio'] = response.meta['peg_ratio']
        item['profit_margin'] = response.meta['profit_margin']
        item['return_on_assets'] = response.meta['return_on_assets']
        item['return_on_equity'] = response.meta['return_on_equity']
        item['revenue'] = response.meta['revenue']
        item['ebitda'] = response.meta['ebitda']
        item['tot_cash'] = response.meta['tot_cash']
        item['tot_debt'] = response.meta['tot_debt']
        item['fifty_day_moving_avg'] = response.meta['fifty_day_moving_avg']
        item['twohundred_day_moving_avg'] = response.meta['twohundred_day_moving_avg']
        item['avg_vol_3month'] = response.meta['avg_vol_3month']
        item['held_by_insiders'] = response.meta['held_by_insiders']
        item['held_by_institutions'] = response.meta['held_by_institutions']
        item['e_score'] = response.meta['e_score']

        yield item