package com.storage.cameras.dao.datajpa;

import com.storage.cameras.model.CameraToLabel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface DataJpaCameraToLabelRepository extends JpaRepository<CameraToLabel, Long> {
    @Query(nativeQuery = true,
            value = "DELETE FROM camera_to_label WHERE camera_id = :cameraId")
    void deleteByCameraId(@Param(value = "cameraId") Long cameraId);
}
