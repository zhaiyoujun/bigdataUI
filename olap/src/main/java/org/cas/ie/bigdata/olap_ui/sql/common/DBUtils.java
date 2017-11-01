package org.cas.ie.bigdata.olap_ui.sql.common;

import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

import org.cas.ie.bigdata.olap_ui.sql.common.PropertyUtils;

public class DBUtils {

	  public static Connection connect(Properties p) throws IOException, ClassNotFoundException, SQLException {
	    Class.forName(p.getProperty("driver"));
	    return DriverManager.getConnection(
	      p.getProperty("dbconnect"),
	      p.getProperty("username"),
	      p.getProperty("password")
	    );
	  }

	  public static Connection connect() throws IOException, ClassNotFoundException, SQLException {
//	    return connect(PropertyUtils.get("db"));
		Properties p= new Properties();
		p.setProperty("driver", "com.mysql.jdbc.Driver");
		p.setProperty("dbconnect", "jdbc:mysql://127.0.0.1:3306");
		p.setProperty("username", "root");
		p.setProperty("password", "root");
		  
	    return connect(p);	    
	  }
	  
	  public static Connection connect(String database) throws IOException, ClassNotFoundException, SQLException {
//		    return connect(PropertyUtils.get("db"));
			Properties p= new Properties();
			p.setProperty("driver", "com.mysql.jdbc.Driver");
			p.setProperty("dbconnect", "jdbc:mysql://127.0.0.1:3306" + "/" + database);
			p.setProperty("username", "root");
			p.setProperty("password", "root");
			  
		    return connect(p);		    
		  }
	}