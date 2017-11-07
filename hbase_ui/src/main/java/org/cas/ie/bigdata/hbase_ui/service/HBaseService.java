package org.cas.ie.bigdata.hbase_ui.service;

import java.io.IOException;
import java.util.Collection;
import java.util.HashSet;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.HColumnDescriptor;
import org.apache.hadoop.hbase.HTableDescriptor;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.util.Bytes;
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
	public Collection<HColumnDescriptor> getDescribeTable(String table) throws IOException {
		this.init();
		TableName tableName = TableName.valueOf(table);
		HTableDescriptor hTableDescriptor = admin.getTableDescriptor(tableName);
		
		HColumnDescriptor[] hColumnDescriptors = hTableDescriptor.getColumnFamilies();
		Collection<HColumnDescriptor> hColumnDescriptors2 = hTableDescriptor.getFamilies();
		
		for (int i = 0; i < hColumnDescriptors.length; i++) {
			hColumnDescriptors[i].getValues();
			System.out.println(hColumnDescriptors[i].toString());
		}
		System.out.println();
		
		for (HColumnDescriptor hColumnDescriptor : hColumnDescriptors2) {
			System.out.println(hColumnDescriptor.toString());
			
			Map<ImmutableBytesWritable, ImmutableBytesWritable> map = hColumnDescriptor.getValues();
			for (ImmutableBytesWritable key : map.keySet()) {
				System.out.println(Bytes.toString(key.get()));
				System.out.println(Bytes.toString(map.get(key).get()));
			}
		}
		
		System.out.println("111111111111111111" + hColumnDescriptors.toString());
		System.out.println("222222222222222222" + hColumnDescriptors2);
		
		return hColumnDescriptors2;
	}
	
	public String getDescribeTableJS(Collection<HColumnDescriptor> hColumnDescriptors) {
		JsonObject result = new JsonObject();
		JsonArray rows = new JsonArray();
//		dt.add(new JsonPrimitive(hTableDescriptor.toString()));
//		result.add("dt", dt);
//		return result.toString();
		
		for (HColumnDescriptor hColumnDescriptor : hColumnDescriptors) {
			JsonArray row = new JsonArray();
			
			rows.add(new JsonPrimitive(hColumnDescriptor.getNameAsString()));
			
			Map<ImmutableBytesWritable, ImmutableBytesWritable> map = hColumnDescriptor.getValues();
			
			for (ImmutableBytesWritable key : map.keySet()) {
				JsonArray ja = new JsonArray();
				ja.add(new JsonPrimitive(Bytes.toString(key.get())));
				ja.add(new JsonPrimitive(Bytes.toString(map.get(key).get())));	
				row.add(ja);
			}
			rows.add(row);			
		}
		result.add("rows", rows);
		return result.toString();
	}	
}
