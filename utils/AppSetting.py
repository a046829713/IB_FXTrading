class AppSetting():
    def coin_map():
        data = {}
        data['CNH'] = '中國元離岸'
        data['KRW'] = '韓國圜'
        data['MXN'] = '墨西哥比索'
        data['CAD'] = '加拿大元'
        data['SGD'] = '新加坡元'
        data['ZAR'] = '南非蘭特'
        data['NOK'] = '挪威克朗'
        data['RUB'] = '俄羅斯盧布'
        data['CHF'] = '瑞士法郎'
        data['DKK'] = '丹麥克朗'
        data['HKD'] = '香港元'
        data['ILS'] = '以色列謝克爾'
        data['SEK'] = '瑞典克朗'
        data['CZK'] = '捷克克朗'
        data['JPY'] = '日元'
        data['HUF'] = '匈牙利福林'
        data['PLN'] = '波蘭茲羅提'
        return data

    def use_map():
        USEMAP = ['USD.JPY', 'USD.CAD', 'USD.SGD', 'USD.HKD']
