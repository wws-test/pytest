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

###### 3.1.3 说明
- 目前的用例我是用项目来区别的，当然项目庞大的话你也可以用模块来区分，怎么区分也是一个学问，合适就行
 但是要符合用例的独立性，减少用例间的依赖。

-  这里添加了markers，用于单独调用某一类用例，方便调式。
```
 [pytest]
markers =
jzyx
bd
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

##### 6.2 HttpBase基础类提供原动力。
HttpBase类中提供了Retrofit基础。
同时，我考虑到了日常控制台和测试报告上都需要看到对应请求信息，故此在HttpClient中默认加入了日志拦截器；日志拦截器的实现方法里，用Reportes.log记录到日志中。
并且，考虑到实际项目中每个Http请求都会有对应类似RequestHeader、RequestBody的加密签名等，预留了拦截器。
可在HttpBase构造方法时传入对应拦截器。
对应的拦截器可以通过实现接口Interceptor，做对应项目需求操作。
先看代码。
```
public class HttpBase {
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    private Retrofit retrofit;
    private String host;

    /**
     * 构造方法（1个参数）
     * 只传Host，默认没有使用拦截器。
     *
     * @param host 访问域名host
     */
    public HttpBase(String host) {
        init(host, null);
    }

    /**
     * 构造方法（2个参数）
     * 只传Host，默认使用日志拦截器。
     *
     * @param host        访问域名host
     * @param interceptor 自定义拦截器
     */
    public HttpBase(String host, Interceptor interceptor) {
        init(host, interceptor);
    }

    /**
     * 初始化方法
     *
     * @param host        访问域名host
     * @param interceptor 自定义拦截器
     */
    private void init(String host, Interceptor interceptor) {
        OkHttpClient.Builder client = getHttpClient(interceptor);
        retrofit = new Retrofit.Builder()
                .baseUrl(host)
                .client(client.build())
                .addConverterFactory(RespVoConverterFactory.create())
                .build();
    }

    /**
     * 获取HttpClient.Builder 方法。
     * 默认添加了，基础日志拦截器
     *
     * @param interceptor 拦截器
     * @return HttpClient.Builder对象
     */
    private OkHttpClient.Builder getHttpClient(Interceptor interceptor) {
        HttpLoggingInterceptor logging = getHttpLoggingInterceptor();
        OkHttpClient.Builder builder = new OkHttpClient.Builder()
                .connectTimeout(10, TimeUnit.SECONDS)
                .retryOnConnectionFailure(true);
        if (interceptor != null) {
            builder.addInterceptor(interceptor);
        }
        builder.addInterceptor(logging);
        return builder;
    }

    /**
     * 日志拦截器
     *
     * @return
     */
    private HttpLoggingInterceptor getHttpLoggingInterceptor() {
        HttpLoggingInterceptor logging = new HttpLoggingInterceptor(new HttpLoggingInterceptor.Logger() {
            @Override
            public void log(String message) {
                Reporter.log("RetrofitLog--> " + message, true);
            }
        });
        logging.setLevel(HttpLoggingInterceptor.Level.BODY);//Level中还有其他等级. 设置打印内容级别到Body。
        return logging;
    }

    /**
     * retrofit构建方法
     *
     * @param clazz 泛型类
     * @param <T>   泛型类
     * @return 泛型类
     */
    public <T> T create(Class<T> clazz) {
        return retrofit.create(clazz);
    }

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }
}
```


##### 6.3 集成HttpBase的Http Api接口请求方法类
这里需要说明下，为什么需要有这个类的存在？
其实在Retrofit已经可以用4行的代码实现Http请求了，如下：
```
        HttpBase httpBase = new HttpBase(host);
        ISearch iSearch = httpBase.create(ISearch.class);
        Call<MovieResponseVO> call = iSearch.searchTags(type, source);
        Response<MovieResponseVO> response = call.execute();
```
看了上面的4行代码，每次都需要写也是挺麻烦的。
所以抽出来，让编写测试用例验证更简洁点。
抽取后的代码如下：
```
public class HttpSearch extends HttpBase {
    private ISearch iSearch;

    public HttpSearch(String host) {
        super(host);
        iSearch = super.create(ISearch.class);
    }

    public Response<MovieResponseVO> searchTags(String type, String source) throws IOException {
        Call<MovieResponseVO> call = iSearch.searchTags(type, source);
        return call.execute();
    }

//    同模块下，新增的接口可添加到这里。
//    public Response<MovieResponseVO> searchTags(String type, String source) throws IOException {
//        Call<MovieResponseVO> call = iSearch.searchTags(type, source);
//        return call.execute();
//    }
}
```

##### 6.4 使用aerrt验证基础响应体



### 四、Jenkins部分配置
> Jenkins的安装上面已有说明，这里不重复。

#### （一） Jenkins插件
##### 1.插件列表
需要使用到的插件有：
- Maven Integration plugin
- HTML Publisher plugin
- Dingding[钉钉] Plugin
- TestNG Results
- Groovy
- Parameterized Trigger Plugin

##### 2. Jenkins插件安装
怎么安装插件？
Jenkins-》系统管理-》插件管理-》搜索插件-》安装即可

 ![](https://upload-images.jianshu.io/upload_images/1592745-c726c78951c2ccd1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##### 3. 插件说明
  -  Maven Integration plugin -必备！
Maven构建插件，使用简单方便。 

- HTML Publisher plugin -必备！
extentreporets美化报告替换testng就是为了好看，但要在jenkins中展示必须安装此插件。

-  Groovy -必备！
Jenkins不支持异类样式CSS，所以Groovy插件是为了解决HTML Publisher plugin在展示extentreporets时能够正确美丽的作用。

- Dingding[钉钉] Plugin -必备！
测试用例构建结果的通知。网上很多说用邮件，说实话使用场景最频繁高效的应该是IM靠谱。这个插件就是解决测试结果的通知。

- TestNG Results - 非必备
TestNg测试结果收集，统计运行结果数据。

- Parameterized Trigger Pl ugin - 非必备
依赖构建传参插件。http://note.youdao.com/noteshare?id=c56333317d3078b36b2479fdf8fe68d7&sub=wcp1530172849180570

#### （二）Jenkins新建任务配置
在插件安装完后，开始任务的新建配置。
- 新建一个maven项目。
    ![image.png](https://upload-images.jianshu.io/upload_images/1592745-9d512595d8e7b610.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### （三）General配置
- 丢弃旧的构建配置 -可配
该配置根据需求配置。
  ![image.png](https://upload-images.jianshu.io/upload_images/1592745-f1e48f5e13c01fa0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### （四） 构建配置-maven配置
在Jenkins使用Maven构建项目自动化测试前，先通过本地使用maven测试是否通过。
这里本来要将参数化构建，但参数化构建前先说明下是如何利用maven构建测试的。




#### （六） 参数化构建过程 配置
  - 6.1添加参数 选择是 【选项参数】。
    ![](https://upload-images.jianshu.io/upload_images/1592745-0486fbca91a38367.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

  - 6.2完整配置信息如下图。
        ![](https://upload-images.jianshu.io/upload_images/1592745-f586ae3356c5dd3b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
        
  - 6.3参数名称xmlFileName，对应maven构建中的-DxmlFileName=%xmlFileName%，再对应pom.xml中的```<suiteXmlFile>${project.basedir}/target/classes/testNg/${xmlFileName}</suiteXmlFile>```
    加入需要运行的集合选项。
  - 6.4 同样，env对应maven构建中的 -P%env% ，再对应pom.xml中的build信息。
    加入运行的环境选项。

#### （七） 源码管理配置
这个配置网上有很多详细文档，这里不重复。具体度娘查看。
    ![image.png](https://upload-images.jianshu.io/upload_images/1592745-f6d102928da390fe.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### （八） 构建触发器
    > 这个配置可根据实际项目需求配置。个人建议: 接口自动化测试中的自动化最核心的是结合持续构建。   
    > 所以建议配置“其他工程构建后触发”，填入所需测试的服务端项目名称即可。当然要在一个Jenkins中。
  ![image.png](https://upload-images.jianshu.io/upload_images/1592745-5c69a2115ce3327c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### （九） 构建信息配置    
    > 上面已经配置了“调用顶层Maven目标”，然后还需要配置Groovy script。  
    > 配置Groovy script的目的是让Http Reported插件css能用，同时不用担心jenkins重启。

- 配置Groovy script前保障Groovy 插件已经安装。
- 增加构建步骤“Execute system Groovy script” ，选择Groovy command，填入```System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")```
    
    ![](https://upload-images.jianshu.io/upload_images/1592745-9a3742f57a4ed0d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

### （十） 构建后操作信息配置
##### 9.1. publish html reports
    加入publish html reports步骤。
    - HTML directory to archive： 报告路径。 填写extentreports默认输出路径：test-output\
    - Index page[s] ： 报告索引名称。填写extentreports默认报告名称：report.html
    - Keep past HTML reports： 保留报告，勾选！不多说。
![](https://upload-images.jianshu.io/upload_images/1592745-9143ff5424476c8d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#####  9.2 publish html reports
    publish testng results 配置。默认**/testng-results.xml 即可。 
    为什么要testng默认报告？ 因为需要统计分析时查看。 当然这个是可选的。
   ![image.png](https://upload-images.jianshu.io/upload_images/1592745-9625b6b2ec2e35df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#####  9.3. 钉钉通知器配置
    怎么玩转钉钉消息？查看https://blog.csdn.net/workdsz/article/details/77531802
    - 填入access token。
![image.png](https://upload-images.jianshu.io/upload_images/1592745-4e1ca2a4d34564d4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

##### 4. 构建后操作信息配置 钉钉通知器配置 二次开发 - 可选      
    http://www.51testing.com/html/25/n-3723525.html


   
#### 写在最后
其实，接口自动化测试平台的搞起来不难。
推动平台接入到持续集成，将测试变成一种服务，更快更及时的服务于项目，才是重点。
正所谓：wiki一定，开发未动，接口已行。
而，服务端测试才挑战。知识储备的深度决定了，测试的深度。

个人GitHub:  https://github.com/Jsir07/TestHub
欢迎Watch + Fork
end...
    
    
