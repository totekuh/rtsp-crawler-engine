package com.storage.cameras.service;

import com.storage.cameras.model.Camera;
import com.storage.cameras.model.Label;
import com.storage.cameras.rest.params.LabelParams;
import java.util.List;

public interface LabelService {

    Label findOrCreateLabel(LabelParams labelParams);

    void save(Label label);

    void markCameraWithLabel(Camera camera, Label label);

    List<Label> getLabelsByCamera(Camera camera);
}
