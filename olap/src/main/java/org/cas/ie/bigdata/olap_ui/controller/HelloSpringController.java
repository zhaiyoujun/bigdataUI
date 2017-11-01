package org.cas.ie.bigdata.olap_ui.controller;

import java.io.IOException;
import java.sql.SQLException;

import org.cas.ie.bigdata.olap_ui.service.QueryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class HelloSpringController {
	
	@Autowired
    QueryService queryService;
	
    String message = "Welcome to Spring MVC!";
 
    @RequestMapping("/hello")
    public ModelAndView showMessage(@RequestParam(value = "name", required = false, defaultValue = "Spring") String name) {
    	 
        ModelAndView mv = new ModelAndView("hellospring");//指定视图
        //向视图中添加所要展示或使用的内容，将在页面中使用
        mv.addObject("message", message);
        mv.addObject("name", name);
        return mv;
    }
    
    @RequestMapping("/showtables")
    public ModelAndView shwoTables(@RequestParam(value = "database", required = true) String name) throws ClassNotFoundException, SQLException, IOException {
     
//    	System.out.println("返回成功");
    	String sql = "show tables;";
    	String query = queryService.query(sql);
//    	System.out.println("返回成功"+query);
    	ModelAndView mv = new ModelAndView("showTables");//指定视图
    	//向视图中添加所要展示或使用的内容，将在页面中使用
    	mv.addObject("sql", sql);
        mv.addObject("rs", query);
    
        return mv;        
    }
}
