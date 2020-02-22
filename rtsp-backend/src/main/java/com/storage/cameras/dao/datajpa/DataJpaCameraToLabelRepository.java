package com.storage.cameras.dao.datajpa;

import com.storage.cameras.model.CameraToLabel;
import org.springframework.data.jpa.repository.JpaRepository;

public interface DataJpaCameraToLabelRepository extends JpaRepository<CameraToLabel, Long> {
}
