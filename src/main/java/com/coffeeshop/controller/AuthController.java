package com.coffeeshop.controller;

import com.coffeeshop.model.User;
import com.coffeeshop.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpSession;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private UserRepository userRepository;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest loginRequest, HttpSession session) {
        try {
            // Authenticate user
            Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(
                    loginRequest.getUsername(), 
                    loginRequest.getPassword()
                )
            );

            // Set authentication in security context
            SecurityContextHolder.getContext().setAuthentication(authentication);

            // Get user details
            Optional<User> userOpt = userRepository.findByUsername(loginRequest.getUsername());
            if (userOpt.isPresent()) {
                User user = userOpt.get();
                
                // Store user info in session
                session.setAttribute("userId", user.getId());
                session.setAttribute("username", user.getUsername());
                session.setAttribute("userRole", user.getRole().name());

                // Prepare response
                Map<String, Object> response = new HashMap<>();
                response.put("success", true);
                response.put("role", user.getRole().name());
                response.put("username", user.getUsername());
                response.put("message", "Login successful");

                return ResponseEntity.ok(response);
            }

            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(Map.of("success", false, "message", "User not found"));

        } catch (BadCredentialsException e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body(Map.of("success", false, "message", "Invalid username or password"));
        }
    }

    @PostMapping("/logout")
    public ResponseEntity<?> logout(HttpSession session) {
        session.invalidate();
        SecurityContextHolder.clearContext();
        return ResponseEntity.ok(Map.of("success", true, "message", "Logged out successfully"));
    }

    @GetMapping("/user")
    public ResponseEntity<?> getCurrentUser(HttpSession session) {
        String username = (String) session.getAttribute("username");
        String role = (String) session.getAttribute("userRole");
        
        if (username != null && role != null) {
            Map<String, Object> response = new HashMap<>();
            response.put("username", username);
            response.put("role", role);
            response.put("authenticated", true);
            return ResponseEntity.ok(response);
        }
        
        return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
            .body(Map.of("authenticated", false, "message", "Not authenticated"));
    }

    // DTO classes
    public static class LoginRequest {
        private String username;
        private String password;

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String password) {
            this.password = password;
        }
    }
}
