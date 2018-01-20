# _*_ coding: utf-8 _*_

from aip import AipOcr

# 定义常量
APP_ID = '10719079'
API_KEY = 'tjdAIZ0pd8kuIMHI9wk8Adc7'
SECRET_KEY = 'L4txQ70M2PaPmh0DiX3x7TNUm2qUweW5'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# 参数
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}

class BaiduAip:
    """ 读取图片 """
    def get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    """ 调用通用文字识别, 图片参数为本地图片 """
    def get_result(self,img_url):
        image = self.get_file_content(img_url)
        return client.basicGeneral(image,options)

if __name__ == '__main__':
    baidu_aip = BaiduAip()
    result = baidu_aip.get_result('../img/code.png')
    words = result['words_result'][0]['words']
    print (words)