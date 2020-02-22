package com.storage.cameras.dao;

import com.storage.cameras.model.Label;

public interface LabelDao {
    
    Label findByName(String name);
    
    Label save(Label label);
}
