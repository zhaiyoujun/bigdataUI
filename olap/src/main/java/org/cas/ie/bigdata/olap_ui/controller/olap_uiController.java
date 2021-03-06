package org.cas.ie.bigdata.olap_ui.controller;

import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;

import org.cas.ie.bigdata.olap_ui.service.QueryService;
import org.cas.ie.bigdata.olap_ui.service.ShellService;
import org.cas.ie.bigdata.olap_ui.sql.common.DBUtils;
import org.cas.ie.bigdata.olap_ui.sql.common.QueryUtils;
import org.cas.ie.bigdata.olap_ui.sql.common.ShellUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

@Controller
public class olap_uiController {
	
	@Autowired
	ShellService shellService;
	
	@Autowired
	ShellUtils shellUtils;
	
	@Autowired
    QueryService queryService;
	
	@Autowired
	DBUtils dbUtils;
	
	@Autowired
	QueryUtils queryUtils;
	
	@RequestMapping("/")
	public ModelAndView showCluster() throws IOException, InterruptedException {
		
		ArrayList<String[]> splitResult = shellUtils.splitHost();
		
		String[] nodeSet = shellUtils.getNodeSet(splitResult);
		String[] ipSet = shellUtils.getIpSet(splitResult);
		
		ArrayList<String> pingCmdSet = shellUtils.getPingCmdSet(ipSet);
		
		String[][] clusterStatus = shellService.getClusterStatus(nodeSet, ipSet, pingCmdSet);
		
		HashMap<String, Integer> statisticsResult = shellService.getStatisticsResult(clusterStatus);
		
		String cs = shellService.getClusterStatusJS(clusterStatus);
		
		ModelAndView mv = new ModelAndView("index");
		mv.addObject("dieCount", statisticsResult.get("Die"));
		mv.addObject("livingCount", statisticsResult.get("Living"));		
		mv.addObject("cs", cs);
		
		return mv;
	}
	
    @RequestMapping("/showdatabases")
    public ModelAndView showDatabases() throws ClassNotFoundException, SQLException, IOException {
     
    	String sql = queryUtils.getShowDatabaseSql();   
    	
    	String rs = queryService.query(sql, null);
    	
    	ModelAndView mv = new ModelAndView("showDatabases");//指定视图
    	//向视图中添加所要展示或使用的内容，将在页面中使用
        mv.addObject("rs", rs);
        return mv;        
    }
    
    @RequestMapping("/showtables")
    public ModelAndView showTables(@RequestParam(value = "database", required = true) String name) throws ClassNotFoundException, SQLException, IOException {
     
    	String sql = queryUtils.getShowTablesSql();
    
    	String rs = queryService.query(sql, name);
    	
    	JsonObject db = new JsonObject();
    	db.add("name", new JsonPrimitive(name));
    	
    	ModelAndView mv = new ModelAndView("showTables");//指定视图
    	//向视图中添加所要展示或使用的内容，将在页面中使用
        mv.addObject("rs", rs);
        mv.addObject("db",db);		
        return mv;
    }
    
    @RequestMapping("/describetable")
    public ModelAndView describeTable(
    		@RequestParam(value = "database", required = true) String database, 
    		@RequestParam(value = "table", required = true) String table) throws ClassNotFoundException, SQLException, IOException {
     
    	String sql = queryUtils.getDescribeTableSqlHead() + table + queryUtils.getDescribeTableSqlEnd();
    
    	String dt = queryService.query(sql, database);
    	
    	ModelAndView mv = new ModelAndView("describeTable");//指定视图
    	//向视图中添加所要展示或使用的内容，将在页面中使用
        mv.addObject("dt", dt);
        return mv;
    }
}
