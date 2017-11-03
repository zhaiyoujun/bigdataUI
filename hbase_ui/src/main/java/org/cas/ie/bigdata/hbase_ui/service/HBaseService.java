package org.cas.ie.bigdata.hbase_ui.service;

import java.io.IOException;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.springframework.stereotype.Service;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

@Service
public class HBaseService {
	
	public String[][] getListTables(Admin admin) throws IOException {
		TableName[] tables = admin.listTableNames();
		String[][] listTables = new String[tables.length][2];
        for (int i = 0; i < tables.length; i++) {
        	listTables[i][0] = tables[i].getNamespaceAsString();
        	listTables[i][1] = tables[i].getNameAsString();
        }
        return listTables;
	}	
	
	public String getListTablesJS(String[][] listTables) {
		int tableCount = listTables.length;
		
		JsonObject result = new JsonObject();
		JsonArray tables = new JsonArray();
		
		for (int i = 0; i < tableCount; i++) {
			JsonArray table = new JsonArray();
			for (int j = 0; j < listTables[i].length; j++) {
				table.add(new JsonPrimitive(listTables[i][j]));
			}
			tables.add(table);
		}
		result.add("tables", tables);
		return result.toString();
	}
	
	public HashSet<String> getListNamespace(String[][] listTables) {
		HashSet<String> namespace = new HashSet<String>();
		for (int i = 0; i < listTables.length; i++) {
			if (!namespace.contains(listTables[i][0])) {
				namespace.add(listTables[i][0]);
			}
		}
		return namespace;
	}
	
	public String getListNamespaceJS(HashSet<String> namespace) {
		int namespaceCount = namespace.size();
		
		JsonObject result = new JsonObject();
		JsonArray namespaces = new JsonArray();
		
		for (String string : namespace) {
			namespaces.add(new JsonPrimitive(string));
		}
		result.add("namespaces", namespaces);
		return result.toString();
	}
	
	public String[] getTablesByNamespace(Admin admin, String namespace) throws IOException {
		TableName[] tables = admin.listTableNamesByNamespace(namespace);
		String[] tablesBySpace = new String[tables.length];
		for (int i = 0; i < tables.length; i++) {
			tablesBySpace[i] = tables[i].getNameAsString();
		}
		return tablesBySpace;
	}
	
	public String getTablesByNamespaceJS(String[] tablesByNamepace) {
		int tableCount = tablesByNamepace.length;
		
		JsonObject result = new JsonObject();
		JsonArray tablesByNamespace = new JsonArray();
		
		for (int i = 0; i < tableCount; i++) {
			tablesByNamespace.add(new JsonPrimitive(tablesByNamepace[i]));
		}
		result.add("tablesByNamespace", tablesByNamespace);
		return result.toString();
	}
		
}
