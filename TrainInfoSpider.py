import urllib2

class TrainInfoSpider:

    #12306余票查询地址
    url = "https://kyfw.12306.cn/otn/leftTicket/queryT?" \
          "leftTicketDTO.train_date=2016-02-14&" \
          "leftTicketDTO.from_station=SNQ&" \
          "leftTicketDTO.to_station=GZQ&" \
          "purpose_codes=ADULT"

    def __init__(self, data):
        self.query_date = data.date
        self.from_station = data.from_station
        self.to_station = data.to_sattion

    def queryTrainInfo(self, date, t_train_code):
        req=urllib2.Request(url)
        res=urllib2.urlopen(req)
        json_data=res.read()

        data=json.loads(json_data)

        for index in range(len(data['data'])):
            #print data['data'][index]['queryLeftNewDTO']['station_train_code']+'\t'+data['data'][index]['queryLeftNewDTO']['start_station_name']+'---'+data['data'][index]['queryLeftNewDTO']['end_station_name']+'\t'+data['data'][index]['queryLeftNewDTO']['from_station_name']+u'发时时间:'+data['data'][index]['queryLeftNewDTO']['start_time']+u'到达时间:'+data['data'][index]['queryLeftNewDTO']['arrive_time']+u'历时:'+data['data'][index]['queryLeftNewDTO']['lishiValue']
            train_code=data['data'][index]['queryLeftNewDTO']['station_train_code']
            if(train_code==t_train_code):

