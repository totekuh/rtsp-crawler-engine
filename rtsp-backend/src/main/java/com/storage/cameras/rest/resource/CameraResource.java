package com.storage.cameras.rest.resource;

import com.storage.cameras.model.Keyword;
import java.util.List;
import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class CameraResource {

    private final Long cameraId;

    private final String rtspUrl;

    private final List<CommentResource> comments;

    private final String creationTimestamp;

    private final String lastUpdateTimestamp;

    private final String status;

    private final String countryName;

    private final String countryCode;

    private final String city;

    private final Set<Keyword> keywords;
    
    private final String base64ImageData;
    
    private final Set<LabelResource> labels;
}
