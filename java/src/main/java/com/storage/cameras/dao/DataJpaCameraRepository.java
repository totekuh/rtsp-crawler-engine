package com.storage.cameras.dao;

import com.storage.cameras.model.Camera;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DataJpaCameraRepository extends JpaRepository<Camera, Long> {
    Camera getById(Long id);

    Camera getByUrl(String url);
}
