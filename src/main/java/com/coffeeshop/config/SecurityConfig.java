package com.coffeeshop.config;

import com.coffeeshop.service.CustomUserDetailsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.authentication.configuration.AuthenticationConfiguration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.security.web.authentication.AuthenticationFailureHandler;

@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true)
public class SecurityConfig {

    @Autowired
    private CustomUserDetailsService userDetailsService;

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public DaoAuthenticationProvider authenticationProvider() {
        DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
        authProvider.setUserDetailsService(userDetailsService);
        authProvider.setPasswordEncoder(passwordEncoder());
        return authProvider;
    }

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf().disable()
            .authorizeRequests()
                // Public endpoints
                .antMatchers("/", "/login.html", "/api/auth/login", "/api/auth/logout", "/api/auth/user").permitAll()
                .antMatchers("/css/**", "/js/**", "/images/**", "/favicon.ico").permitAll()
                
                // Admin-only endpoints
                .antMatchers("/index.html").hasRole("ADMIN")
                
                // Staff and Admin can access menu and coffee API
                .antMatchers("/menu.html", "/api/coffees").hasAnyRole("ADMIN", "STAFF")
                
                // Only Admin can create/update/delete coffees
                .antMatchers("/api/coffees/**").hasRole("ADMIN")
                
                // All other requests need authentication
                .anyRequest().authenticated()
            .and()
            .formLogin()
                .loginPage("/login.html")
                .permitAll()
                .successHandler(authenticationSuccessHandler())
                .failureHandler(authenticationFailureHandler())
            .and()
            .logout()
                .logoutUrl("/api/auth/logout")
                .logoutSuccessUrl("/login.html")
                .invalidateHttpSession(true)
                .deleteCookies("JSESSIONID")
                .permitAll()
            .and()
            .sessionManagement()
                .maximumSessions(1)
                .maxSessionsPreventsLogin(false);
        
        return http.build();
    }

    @Bean
    public AuthenticationSuccessHandler authenticationSuccessHandler() {
        return (request, response, authentication) -> {
            String role = authentication.getAuthorities().iterator().next().getAuthority();
            if ("ROLE_ADMIN".equals(role)) {
                response.sendRedirect("/index.html");
            } else if ("ROLE_STAFF".equals(role)) {
                response.sendRedirect("/menu.html");
            } else {
                response.sendRedirect("/login.html");
            }
        };
    }

    @Bean
    public AuthenticationFailureHandler authenticationFailureHandler() {
        return (request, response, exception) -> {
            response.sendRedirect("/login.html?error=true");
        };
    }
}
