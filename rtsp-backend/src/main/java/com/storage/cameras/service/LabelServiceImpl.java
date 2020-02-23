package com.storage.cameras.service;

import com.storage.cameras.dao.CameraToLabelDao;
import com.storage.cameras.dao.LabelDao;
import com.storage.cameras.model.Camera;
import com.storage.cameras.model.CameraToLabel;
import com.storage.cameras.model.Label;
import com.storage.cameras.rest.params.LabelParams;
import java.util.List;
import static java.util.Optional.ofNullable;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import static org.springframework.transaction.annotation.Propagation.REQUIRED;
import org.springframework.transaction.annotation.Transactional;

@Service
@Slf4j
@Transactional(propagation = REQUIRED)
@AllArgsConstructor
public class LabelServiceImpl implements LabelService {
    private final LabelDao labelDao;
    private final CameraToLabelDao cameraToLabelDao;

    @Override
    public Label findOrCreateLabel(LabelParams labelParams) {
        final String labelName = labelParams.getName();
        return ofNullable(labelDao.findByName(labelName))
                .orElseGet(() -> {
                    final Label newLabel = new Label();
                    newLabel.setName(labelName);
                    return labelDao.save(newLabel);
                });
    }

    @Override
    public void save(Label label) {
        labelDao.save(label);
    }

    @Override
    public void markCameraWithLabel(Camera camera, Label label) {
        final CameraToLabel cameraToLabel = new CameraToLabel();
        cameraToLabel.setCamera(camera);
        cameraToLabel.setLabel(label);
        cameraToLabelDao.save(cameraToLabel);
    }

    @Override
    public List<Label> getLabelsByCamera(Camera camera) {
        return labelDao.findLabelsByCamera(camera);
    }

    @Override
    public void unlinkLabelsFromCamera(Long cameraId) {
        cameraToLabelDao.deleteByCameraId(cameraId);
    }
}
