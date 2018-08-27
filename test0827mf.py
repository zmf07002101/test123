# -*- coding:UTF-8 -*-

__author__ = 'zmf'
__date__ = '2018/5/14 16:46'
'''
jpg登录测试，分下面几种情况： 
(1)用户名、密码正确 
(2)用户名正确、密码不正确 
(3)用户名正确、密码为空 
(4)用户名错误、密码正确 
(5)用户名为空、密码正确 
（还有其他情况，如无权限用户，被锁定用户等，就不出来了）
'''
'''
加入需要的python库: 
unittest为python的测试框架 
webdriver为python的selenium下的库 
sleep为睡眠时间，类似于lr的思考时间，页面停留，也可以直接写import time，但是用法就是time.sleep() 
os是为了创建目录time获取日期和时间 
'''
import unittest
from selenium import webdriver
from time import sleep
import os
import time
from HTMLTestRunner import HTMLTestRunner

#定义打开浏览器的方法，这里用的是Chrome，火狐为Firfox，IE为Ie，必须在根目录下对应的driver才能调用
dr = webdriver.Chrome()

#浏览器最大化
dr.maximize_window()


#创建测试类LoginCase，用unittest的测试框架的格式
class LoginCase(unittest.TestCase):
    #定义登录方法，被测试用例调用
    def login(self,username,password):
        #需要测试的网页
        dr.get('https://passport.cnblogs.com/user/signin')
        #需要输入的用户名，变量名和方法中的一致，find_element_by_id('input1')为抓取到的用户名的输入框，用谷歌或者火狐F12可以抓取到
        dr.find_element_by_id('input1').send_keys(username)
        #需要输入的密码，变量名和方法中的一致，find_element_by_id('input2')为抓取到的密码的输入框
        dr.find_element_by_id('input2').send_keys(password)
        #点击登录按钮，find_element_by_id('signin')为抓取到的登录按钮，click()为点击事件
        dr.find_element_by_id('signin').click()


    #定义测试方法，框架中的测试方法以test_开头，底下引号中的中文会在报告中显示，利于清楚的知道测试目的
    def test_login_success(self):
        '''用户名、密码正确'''
        self.login('晨曦Test','Qweqwe213@')#调用定义的login方法，传入正确用户名和密码
        sleep(3)

        #可以用get_screenshot_as_file方法来截图，可自定义截图后保存的位置和图片命名
        dr.get_screenshot_as_file(path+'login_sucess.jpg')

        #定义了一个实际值，用谷歌或者火狐F12可以抓取到登录后显示的用户名，.text是获取地址的文本值
        #assert先判断需要的实际值是否正确。正确，继续运行用例；不正确，不继续运行该用例并返回错误；
        assert dr.find_element_by_id('lnk_current_user').text,'判断的元素错误，请确认！'

        #将实际值赋值给一个变量link，方便比较，可自定义
        link = dr.find_element_by_id('lnk_current_user').text

        #用assertTrue(x)方法来判断断言，登录成功后预期的值是否和定义的实际值一致
        self.assertTrue('晨曦TestOk' in link)


    def test_login_pwd_error(self):
        '''用户名正确、密码不正确'''
        self.login('晨曦Test','1')#正确用户名，错误密码
        sleep(3)
        dr.get_screenshot_as_file(path+'login_password_error.jpg')
        assert dr.find_element_by_id('tip_btn').text,'提示信息类型错误'
        error_message = dr.find_element_by_id('tip_btn').text
        self.assertIn('用户名或者密码错误',error_message) #用assertIn(a,b)方法来断言


    def test_login_pwd_null(self):
        '''用户名正确、密码为空'''
        self.login('晨曦Test','') #密码为空
        sleep(3)
        dr.get_screenshot_as_file(path+'login_password_null.jpg')
        assert dr.find_element_by_id('tip_input2').text,'提示信息类型错误'
        error_message = dr.find_element_by_id('tip_input2').text
        self.assertEqual(error_message,'请输入密码') #用assertEqual(a,b)方法来判断


    def test_login_user_error(self):
        '''用户名错误、密码正确'''
        self.login('1','Qweqwe213@') #密码正确，用户名错误
        sleep(3)
        dr.get_screenshot_as_file(path+'login_username_error.jpg')
        assert dr.find_element_by_id('tip_btn').text,'提示信息类型错误！'
        error_message = dr.find_element_by_id('tip_btn').text
        self.assertIn('用户不存在',error_message) #用assertIn(a,b)方法来断言a in b


    def test_login_user_null(self):
        '''用户名为空，密码正确'''
        self.login('','Qweqwe123@') #用户名为空，密码正确
        sleep(3)
        dr.get_screenshot_as_file(path+'login_username_null.jpg')
        error_message = dr.find_element_by_id('tip_input1').text
        assert (error_message,'提示信息类型错误！')
        self.assertEqual(error_message,'请输入登录用户名') #用assertEqual(a,b)方法来断言


    #每个test_执行完，则执行一次tearDown（）方法
    def tearDown(self):
        sleep(1)
        #refresh()方法为刷新浏览器
        dr.refresh()

if __name__ == '__main__':
    #定义脚本标题，加u为了防止中文乱码
    report_title = u'登录模块测试报告'

    #定义脚本内容，加u为了防止中文乱码
    desc = u'博客园登录模块测试报告详情'

    #定义date为日期，time为时间
    date = time.strftime('%Y%m%d')
    time = time.strftime('%Y%m%d%H%M%S')

    #定义path为文件路径，目录级别，可根据实际实际情况自定义修改
    path ='E:/My_script/Test_screenshot/' + date + '/login/' + time + '/'

    #定义报告文件路径和名字，路径为前面定义的path，名字为report（可自定义），格式为.html
    report_path = path + 'report.html'

    #判断是否定义的路径目录存在，不存在则创建
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass

    #定义一个测试容器
    testsuite = unittest.TestSuite()

    #将测试用例添加到容器
    testsuite.addTest(LoginCase('test_login_success'))
    testsuite.addTest(LoginCase('test_login_pwd_error'))
    testsuite.addTest(LoginCase('test_login_pwd_null'))
    testsuite.addTest(LoginCase('test_login_user_error'))
    testsuite.addTest(LoginCase('test_login_user_null'))

    #将运行结果保存到report，名字为定义的路径和文件名，运行脚本
    with open(report_path,'wb') as report:
        runner = HTMLTestRunner(stream=report,title=report_title,description=desc)
        runner.run(testsuite)

    #关闭report，脚本结束
    report.close()
    #关闭浏览器
    dr.quit()