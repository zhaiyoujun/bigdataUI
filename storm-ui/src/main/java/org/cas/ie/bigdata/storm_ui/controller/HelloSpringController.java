package org.cas.ie.bigdata.storm_ui.controller;

import org.cas.ie.bigdata.storm_ui.Utils.IpUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;


@Controller
public class HelloSpringController {
	
	@Autowired
	IpUtil ipUtil;	

    @RequestMapping("/")
    public ModelAndView showCluster() {
//    	String string = "http://192.168.2.58:8089";
//    	JsonObject jsonObject = new JsonObject();
//    	JsonArray jsonArray = new JsonArray();
//    	jsonArray.add(new JsonPrimitive(string));
//    	jsonObject.add("ip", jsonArray);
        ModelAndView mv = new ModelAndView("index");//指定视图
//向视图中添加所要展示或使用的内容，将在页面中使用
        mv.addObject("ip", "http://192.168.2.58:8089");
        return mv;
    }
    @RequestMapping("/topology")
    public ModelAndView showTopology() {
        ModelAndView mv = new ModelAndView("topology");//指定视图
//向视图中添加所要展示或使用的内容，将在页面中使用
        return mv;
    }
    
    @RequestMapping("/getStorm_Host_Ip")
    public String getStorm_Hosp_Ip() {
    	return ipUtil.getStorm_Host_Ip();
    }
	
}

