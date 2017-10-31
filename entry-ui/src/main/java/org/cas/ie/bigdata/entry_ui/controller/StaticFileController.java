package org.cas.ie.bigdata.entry_ui.controller;

import javax.servlet.http.HttpServletRequest;  
import javax.servlet.http.HttpServletResponse;

import org.springframework.stereotype.Controller;  
import org.springframework.ui.ModelMap;  
import org.springframework.web.bind.annotation.RequestMapping;  
import org.springframework.web.servlet.ModelAndView;  
import org.springframework.web.bind.annotation.RequestParam;

@Controller  
public class StaticFileController {  
    @RequestMapping(value="/images")  
    public ModelAndView showMessage() {
        return new ModelAndView("image");//÷∏∂® ”Õº
    }
    
} 
