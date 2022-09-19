# 使用 Github Actions 的爱跑自动跑步脚本

> 如果您认为`BIOS `是一种新的植物性燃料，或者`Python`是一种主要分布在东南亚的濒危动物，那么该项目可能不适合您。

在使用本脚本前，请确认跑步软件的名称为**阳光体育服务平台**，且Android包名为`com.aipao.hanmoveschool`。

## 使用方法

1. fork本项目；

2. 在你自己的仓库中，依次点击**Settings**，**Secrets**，**Actions**；

3. 点击**New repository secret**；

4. 在**Name**与**Secret**项目中填上以下值，其中需要将相应的值改为你自己的：

| Name        | Secret(示例)           | 备注                                    |
| :---------- | ---------------------- | --------------------------------------- |
| SMTP_SERVER | `smtp.example.com`     | smtp服务器地址                          |
| SMTP_PORT   | `465`                  | smtp服务器端口                          |
| SMTP_USER   | `mailfrom@example.com` | 送信邮箱地址                            |
| SMTP_PASSWD | `Passw0rd114514`       | 送信邮箱密码                            |
| SMTP_MAILTO | `mailto@example.com`   | 收信邮箱地址                            |
| IMEI        | `xxx`                  | 重要，跑步token，32位，可能需要定时更新 |

5. star自己的项目，如果能够跑步成功，则已经设置完成。

## IMEI获取方法

### Android客户端

使用`HttpCanary`抓包。由于应用的通信全部使用了`http`，因此无须安装CA证书。

开始抓包后，打开app，登录完成后停止抓包。找到某一数据包的响应为

```json
{
  "Success": true,
  "Data": {
    "Token": "xxx",
    "UserId": xxx,
    "IMEICode": "xxx",
    "AndroidVer": 2.40,
    "AppleVer": 1.24,
    "WinVer": 1.0
  }
}
```

其中`IMEICode`即为IMEI。

### iOS客户端

在同一局域网下的计算机安装`fiddler`，并开启代理模式并手机上配置代理。

下面的步骤同Android客户端，且该方法Android也可用。
