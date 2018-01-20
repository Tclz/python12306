# python12306
使用python2.x购买12306火车票

当前需要手动输入验证码  自动识别图片据说效率很低 暂时没想去实现
要运行的话 将configure/conf.ini文件中的信息正确填写一下 跑ticket_order/buy_ticket.py
(直接运行测试的是查找硬卧的信息,其他席别还需在train_data/get_train_data.py中对data_list[]中的下标进行相应修改 不同下标对应不同席别 以及火车的一些其他信息)
整个购票流程/逻辑 在buy_ticket.py中描述的比较清楚了 不想在这写了




