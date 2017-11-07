package org.cas.ie.bigdata.olap_ui.sql.common;

import java.util.ArrayList;

public class ShellUtils {
	private String host = "node1#192.168.2.11,node2#192.168.2.12,node3#192.168.2.13";
	
	public void setHost(String host) {
		this.host = host;
	}
	
	public ArrayList<String[]> splitHost() {
		String[] hostSet = this.host.split(",");
		
		int hostCount = hostSet.length;
		
		String[] nodeSet = new String[hostCount];
		String[] ipSet = new String[hostCount];
		
		for (int i = 0 ; i < hostCount; i++) {
			String[] node = hostSet[i].split("#");
			nodeSet[i] = node[0];
			ipSet[i] = node[1];
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
			pingCmdSet.add("ping" + " " + ipSet[i] + " " + "-n 1 -w 100");
		}
		return pingCmdSet;
	}	
}
