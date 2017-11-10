package org.cas.ie.bigdata.olap_ui.sql.common;

public class QueryUtils {
	
	private String showDatabaseSql = "show databases;";
	
	private String showTablesSql = "show tables;";
	
	private String describeTableSqlHead = "describe ";
	
	private String describeTableSqlEnd = " ;";
	
	public void setShowDatabaseSql(String showDatabaseSql) {
		this.showDatabaseSql = showDatabaseSql;
	}
	
	public void setShowTablesSql(String showTablesSql) {
		this.showTablesSql = showTablesSql;
	}
	
	public void setDescribeTableSqlHead(String describeTableSqlHead) {
		this.describeTableSqlHead = describeTableSqlHead;
	}
	
	public void setDescribeTableSqlEnd(String describeTableSqlEnd) {
		this.describeTableSqlEnd = describeTableSqlEnd;
	}
	
	public String getShowDatabaseSql() {
		return this.showDatabaseSql;
	}
	
	public String getShowTablesSql() {
		return this.showTablesSql;
	}
	
	public String getDescribeTableSqlHead() {
		return this.describeTableSqlHead;
	}
	
	public String getDescribeTableSqlEnd() {
		return this.describeTableSqlEnd;
	}

}
