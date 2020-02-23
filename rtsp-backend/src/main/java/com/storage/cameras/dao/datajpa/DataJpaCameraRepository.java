package com.storage.cameras.dao.datajpa;

import com.storage.cameras.model.Camera;
import com.storage.cameras.model.CameraStatus;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface DataJpaCameraRepository extends JpaRepository<Camera, Long> {
    Camera getById(Long id);

    Camera getByUrl(String url);

    List<Camera> findAll();

    List<Camera> findAllByStatus(CameraStatus status);

    List<Camera> findAllByStatusAndCountryCode(CameraStatus status, String countryCode);

    List<Camera> findAllByStatusAndCity(CameraStatus status, String city);

    @Query(nativeQuery = true,
            value = "SELECT * FROM cameras_db.camera " +
                    "WHERE city IS NULL " +
                    "OR country_code IS NULL " +
                    "OR country_name IS NULL")
    List<Camera> findWithNoGeolocation();

    @Query(nativeQuery = true, value = "SELECT id FROM camera")
    List<Long> getAllIds();

    @Query(nativeQuery = true, value =
            "SELECT id FROM camera c " +
                    "WHERE EXISTS (SELECT 1 FROM camera_to_label ctl WHERE ctl.camera_id = c.id AND " +
                    "ctl.label_id =:labelId) ")
    List<Long> findMarkedByLabelId(@Param(value = "labelId") Long labelId);
}
