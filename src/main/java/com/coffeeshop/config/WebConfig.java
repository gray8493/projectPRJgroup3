package com.coffeeshop.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.ViewControllerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    
    @Override
    public void addViewControllers(ViewControllerRegistry registry) {
        // Redirect root to login page
        registry.addViewController("/").setViewName("forward:/login.html");
        
        // Add explicit mappings for static pages
        registry.addViewController("/login").setViewName("forward:/login.html");
        registry.addViewController("/admin").setViewName("forward:/index.html");
        registry.addViewController("/menu").setViewName("forward:/menu.html");
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/**")
                .addResourceLocations("classpath:/static/");
    }
}