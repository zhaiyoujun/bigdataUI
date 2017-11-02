package org.cas.ie.bigdata.hbase_ui.service;

import java.io.IOException;

import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.Connection;
import org.springframework.stereotype.Service;

@Service
public class HBaseService {
	
	public String[][] ListTables(Connection connection) throws IOException {
		Admin admin = connection.getAdmin();
		TableName[] tables = admin.listTableNames();
		
		String[][] listTables = new String[tables.length][2];
        for (int i = 0; i < tables.length; i++) {
        	listTables[i][0] = tables[i].getNamespaceAsString();
        	listTables[i][1] = tables[i].getNameAsString();
        }
        return listTables;
	}
		
}
