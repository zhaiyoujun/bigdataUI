package org.cas.ie.bigdata.olap_ui.service;

import java.io.IOException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import org.cas.ie.bigdata.olap_ui.sql.common.DBUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonPrimitive;

@Service
public class QueryService {
	
	@Autowired
	DBUtils dbUtils;
	
	private Connection connection = null;
	
	private void init(String database) throws ClassNotFoundException, IOException, SQLException {
		this.connection = dbUtils.connect(database);
	}
    
    public String query(String sql,String database) throws SQLException, IOException, ClassNotFoundException {
    	this.init(database);
    	
      JsonObject result = new JsonObject();
      
      Statement stmt = connection.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE, ResultSet.CONCUR_READ_ONLY);
      
      ResultSet rs = stmt.executeQuery(sql);
      
      JsonArray columnNames = new JsonArray();
      for (int i = 1; i <= rs.getMetaData().getColumnCount(); ++i) {
        columnNames.add(new JsonPrimitive(rs.getMetaData().getColumnName(i)));
      }
      result.add("columns", columnNames);

      JsonArray rows = new JsonArray();
      for (int rid = 0; rs.next(); ++rid) {
        JsonArray row = new JsonArray();
        for (int i = 1; i <= rs.getMetaData().getColumnCount(); ++i) {
          row.add(new JsonPrimitive(String.valueOf(rs.getObject(i))));
        }
        rows.add(row);
      }

      result.add("rows", rows);

      stmt.close();

      return (result.toString());
    }
}
