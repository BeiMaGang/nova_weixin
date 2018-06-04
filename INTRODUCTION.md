# Guide to nova_weixin
## 项目结构
### app
在app 中，包含了网站的主要逻辑
#### auth
即.../auth/ 的蓝图
#### bind
即.../bind/ 的蓝图
#### static
网页的img, js, css 等静态内容
#### templates
网页的jinja 模板
#### weixin
即.../ 的主要逻辑，包括了网站主页和控制微信开发的部分。