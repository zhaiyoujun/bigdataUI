package org.cas.ie.bigdata.storm_ui.controller;

import org.cas.ie.bigdata.storm_ui.Utils.IpUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class HelloSpringController {
	
	@Autowired
	IpUtil ipUtil;	

    @RequestMapping("/")
    public ModelAndView showCluster() {
        ModelAndView mv = new ModelAndView("index", "ip", ipUtil.getStorm_Host_Ip());//指定视图
//向视图中添加所要展示或使用的内容，将在页面中使用
        return mv;
    }
    @RequestMapping("/topology")
    public ModelAndView showTopology() {
        ModelAndView mv = new ModelAndView("topology", "ip", ipUtil.getStorm_Host_Ip());//指定视图
//向视图中添加所要展示或使用的内容，将在页面中使用
        return mv;
    }
    @RequestMapping("/topologydetails")
    public ModelAndView showTopologyDetails(
    		@RequestParam(value = "id",required = true)String id,
    		@RequestParam(value = "sys", required = true)String sys) {
    	
        ModelAndView mv = new ModelAndView("topologyDetails", "ip", ipUtil.getStorm_Host_Ip());//指定视图
//向视图中添加所要展示或使用的内容，将在页面中使用
        return mv;
    }
}

