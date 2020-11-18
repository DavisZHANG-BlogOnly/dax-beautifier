### About DAX Beautifier

DAX Beautifier is a Power BI Desktop external tool developed by myself (Davis.Z), and it is also the first PBID external tool developed based on the Python language in the global Power BI community. Its function is to enable you to beautify all DAX formulas in the entire PBI file with one click, enhance code readability and greatly improve development efficiency.

The program directly interacts with Analysis Services. Based on the test of the current version (v 1.0.0 beta), it perfectly implements the one-click beautification of all DAX formulas (whether it is a calculated table, a calculated column or a measure)!

### Download and Install

Download: The current version (v1.0.0 beta) and subsequent versions will be released to this Github repositories(or [click here](https://github.com/DavisZHANG-BlogOnly/dax-beautifier/blob/master/dax-beautifier.zip)).

Install: Just run the .exe, as follow:

![Install](https://img-blog.csdnimg.cn/20200803110303755.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_RC1CSSB8IERhdmlzIG9uIEJJ,size_16,color_FFFFFF,t_70)

Besides, you can also install the tool by [BUSINESS OPS](https://powerbi.tips/).

### Prerequisites

1.Please confirm that your version of Power BI Desktop supports external tools (the version number should not be less than: 2.83.5894.661).

![Version](https://img-blog.csdnimg.cn/20200803110918521.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_RC1CSSB8IERhdmlzIG9uIEJJ,size_16,color_FFFFFF,t_70)

2.Confirm that you have enabled enhanced metadata for PBID：

![enhanced metadata](https://img-blog.csdnimg.cn/20200803111024197.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_RC1CSSB8IERhdmlzIG9uIEJJ,size_16,color_FFFFFF,t_70)

3.Make sure that your tabular model can be connected to the data source (if there is a situation similar to the figure below, it may cause the tool to fail)：

![Make sure connected to the data source](https://img-blog.csdnimg.cn/20200803111231330.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_RC1CSSB8IERhdmlzIG9uIEJJ,size_16,color_FFFFFF,t_70)

4.Make sure that the device where your report is located can connect to the Internet. Since the DAX beautification function of the tool needs to rely on the API provided by [daxformatter.com](https://www.daxformatter.com/), if you cannot connect to the Internet or the network is disconnected when the program is running, it may cause the tool to fail.


### Demo

The use of this tool can refer to the following video (It's very simple)：


<iframe width="560px" height="315px" allow="autoplay" src="https://youtu.be/JgLyNkpEeRo" name="iframeId" id="iframeId" frameborder="0" allowfullscreen="true" scrolling="no"></iframe>

### Limitations

Limited by the compatibility level of the calculation table, DAX formatting is temporarily unavailable for calculated columns in calculated tables.

### Q&A

Question: The program throw an exception:" Please install AMO library and make sure the path is correct."

*Answer: You need to install AMO library from [here](https://docs.microsoft.com/en-us/analysis-services/client-libraries?view=asallproducts-allversions) and make sure the path is "C:\Windows\Microsoft.NET\assembly\GAC_MSIL".*

Question: Why does the DAX in my PBI report have not changed after I use DAX Beautifier, and I have met all the prerequisites?

*Answer: In some cases, the formatted results returned by DAX Beautifier will not be reflected in Power BI Desktop immediately, but at this time the internal formatting of the model has been completed, you can save the report and restart the PBID to check. If the problem persists, please refresh the dataset and try again. In addition, if your formula itself has a grammatical error, it will retain the original format without being beautified.*

### Acknowledgment

Free API provided by Macro Russo's [DAX FORMATTER](https://www.daxformatter.com/)

![DAX FORMATTER](https://img-blog.csdnimg.cn/20200803114654732.png)

Sponsored by [PowerBI Quan](http://powerbiquan.com/)

![PowerBI Quan](https://img-blog.csdnimg.cn/20200803114617795.jpg)

And friends who helped test the tool before it was released.

### Updated

##### Version:1.0.3 (2020-11-18)

This version adds support for Power BI Report Server (PBIRS). 

Since PBIRS does not support external tools(as of November 2020), dax-beautifier.exe can run independently for it. 

To quickly format all DAX code, you just need to double-click the program itself or its shortcut.

*Note: This mode is only for PBIRS. If you use the standard version of PBID, you still need to run it from the external tools tab*

![v:1.0.3](https://img-blog.csdnimg.cn/20201118100407154.png)

PBIRS Requirements: Power BI Report Server (October 2020) or above versions.

##### Version:1.0.2 (2020-8-13)

Modify the icon size of the program.

Modify the setup.exe UI.

##### Version:1.0.1 (2020-8-7)

Users can choose to format only recently modified or created formulas instead of processing all formulas. You only need to enter an integer not less than zero in DAX Beautifier. For example, if you enter 0, it means that the program will formatting all formulas. If you enter 3, it means that the program will only beautify the modified ones (or the formula created) in the past 3 hours. 

![v:1.0.1](https://img-blog.csdnimg.cn/20200809190938949.png)



