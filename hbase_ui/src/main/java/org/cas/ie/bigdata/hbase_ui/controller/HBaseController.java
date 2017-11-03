package org.cas.ie.bigdata.hbase_ui.controller;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.cas.ie.bigdata.hbase_ui.service.HBaseService;
import org.cas.ie.bigdata.hbase_ui.service.ShellService;
import org.cas.ie.bigdata.hbase_ui.bean.ShellUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class HBaseController {
	
	@Autowired
	HBaseService hBaseService;
	
	@Autowired
	ShellService shellService;
	
	@Autowired
	ShellUtils shellUtils;
	
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
	
	@RequestMapping("/listtables")
	public ModelAndView listTables() throws IOException {
		
		Configuration conf = new Configuration();
        conf.addResource("hbase-site.xml");
        conf = HBaseConfiguration.create(conf);
		
		Connection connection = ConnectionFactory.createConnection(conf);
		Admin admin = connection.getAdmin();
		String[][] listTables = hBaseService.getListTables(admin);
		String ts = hBaseService.getListTablesJS(listTables);
		
        connection.close();

		ModelAndView mv = new ModelAndView("listTables");
		mv.addObject("ts", ts);
		return mv;				
	}
	
	@RequestMapping("/listnamespaces")
	public ModelAndView listNamespaces() throws IOException {
		
		Configuration conf = new Configuration();
        conf.addResource("hbase-site.xml");
        conf = HBaseConfiguration.create(conf);
		
		Connection connection = ConnectionFactory.createConnection(conf);
		Admin admin = connection.getAdmin();
		
		String[][] listTables = hBaseService.getListTables(admin);
		HashSet<String> listNamespace = hBaseService.getListNamespace(listTables);
		String ns = hBaseService.getListNamespaceJS(listNamespace);
		
        connection.close();

		ModelAndView mv = new ModelAndView("listNamespaces");
		mv.addObject("ns", ns);
		return mv;				
	}
	
	@RequestMapping("/listtablesbynamespace")
	public ModelAndView listTablesByNamespace(@RequestParam(value = "namespace", required = true)String namespace) throws IOException {
		
		Configuration conf = new Configuration();
        conf.addResource("hbase-site.xml");
        conf = HBaseConfiguration.create(conf);
        
		Connection connection = ConnectionFactory.createConnection(conf);
		Admin admin = connection.getAdmin();
		String[] tablesByNamespace = hBaseService.getTablesByNamespace(admin, namespace);
		String tn = hBaseService.getTablesByNamespaceJS(tablesByNamespace);
		
        connection.close();

		ModelAndView mv = new ModelAndView("listTablesByNamespace");
		mv.addObject("tn", tn);
		return mv;				
	}
	
}
