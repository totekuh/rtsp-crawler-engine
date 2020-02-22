package com.storage.cameras.mapper;

import com.storage.cameras.model.Label;
import com.storage.cameras.rest.resource.LabelResource;

public interface LabelToResourceMapper {
    LabelToResourceMapper INSTANCE = label -> new LabelResource(label.getId(), label.getName());

    LabelResource convert(Label comment);
}
