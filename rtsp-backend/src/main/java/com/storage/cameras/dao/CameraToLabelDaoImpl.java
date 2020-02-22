package com.storage.cameras.dao;

import com.storage.cameras.dao.datajpa.DataJpaCameraToLabelRepository;
import com.storage.cameras.model.CameraToLabel;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Repository;

@Repository
@AllArgsConstructor
public class CameraToLabelDaoImpl implements CameraToLabelDao {
    private final DataJpaCameraToLabelRepository dataJpaCameraToLabelRepository;

    @Override
    public void save(CameraToLabel cameraToLabel) {
        dataJpaCameraToLabelRepository.save(cameraToLabel);
    }
}
