package org.cas.ie.bigdata.hbase_ui.controller;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;

import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
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
	
	@RequestMapping("/listnamespaces")
	public ModelAndView listNamespaces() throws IOException {
		
		String[][] listTables = hBaseService.getListTables();
		HashSet<String> listNamespace = hBaseService.getListNamespace(listTables);
		String ns = hBaseService.getListNamespaceJS(listNamespace);
		
		ModelAndView mv = new ModelAndView("listNamespaces");
		mv.addObject("ns", ns);
		return mv;				
	}
		
	@RequestMapping("/listtablesbynamespace")
	public ModelAndView listTablesByNamespace(@RequestParam(value = "namespace", required = true)String namespace) throws IOException {
		
		TableName[] tables = hBaseService.getTablesByNamespace(namespace);
		String[] tablesByNamespace = hBaseService.getTablesByNamespaceString(tables);
		String tn = hBaseService.getTablesByNamespaceJS(tablesByNamespace);
		
		ModelAndView mv = new ModelAndView("listTablesByNamespace");
		mv.addObject("tn", tn);
		return mv;				
	}
	
	@RequestMapping("/describetable")
	public ModelAndView describeTable(@RequestParam(value = "table", required = true)String table) throws IOException {
		
//		HTableDescriptor hTableDescriptor = hBaseService.getDescribeTable(table);
//		String dt = hBaseService.getDescribeTableJS(hTableDescriptor);
		
		Collection<HColumnDescriptor> hColumnDescriptors = hBaseService.getDescribeTable(table);
		String dt = hBaseService.getDescribeTableJS(hColumnDescriptors);
		
		ModelAndView mv = new ModelAndView("describeTable");
		mv.addObject("dt", dt);
		return mv;				
	}	
}
