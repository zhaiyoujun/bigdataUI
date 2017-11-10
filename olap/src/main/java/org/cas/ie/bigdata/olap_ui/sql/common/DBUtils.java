package org.cas.ie.bigdata.olap_ui.sql.common;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DBUtils {

	private String driver = "com.mysql.jdbc.Driver";
	private String dbconnect = "jdbc:mysql://127.0.0.1:3306";
	private String username = "root";
	private String password = "root";
	private String database = "test";
	
	public void setDriver(String driver) {
		this.driver = driver;
	}
	
	public void setDbconnect(String dbconnect) {
		this.dbconnect = dbconnect;
	}
	
	public void setUsername(String username) {
		this.username = username;
	}
	
	public void setPassword(String password) {
		this.password = password;
	}
	
	public void setDatabase(String database) {
		this.database = database;
	}
	
	public Connection connect(String database) throws IOException, ClassNotFoundException, SQLException {
		Class.forName(this.driver);
	    String dbconn = this.dbconnect;
	    if (database != null) {
	    	dbconn = dbconn + '/' + database;
	    }else {
	    	dbconn = dbconn + '/' + this.database;
	    }
	    return DriverManager.getConnection(
	      dbconn,
	      this.username,
	      this.password
	    );
	}
}
