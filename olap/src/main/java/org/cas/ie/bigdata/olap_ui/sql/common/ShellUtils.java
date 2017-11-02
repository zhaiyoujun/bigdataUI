package org.cas.ie.bigdata.olap_ui.sql.common;

import java.util.ArrayList;

public class ShellUtils {
	private String host = "192.168.2.11,192.168.2.12,192.168.2.13";
	
	public void setHost(String host) {
		this.host = host;
	}
	
	public String[] getIpSet() {
		String[] ipSet = this.host.split(",");
		return ipSet;
	}
	
	public ArrayList<String> getPingCmdSet(String[] ipSet) {
		ArrayList<String> pingCmdSet = new ArrayList<String>();
		for (int i = 0; i < ipSet.length; i++) {
			pingCmdSet.add("ping" + " " + ipSet[i] + " " + "-n 1");
		}
		return pingCmdSet;
	}
	
}
