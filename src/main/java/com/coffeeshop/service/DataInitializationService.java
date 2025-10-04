package com.coffeeshop.service;

import com.coffeeshop.model.User;
import com.coffeeshop.model.Coffee;
import com.coffeeshop.repository.UserRepository;
import com.coffeeshop.repository.CoffeeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class DataInitializationService implements CommandLineRunner {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private CoffeeRepository coffeeRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        initializeUsers();
        initializeCoffeeMenu();
    }

    private void initializeUsers() {
        // Create admin user if not exists
        if (!userRepository.existsByUsername("admin")) {
            User admin = new User();
            admin.setUsername("admin");
            admin.setPassword(passwordEncoder.encode("admin123"));
            admin.setRole(User.Role.ADMIN);
            admin.setEnabled(true);
            userRepository.save(admin);
            System.out.println("Default admin user created: admin/admin123");
        }

        // Create staff user if not exists
        if (!userRepository.existsByUsername("staff")) {
            User staff = new User();
            staff.setUsername("staff");
            staff.setPassword(passwordEncoder.encode("staff123"));
            staff.setRole(User.Role.STAFF);
            staff.setEnabled(true);
            userRepository.save(staff);
            System.out.println("Default staff user created: staff/staff123");
        }
    }

    private void initializeCoffeeMenu() {
        // Check if menu items already exist
        if (coffeeRepository.count() > 0) {
            System.out.println("Coffee menu already initialized with " + coffeeRepository.count() + " items");
            return;
        }

        // Create sample coffee menu items
        Coffee[] coffeeItems = {
            createCoffee("Espresso", "Rich and bold espresso shot", 2.50, "Coffee"),
            createCoffee("Cappuccino", "Espresso with steamed milk and foam", 4.00, "Coffee"),
            createCoffee("Latte", "Espresso with steamed milk", 4.50, "Coffee"),
            createCoffee("Americano", "Espresso with hot water", 3.00, "Coffee"),
            createCoffee("Mocha", "Chocolate flavored coffee drink", 5.00, "Coffee"),
            createCoffee("Macchiato", "Espresso with a dollop of steamed milk", 4.25, "Coffee"),
            createCoffee("Flat White", "Double espresso with steamed milk", 4.75, "Coffee"),
            createCoffee("Cold Brew", "Smooth cold coffee concentrate", 3.50, "Cold Coffee"),
            createCoffee("Iced Latte", "Chilled espresso with cold milk", 4.50, "Cold Coffee"),
            createCoffee("Frappuccino", "Blended coffee drink with ice", 5.50, "Cold Coffee"),
            createCoffee("Green Tea Latte", "Matcha green tea with steamed milk", 4.25, "Tea"),
            createCoffee("Chai Latte", "Spiced tea with steamed milk", 4.00, "Tea")
        };

        for (Coffee coffee : coffeeItems) {
            coffeeRepository.save(coffee);
        }

        System.out.println("Coffee menu initialized with " + coffeeItems.length + " items");
    }

    private Coffee createCoffee(String name, String description, double price, String category) {
        Coffee coffee = new Coffee();
        coffee.setName(name);
        coffee.setDescription(description);
        coffee.setPrice(price);
        coffee.setCategory(category);
        coffee.setAvailable(true);
        return coffee;
    }
}
