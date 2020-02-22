package com.storage.cameras.service;

import com.storage.cameras.model.Camera;
import com.storage.cameras.model.Label;
import com.storage.cameras.rest.params.LabelParams;

public interface LabelService {
    
    Label findOrCreateLabel(LabelParams labelParams);

    void save(Label label);

    void markCameraWithLabel(Camera camera, Label label);
}
