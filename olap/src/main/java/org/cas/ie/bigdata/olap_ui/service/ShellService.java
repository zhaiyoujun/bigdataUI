package org.cas.ie.bigdata.olap_ui.service;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import org.springframework.stereotype.Service;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

@Service
public class ShellService {
	public String[][] getClusterStatus(String[] ipSet, ArrayList<String> pingCmdSet) throws IOException, InterruptedException {
		Process process;
		int ipCount = ipSet.length;
		String[][] clusterStatus = new String[ipCount][2];
		
		for (int i = 0; i < ipCount; i++) {
			clusterStatus[i][0] = ipSet[i];			
			process = Runtime.getRuntime().exec(pingCmdSet.get(i));			
			int status = process.waitFor();
			
			if (status == 0) {
				clusterStatus[i][1] = "Living";
			}else {
				clusterStatus[i][1] = "Die";
			}			
		}
		return clusterStatus;
	}
	
	public String getClusterStatusJS(String[][] clusterStatus) throws IOException, InterruptedException {
		int ipCount = clusterStatus.length;
	    JsonObject result = new JsonObject();
	    
	    JsonArray rows = new JsonArray();
	    for (int i = 0; i < ipCount; i++) {
	    	JsonArray row = new JsonArray();
	    	for (int j = 0; j < 2; j++) {
	    		row.add(new JsonPrimitive(clusterStatus[i][j]));
	    	}
	    	rows.add(row);
	    }
	    
	    result.add("rows", rows);

		return result.toString();
	}
	
	public HashMap<String, Integer> getStatisticsResult(String[][] clusterStatus) {
		HashMap<String, Integer> statisticsResult = new HashMap<String, Integer>();
		statisticsResult.put("Die", 0);
		statisticsResult.put("Living", 0);
		
		for (int i = 0; i < clusterStatus.length; i++) {
			if (clusterStatus[i][1].equals("Living")) {
				statisticsResult.put("Living", statisticsResult.get("Living") + 1);
			}else {
				statisticsResult.put("Die", statisticsResult.get("Die") + 1);
			}
		}
		return statisticsResult;
	}
}
