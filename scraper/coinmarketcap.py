# scraper/coinmarketcap.py

import requests
from bs4 import BeautifulSoup

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def fetch_coin_data(self, coin):
        url = f"{self.BASE_URL}{coin}/"
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data for {coin}, status code: {response.status_code}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data = {
            "price": self.get_price(soup),
            "price_change": self.get_price_change(soup),
            "market_cap": self.get_market_cap(soup),
            "market_cap_rank": self.get_market_cap_rank(soup),
            "volume": self.get_volume(soup),
            "volume_rank": self.get_volume_rank(soup),
            "volume_change": self.get_volume_change(soup),
            "circulating_supply": self.get_circulating_supply(soup),
            "total_supply": self.get_total_supply(soup),
            "max_supply": self.get_max_supply(soup),
            "diluted_market_cap": self.get_diluted_market_cap(soup),
            "contracts": self.get_contracts(soup),
            "official_links": self.get_official_links(soup),
        }
        
        return data

    def get_price(self, soup):
        price_tag = soup.find('span', class_='sc-d1ede7e3-0 fsQm base-text')
        return float(price_tag.text.strip('$').replace(',', '')) if price_tag else None

    def get_price_change(self, soup):
        change_tag = soup.find('p', class_='sc-71024e3e-0 sc-58c82cf9-1 ihXFUo iPawMI')
        return float(change_tag.text.split('%')[0].strip()) if change_tag else None

    def get_market_cap(self, soup):
        base_text_tags = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')
        if len(base_text_tags) > 0:
            market_cap_text = base_text_tags[0].text.strip()
            market_cap_value = market_cap_text.split('$')[-1].replace(',', '')
            return float(market_cap_value)
        return None

    def get_market_cap_rank(self, soup):
        market_cap_rank_tag = soup.find('span', class_='text slider-value rank-value')
        return int(market_cap_rank_tag.text.strip('#')) if market_cap_rank_tag else None

    def get_volume(self, soup):
        base_text_tags = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')
        if len(base_text_tags) > 1:
            volume_text = base_text_tags[1].text.strip()
            dollar_value_text = volume_text.split('$')
            dollar_value = float(dollar_value_text[1].replace(',', ''))
            return dollar_value
        return None

    def get_volume_rank(self, soup):
        market_cap_rank_tag = soup.find('span', class_='text slider-value rank-value')
        volume_rank_tag = market_cap_rank_tag.find_next('span', class_='text slider-value rank-value')
        return int(volume_rank_tag.text.replace('#', '')) if volume_rank_tag else None

    def get_volume_change(self, soup):
        base_text_tags = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')
        if len(base_text_tags) > 2:
            volume_change_text = base_text_tags[2].text.strip()
            volume_change_value = volume_change_text.split('%')[0]
            return float(volume_change_value)
        return None

    def get_circulating_supply(self, soup):
        base_text_tags = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')
        if len(base_text_tags) > 3:
            circulating_supply_text = base_text_tags[3].text.strip()
            list_circulating_supply_value = list(circulating_supply_text.split())
            t_circulating_supply_value = float(list_circulating_supply_value[0].replace(',',''))
            return t_circulating_supply_value
            #return float(circulating_supply_value)
        return None

    def get_total_supply(self, soup):
        base_text_tags = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')
        if len(base_text_tags) > 4:
            total_supply_text = base_text_tags[4].text.strip().replace(',', '')
            list_total_supply_value = total_supply_text.split()
            total_supply_value = float(list_total_supply_value[0])
            return float(total_supply_value)
        return None

    def get_max_supply(self, soup):
        base_text_tags = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')
        if len(base_text_tags) > 5:
            max_supply_text = base_text_tags[5].text.strip().replace(',', '')
            list_max_supply_value = max_supply_text.split()
            max_supply_value = list_max_supply_value[0]
            if max_supply_value == '--':
                return None
            return float(max_supply_value)
        return None

    def get_diluted_market_cap(self, soup):
        base_text_tags = soup.find_all('dd', class_='sc-d1ede7e3-0 hPHvUM base-text')
        if len(base_text_tags) > 6:
            diluted_market_cap_text = base_text_tags[6].text.strip()
            diluted_market_cap_value = diluted_market_cap_text.replace(',', '').strip('$')
            return float(diluted_market_cap_value)
        return None

    def get_contracts(self, soup):
        contract_info = soup.find_all('a', class_='chain-name')
        href_list = [tag['href'] for tag in contract_info]
        return href_list

    def get_official_links(self, soup):
        official_links = []
        href_list = self.get_contracts(soup)
        link_tags = soup.find_all('a', rel='nofollow noopener')
        for link_tag in link_tags:
            name = link_tag.get_text(strip=True)
            link = link_tag['href']
            if link not in href_list:
                official_links.append(link)
        return official_links