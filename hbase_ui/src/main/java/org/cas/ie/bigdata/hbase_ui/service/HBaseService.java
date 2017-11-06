package org.cas.ie.bigdata.hbase_ui.service;

import java.io.IOException;
import java.util.HashSet;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.springframework.stereotype.Service;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

@Service
public class HBaseService {
	
	private Connection connection = null;
	private Admin admin = null;
	//初始化连接
	private void init() throws IOException {
		if (this.connection != null)
			return;
		
		Configuration conf = new Configuration();
        conf.addResource("hbase-site.xml");
        conf = HBaseConfiguration.create(conf);
		
		this.connection = ConnectionFactory.createConnection(conf);
		this.admin = this.connection.getAdmin();
	}
	//不分库查表
	public String[][] getListTables() throws IOException {
		this.init();
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
	//查库
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
		
		JsonObject result = new JsonObject();
		JsonArray namespaces = new JsonArray();
		
		for (String string : namespace) {
			namespaces.add(new JsonPrimitive(string));
		}
		result.add("namespaces", namespaces);
		return result.toString();
	}
	
	//分库查表
	public TableName[] getTablesByNamespace(String namespace) throws IOException {
		this.init();
		TableName[] tables = admin.listTableNamesByNamespace(namespace);
		
		return tables;
	}	
	
	public String[] getTablesByNamespaceString(TableName[] tables) throws IOException {
		
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
	//查看表结构
	public HTableDescriptor getDescribeTable(String table) throws IOException {
		this.init();
		TableName tableName = TableName.valueOf(table);
		return admin.getTableDescriptor(tableName);
	}
	
	public String getDescribeTableJS(HTableDescriptor hTableDescriptor) {
		JsonObject result = new JsonObject();
		JsonArray dt = new JsonArray();
		dt.add(new JsonPrimitive(hTableDescriptor.toString()));
		result.add("dt", dt);
		return result.toString();
	}	
}
