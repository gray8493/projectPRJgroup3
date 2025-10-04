package com.coffeeshop.controller;

import org.springframework.security.access.prepost.PreAuthorize;

import com.coffeeshop.model.Coffee;
import com.coffeeshop.repository.CoffeeRepository;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.util.List;
import java.time.LocalDateTime;

@RestController
@RequestMapping("/api/coffees")
@CrossOrigin // nếu frontend khác origin/port
public class CoffeeController {

    private final CoffeeRepository coffeeRepository;

    public CoffeeController(CoffeeRepository coffeeRepository) {
        this.coffeeRepository = coffeeRepository;
    }

    @GetMapping
    @PreAuthorize("hasRole('ADMIN') or hasRole('STAFF')")
    public List<Coffee> getAllCoffees() {
        // Nếu muốn chỉ lấy item đang active:
        // return coffeeRepository.findByAvailableTrueOrderByIdDesc();
        return coffeeRepository.findAll();
    }

    @GetMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN') or hasRole('STAFF')")
    public Coffee getCoffeeById(@PathVariable Long id) {
        return coffeeRepository.findById(id).orElse(null);
    }

    @PostMapping
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Coffee> createCoffee(@RequestBody Coffee coffee) {
        try {
            coffee.setCreatedAt(LocalDateTime.now());
            coffee.setUpdatedAt(LocalDateTime.now());
            Coffee savedCoffee = coffeeRepository.save(coffee);
            return ResponseEntity.ok(savedCoffee);
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Coffee> updateCoffee(@PathVariable Long id, @RequestBody Coffee coffee) {
        try {
            return coffeeRepository.findById(id)
                .map(existingCoffee -> {
                    existingCoffee.setName(coffee.getName());
                    existingCoffee.setDescription(coffee.getDescription());
                    existingCoffee.setPrice(coffee.getPrice());
                    existingCoffee.setCategory(coffee.getCategory());
                    existingCoffee.setAvailable(coffee.isAvailable());
                    existingCoffee.setUpdatedAt(LocalDateTime.now());
                    Coffee updatedCoffee = coffeeRepository.save(existingCoffee);
                    return ResponseEntity.ok(updatedCoffee);
                })
                .orElse(ResponseEntity.notFound().build());
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> deleteCoffee(@PathVariable Long id) {
        try {
            if (coffeeRepository.existsById(id)) {
                coffeeRepository.deleteById(id);
                return ResponseEntity.ok().build();
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            return ResponseEntity.badRequest().build();
        }
    }
}
