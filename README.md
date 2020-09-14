# Selenium+Pytest自动化测试框架

> 测试框架的整体目录

- common	这个包中存放的是常见的通用的类	
 - onfig	配置文件目录	
 - logs	日志目录	
-  page	对selenium的方放进行深度的封装	
 - page_element	页面元素存放目录	
  - page_object	页面对象POM设计模式
- report	报告文件目录	
- TestCase	所有的测试用例集	
- tools	工具类	
- conftest.py	常用目录等
- pytest.ini	pytest配置文件	
通过上图我们可以看出，通过POM模型思想，我们把：

页面元素

页面行为

测试用例
元素组成了页面行为，各种行为组合成了我们的测试用例。
以上四种代码主体进行了拆分，虽然在用例很少的情况下做会增加代码，但是当用例多的时候意义很大，代码量会在用例增加的时候显著减少。我们维护代码变得更加直观明显，代码可读性也变得比工厂模式强很多，代码复用率也极大的得到了提高。

#### 无聊的背景
  其实做测试最早接触的就是UI自动化，当时看着觉得很酷，页面自己会动。那个老师是这么说的，成熟的自动化工程师看着脚本跑就行了
  当时觉得这工作也太适合我这个懒人了，于是入了坑。当然现在看来有点单纯了。（废话...） 
  之前是用java写的，但是java还是不太适合测试，要注意的点太多，语法也比较复杂，当然写起来也很麻烦。主要是社区上很少有人用java去写
  导致讨论量不够，遇到问题排查起来无从下手。
  ##### 需求引起项目 
  大家也都知道UI自动化最关键的作用就是做回归测试，很多时候开发要回归测一遍，产品要回归测一遍，一点点小需求也要走一遍流程，说实话很痛苦
  ，相信大家也都经历过。所以一套自动化的回归流程就能解放我们的双手。所以我决定重拾UI自动化。（肯定很多人说干嘛不做接口，接口用jmeter在做，暂时不打算做成自动化）
 最后，UI自动化测试的框架和平台形形色色，不用评论哪个好，哪个差。只有最合适项目团队的才是最好的。（废话...）  

    本文代码github：https://github.com/Aron-01/pytest 

    话不多说，先上Jenkins上自助运行用例，查看报告流程截图。也可结合持续集成自动触发测试服务。

## 一、方案介绍
### ①. 选型：python + pytest + allure  + Git  + Jenkins +selenium
- 使用python作为项目编程语言，毕竟大势所趋。
- 使用pytest作为项目运行框架，方便执行调度测试用例。
- 使用allure作为报告驱动，增加错误报告截图，二次美化功能，界面更美观，内容清晰
- 使用Git作为仓库管理工具，方便管理项目代码。
- 使用Jenkins作为自动化持续集成平台，方便自动编译，自动打包，自动运行测试脚本，邮件发送测试报告，通知等。

### ②. 功能介绍：
0.  实现持续集成测试，自助式测试，一站式测试平台。
1.  通过yaml作为管理页面元素的工具，使用方便简洁。同时可分离用例与元素，方便元素重复调用。
2.  二次封装basepage，分离元素定位器，编写用例更快捷，只需考虑元素。
3.  pytest管理调度用例，方便调试以及单独项目运行

## 二、环境安装与配置
#### （一）开发环境：
1. python3 及以上
2. PYCHARM 社区版（壕->pro）
3. selenium3 不限
4. Git  不限
5. Jenkins 不限

#### （二）环境安装细节：
##### 1. 环境配置部分不解释了，常规安装，无特殊之处
##### 2. Jenkins本地安装，因为涉及到截图功能所以暂时不考虑liunx运行，公司环境外加了一台windows节点跑脚本。

*若遇网站需要翻墙，具体下载安装请自行百度。*

### (三) pytest配置部分
##### 3.1. 在根目录下创建conftest
后续因为在jenkins上运行所以邮件用jenkins来发，conftest只保留driver初始化，以及截图功能。
 ```
 @pytest.fixture(scope='session', autouse=True)
def drivers(request):
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-infobars')
        options.add_argument('--blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(options=options)
    inspect_element()
    testclear()
    

    def fn():
        driver.quit()

    request.addfinalizer(fn)
    return driver


def _capture_screenshot():
    '''
    截图保存为base64
    '''
    now_time = datetime_strftime("%Y%m%d%H%M%S")
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    screen_path = os.path.join(SCREENSHOT_DIR, "{}.png".format(now_time))
    driver.save_screenshot(screen_path)
    allure.attach.file(screen_path, "测试失败截图...{}".format(
        now_time), allure.attachment_type.PNG)
    with open(screen_path, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()
  ```
###### 3.1.1 每个文件夹可以是独立模块，每个模块下可以有模块的测试集合。
- 例如，在testcase下创建测试集合：使用pytest.mark 标记用例集合。配置如下：
    ```
  @allure.feature("jzyx-基本流程")
@pytest.mark.flaky(reruns=2, reruns_delay=5)
class TestCreatpl:

    @pytest.fixture(scope='function', autouse=True)
    def create(self, drivers):
        Create = Createpl(drivers)
        Create.get_url(ini.url)
        Create.login()


    # @pytest.mark.skip(reason="no way of currently testing this")
    # @pytest.mark.run(order=1)
    @pytest.mark.zjyx
    @allure.story("创建计划-输入内容-提交计划")
    def test_cp(self, drivers):
        """点击营销
            创建计划
            选择人群包-输入计划内容"""
        Create = Createpl(drivers)
        Create.clickprecision()
        Create.Selectcrowd()
        Create.Fillplan()

    # @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.jzyx
    @allure.story("创建人群包-创建")
    def test_cr(self, drivers):
        uploading = upload(drivers)
        uploading.up()
    @pytest.mark.jzyx
    @allure.story("创建人群包-搜索")
    def test_sr(self, drivers):
        uploading = upload(drivers)
        uploading.search_r()
    ```



### （四） TestCase测试用例
##### 4.1 Test用例类
- 首先，满足pytest工程结构在类名以Test_开头.```如：Test_ayx.java```
- 其次，用feature标记整体流程，fixture开始流程。
 ```
  
    @pytest.fixture(scope='function', autouse=True)
    def create(self, drivers):
        bd = bd_test(drivers)
        bd.get_url(ini.bdurl)
        bd.login()

    # @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.bd
    @allure.story("创建人群包-搜索")
    def test_cw(self, drivers):
        bd = bd_test(drivers)
        bd.createcw()
 ```
##### 4.2 测试用例怎么写？
- 目前的用例我是用项目来区别的，当然项目庞大的话你也可以用模块来区分，怎么区分也是一个学问，合适就行
 但是要符合用例的独立性，减少用例间的依赖。用例的话尽量封装一些会重复使用的流程，流程也不要定的过长。

-  这里添加了markers，用于单独调用某一类用例，方便调式。
```
 [pytest]
markers =
jzyx
bd
```
###### 4.3 说明
- 我这边分离页面元素是用yaml来保存页面元素，中文是用来说明元素的名称，里面还包含了定位器以及元素本身。
```
用户名: "id==username"
密码: "id==password"
登录: "xpath==//input[@class='logininfo_submit']"
```
用了一个readelement的方法来读取我的页面元素
```
 def __init__(self, name):
        self.file_name = '%s.yaml' % name
        self.element_path = os.path.join(ELEMENT_PATH, self.file_name)
        if not os.path.exists(self.element_path):
            raise FileNotFoundError("%s 文件不存在！" % self.element_path)
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, item):
        """获取属性"""
        data = self.data.get(item)
        if data:
            name, value = data.split('==')
            return name, value
        raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))
 ```
 这样的话，我们在调用元素的时候，就可以写成这样
  ```
  self.send_key(search['用户名'], ini.bdaccount)
  self.send_key(search['密码'], ini.bdpasswd)
  --------------------------------------------
  public WebElement getLink_PersonName(){
		String xpath = "//div[@class='person-name']/span"; 
		return getElment(By.xpath(xpath));
  
  public void input_Password(){
		driver.sendKeysEvent(orderPayPage.getLink_PersonName(), pageName, "输入储值卡支付密码", "123456");
	}
	}
  ```
  
  self调用basepage的方法，再放入locator，中文字符又可以当解释，又成为了一种参数，一举两得，这边我们可以看下以前的java方法对下，就可以清晰认知到这样封装以后
  哪怕以后回过头来看，都可以马上捡回来。不得不说python这样写起来真是快啊。
  关于断言这块就不多写了，我目前断言做的比较少，可能是业务的关系吧，放一段断言示例吧
    ```
        def get_result(self):
        a=self.get_text(search['待审核'])
        return a
        log.info("待审核=：{}".format(a))
        ------------------------------------
     result = Create.get_result()
        log.info("结果".format(result))
        assert  result== "提交成功，等待审核..."
      ```
  

### （五） allure报告
> allure是什么？网上有很多关于使用allure替代pytest自带报告。原因是什么？
> 漂亮。先上张图。

![](https://docs.qameta.io/allure/images/get_started_report_overview.png)
官网很重要：https://docs.qameta.io/allure/. 其实官网已经给了很多demo了，这里我根据自己的经验进行了配置。

pytest原有报告有点丑，信息整理有点乱。allure是用于替换pytest原有的报告。
##### 5.1 如何使用allure
跟pytest差不多，都是约定大于规则。在我的测试用例标记上的fearture/story.allure
会自动收集这些信息并生产报告。
```
call pytest -s -q --reruns=0 --alluredir allure-results --clean-alluredir
```
只需要输入生产报告命令，忘了说它跟pytest命令集成的非常好。后续的与jenkins集成具体可以参考网上的资料，非常多。
    至此，allure美化报告完成。


### （六）. selenium测试驱动原力
> 做UI自动化的没的说，那肯定是selenium了，现在selenium的官方文档也更新过了
现在连官方文档都开始推荐使用POM模式了，大家有兴趣的可以去看看https://www.selenium.dev/documentation/en/getting_started/
首先我们要做肯定是对于selenium原方法的封装，主要是统一方法，方便调用，每个用例都继承这个基类
```
@staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素"""
        return Page.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)

    def find_elements(self, locator):
        """查找多个相同的元素"""
        return Page.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def isclick(self, locator):
        """点击"""
        """点击"""
        self.find_element(locator).click()
        sleep()
        log.info("点击元素：{}".format(locator))

    def on_page(self, pagetitle):
        return pagetitle in self.driver.title

    def get_url(self, base_url):
        """打开网址并验证"""
        self.driver.set_window_size(1600,900)
        log.info("设置页面大小")
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(base_url)
            self.driver.implicitly_wait(10)
            log.info("打开网页：%s" % base_url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % base_url)
 ```




### 四、Jenkins部分配置
> Jenkins的安装上面已有说明，这里不重复。





#### （六） 参数化构建过程 配置
  - 6.1添加参数 选择是 【选项参数】。
    ![](https://img2020.cnblogs.com/blog/1789010/202009/1789010-20200914163240842-1308016030.png)
    参数化
    ![](https://img2020.cnblogs.com/blog/1789010/202009/1789010-20200914163418508-2036618630.png)
    将变量写入命令行
     ![](https://img2020.cnblogs.com/blog/1789010/202009/1789010-20200914163328205-886974637.png)
    

#### （七） 源码管理配置
这个配置网上有很多详细文档，这里不重复。具体度娘查看。
    ![image.png](https://upload-images.jianshu.io/upload_images/1592745-f6d102928da390fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### （八） 构建触发器
    > 这个配置可根据实际项目需求配置。个人建议: 自动化测试中的自动化最核心的是结合持续构建。   
    > 所以建议配置“代码提交时构建”，也可以填入所需测试的服务端项目构建后构建。当然要在一个Jenkins中。
  ![image.png](https://img2020.cnblogs.com/blog/1789010/202009/1789010-20200914163318399-692905750.png)

### （十） 构建后操作信息配置
##### 9.1. allure html reports
![](https://img2020.cnblogs.com/blog/1789010/202009/1789010-20200914163344378-596730886.png)

#####  9.2 publish html reports
    通过jenkins发邮件通知结果。 
   ![image.png](https://img2020.cnblogs.com/blog/1789010/202009/1789010-20200914164139013-296597951.png)

#####  9.3. 钉钉通知器配置
    怎么玩转钉钉消息？查看https://blog.csdn.net/workdsz/article/details/77531802
    - 填入access token。
![image.png](https://upload-images.jianshu.io/upload_images/1592745-4e1ca2a4d34564d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)




   
#### 写在最后
其实，UI自动化测试平台的搞起来不难。
推动平台接入到持续集成，将测试变成一种服务，更快更及时的服务于项目，才是重点。



欢迎Watch + Fork
end...
    
    
