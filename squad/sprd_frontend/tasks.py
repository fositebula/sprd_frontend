from squad.celery import app as celery
from celery.utils.log import get_task_logger
from squad.sprd_frontend.models import DeviceType
from bs4 import BeautifulSoup

import requests

logger = get_task_logger(__name__)

def pac_node_spider(url):
    #http://10.0.70.113:8080/download-lava/autodaily/verify_daily_pac_sharkl3/{}/target/
    url = '/'.join(url.split('/')[:-3])
    r = requests.get(url)
    bs = BeautifulSoup(r.content, 'lxml')
    nodes = []
    for i in bs.select('table [align=left] tt'):
        if '.log' in i.get_text():
            # print i.parent.get('href')
            node_num = i.get_text().split('.')[0]
            nodes.append(node_num)

    nodes.sort()
    return nodes


@celery.task
def update_pac_node(device_type_id=None):
    if device_type_id == None:
        device_type = DeviceType.objects.all()
        for d in device_type:
            nodes = pac_node_spider(d.base_pac_url)
            d.pac_node = ','.join(nodes)
            d.save()
    else:
        device_type = DeviceType.objects.get(id=device_type_id)
        nodes = pac_node_spider(device_type.base_pac_url)
        device_type.pac_node = ','.join(nodes)
        device_type.save()

if __name__ == '__main__':
    ret = pac_node_spider('http://10.0.70.113:8080/download-lava/autodaily/verify_daily_pac_sharkl3/{}/target/')
    print(ret)