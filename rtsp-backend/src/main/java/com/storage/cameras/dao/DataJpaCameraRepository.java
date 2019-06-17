package com.storage.cameras.dao;

import com.storage.cameras.model.Camera;
import com.storage.cameras.model.CameraStatus;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface DataJpaCameraRepository extends JpaRepository<Camera, Long> {
    Camera getById(Long id);

    Camera getByUrl(String url);

    List<Camera> findAll();

    List<Camera> findAllByStatus(CameraStatus status);

    List<Camera> findAllByCountryCode(String countryCode);

    List<Camera> findAllByStatusAndCountryCode(CameraStatus status, String countryCode);


}
