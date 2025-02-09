---
title: 部署VueJS静态网站到阿里云OSS
date: 2019-08-19 10:20:00 
categories: Nodejs
tags: [aliyun, web, vuejs, webpack, router]
---
`VueJS` 非常不错，对于一个后端开发也很友好。近期我有机会在写一个网站的时候接触了VueJS，虽然不是一个很专业的前端，但是感觉VueJS非常容易上手。
出于为了性能的需要，打算将该网站通过 `webpack` 编译后上传到阿里云的 `OSS` 作为静态网站发布，但是遇到了一些坑，特意将踩坑的过程分享一下。

首先在托管静态网站的时候，创建OSS桶需要注意两点配置：

1） OSS桶必须设置公共读，因为网站需要所有人都可以访问

2） OSS桶里有个默认首页的配置，需要配置成 `index.html`

因为使用了Vue-Router，在阿里云上一开始部署的时候有个严重的问题，就是在非主页刷新页面，OSS都找不到资源，这时候重新刷新，阿里云又找不到该目录下的这个文件，就会报找不到资源的错误。例如有一个路径是 `www.example.com/hello/world` ，通过主页 `www.example.com/index.html` 跳转到 `www.example.com/hello/worlds` 是正常的，但是当刷新页面，阿里云会直接去找OSS桶里的 `hello/world` 这个路径，发现找不到，直接报404.

然后发现阿里云里的设置，其实有个“默认 404 页”的设置，所以一开始异想天开，把默认页面设置成了 `index.html` ，结果虽然不报404了，却每次刷新都跳转到主页，显然也不符合我想要的想过。

然后我通过一番调研，发现原来是因为我的 Vue Router 配置，无法直接用阿里云OSS桶实现静态页面托管。

因为 Vue Router 有两种模式

1）`hash模式` ：用地址栏里的“#”来路由，不会改变实际的请求，例如 www.example.com/hello 和 www.example.com/hello#world 的Http请求是一样的，因此不需要改变请求，只通过#后面的内容进行路由

2）`history模式` ：用html5中的 pushState() 和 replaceState() 在不刷新页面的情况下实现路由跳转。

所有我的问题就很明显了，因为一开始我Vue Router的理解不够，认为history模式没有“#”看上去更加美观，就用了history模式。但是因为没有“#”，当刷新页面的时候，Http请求直接就去请求OSS桶里的该路径下的资源，结果当然是404了。我最后的解决方案便是放弃了美观，直接用了hash模式来托管网站，网站的路由就没有什么问题了。

但是我觉得，其实OSS不可以挂在history模式的VueJS似乎也不太可能，应该有别的方法。但是目前搜不到oss和vuejs的history模式相关的资料，只搜到部署到AWS S3的资料，里面的方法居然就是把 `404页` 跳转到 `index.html`。我的理解是 `OSS` 和 `S3` 并不完全相同，又或者我的Vue Router里面还有其他的配置需要调整，总之目前还不确定OSS能否成功实现history方式的VueJS网站托管。

找到的资料链接我先放在这里了，下次会再做一些尝试验证一下。


参考资料：

[HTML5 History Mode - Vue Offical Docs](https://router.vuejs.org/guide/essentials/history-mode.html#example-server-configurations)

[Vue.js Router: history mode and AWS S3 (RoutingRules) - StackOverflow
](https://stackoverflow.com/questions/43095823/vue-js-router-history-mode-and-aws-s3-routingrules)


