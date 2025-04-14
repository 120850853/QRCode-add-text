## qrcodewithtext

**Author:** liu
**Version:** 0.0.2
**Type:** tool

### Description
在二维码图片，下方添加文字描述

## Usage
1. 在配置文件中，要有如下配置
FILES_URL=http://your_domain

否则，会出现`Request URL is missing an 'http://' or 'https://'protocol`的错误提示

2. 把字体放到`./volumes/plugin_daemon/assets/`文件夹下。因为字体太大超过50M，无法打包，所以放到`./volumes/plugin_daemon/assets/`文件夹下。
