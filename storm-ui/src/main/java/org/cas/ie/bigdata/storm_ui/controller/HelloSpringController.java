package org.cas.ie.bigdata.storm_ui.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;


@Controller
public class HelloSpringController {
    @RequestMapping("/")
    public ModelAndView showCluster() {
        ModelAndView mv = new ModelAndView("index");//指定视图
//向视图中添加所要展示或使用的内容，将在页面中使用
        return mv;
    }
    @RequestMapping("/topology")
    public ModelAndView showTopology() {
        ModelAndView mv = new ModelAndView("topology");//指定视图
//向视图中添加所要展示或使用的内容，将在页面中使用
        return mv;
    }
	
}

