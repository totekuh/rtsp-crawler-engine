package com.storage.cameras.dao;

import com.storage.cameras.model.Camera;
import com.storage.cameras.model.Label;
import java.util.List;

public interface LabelDao {
    
    Label findByName(String name);
    
    Label save(Label label);

    List<Label> findLabelsByCamera(Camera camera);
}
