package org.cas.ie.bigdata.hbase_ui.controller;

import java.io.IOException;
import java.sql.SQLException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.cas.ie.bigdata.hbase_ui.service.HBaseService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class HBaseController {
	
	@Autowired
	HBaseService hBaseService;
	
	@RequestMapping("/listtables")
	public ModelAndView listTables() throws IOException {
		Configuration conf = HBaseConfiguration.create();
		
		conf.set("hbase.zookeeper.quorum", "192.168.2.58");
		conf.set("hbase.zookeeper.property.clientPort", "2181");
		
		Connection connection = ConnectionFactory.createConnection(conf);
		String[][] listTables = hBaseService.ListTables(connection);
		ModelAndView mv = new ModelAndView("listTables");
		mv.addObject("listTables", listTables);
		return mv;				
	}
	@RequestMapping("/showdatabases")
    public ModelAndView shwoDatabases() {
    	ModelAndView mv = new ModelAndView("showDatabases");//指定视图
    	//向视图中添加所要展示或使用的内容，将在页面中使用
        return mv;        
    }
    
    @RequestMapping("/showtables")
    public ModelAndView shwoTables() {
    	ModelAndView mv = new ModelAndView("showTables");//指定视图
    	//向视图中添加所要展示或使用的内容，将在页面中使用
        return mv;        
    }
	
}
