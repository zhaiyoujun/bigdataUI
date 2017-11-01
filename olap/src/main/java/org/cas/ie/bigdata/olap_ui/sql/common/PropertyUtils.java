package org.cas.ie.bigdata.olap_ui.sql.common;

import java.io.IOException;
import java.util.Properties;

public class PropertyUtils {

	  public static Properties get(String name) throws IOException {
	    if (!name.endsWith(".properties"))
	      name = name + ".properties";
	    Properties p = new Properties();
	    p.load(ClassLoader.getSystemResourceAsStream("/src/main/resources" + name));
	    return p;
	  }

	}