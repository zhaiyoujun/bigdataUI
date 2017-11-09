package org.cas.ie.bigdata.hbase_ui.bean;

import java.util.ArrayList;

public class ShellUtils {
	private String host = "node0#192.168.2.57,node1#192.168.2.58";
	
	private String cmdParam = "-n 1 -w 100";
	
	public void setHost(String host) {
		this.host = host;
	}
	
	public void setCmdParam(String cmdParam) {
		this.cmdParam = cmdParam;
	}
	
	public ArrayList<String[]> splitHost() {
		String[] hostSet = this.host.split(",");
		
		int hostCount = hostSet.length;
		
		String[] nodeSet = new String[hostCount];
		String[] ipSet = new String[hostCount];
		
		for (int i = 0 ; i < hostCount; i++) {
			String[] node = hostSet[i].split("#");
			nodeSet[i] = node[0];
			if (node.length > 1) {				
				ipSet[i] = node[1];
			}			
		}
		ArrayList<String[]> splitResult = new ArrayList<String[]>();
		splitResult.add(0, nodeSet);
		splitResult.add(1, ipSet);
		return splitResult;
	}
	
	public String[] getNodeSet(ArrayList<String[]> splitResult) {
		return splitResult.get(0);
	}
	
	public String[] getIpSet(ArrayList<String[]> splitResult) {
		return splitResult.get(1);
	}
	
	public ArrayList<String> getPingCmdSet(String[] ipSet) {
		ArrayList<String> pingCmdSet = new ArrayList<String>();
		for (int i = 0; i < ipSet.length; i++) {
			pingCmdSet.add("ping" + " " + ipSet[i] + " " + this.cmdParam);
		}
		return pingCmdSet;
	}
}
